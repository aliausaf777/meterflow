import httpx
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import SessionLocal, usage_logs, redis_client
from models.api_key import APIKey
from models.api import API
from datetime import datetime
import time


async def gateway_middleware(request: Request, call_next):
    # Only intercept /gateway/ routes
    excluded = ["/gateway/my-usage", "/gateway/info"]
    if not request.url.path.startswith("/gateway/") or request.url.path in excluded:
        return await call_next(request)

    start_time = time.time()

    # Step 1: Extract API key from URL
    # Format: /gateway/{api_key}/endpoint
    parts = request.url.path.split("/")

    if len(parts) < 3:
        return JSONResponse(status_code=400, content={"error": "Invalid gateway URL format"})

    api_key_value = parts[2]
    downstream_path = "/" + "/".join(parts[3:]) if len(parts) > 3 else "/"

    # Step 2: Validate API Key in MySQL
    db: Session = SessionLocal()
    try:
        api_key = db.query(APIKey).filter(
            APIKey.key_value == api_key_value,
            APIKey.status == "active"
        ).first()

        if not api_key:
            await _log_request(
                api_key=api_key_value,
                endpoint=downstream_path,
                method=request.method,
                status_code=401,
                latency_ms=0,
                error="Invalid or revoked API key"
            )
            return JSONResponse(status_code=401, content={"error": "Invalid or revoked API key"})

        # Check if key is expired
        if api_key.expires_at and api_key.expires_at < datetime.utcnow():
            api_key.status = "expired"
            db.commit()
            return JSONResponse(status_code=401, content={"error": "API key has expired"})

        # Get the associated API
        api = db.query(API).filter(API.id == api_key.api_id).first()
        if not api or not api.is_active:
            return JSONResponse(status_code=404, content={"error": "API not found or inactive"})

        # Step 3: Rate Limiting with Redis
        rate_limit_result = await _check_rate_limit(api_key_value)
        if not rate_limit_result["allowed"]:
            await _log_request(
                api_key=api_key_value,
                endpoint=downstream_path,
                method=request.method,
                status_code=429,
                latency_ms=0,
                error="Rate limit exceeded"
            )
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "limit": rate_limit_result["limit"],
                    "retry_after": "60 seconds"
                }
            )

        # Step 4: Forward request to real API
        target_url = api.base_url.rstrip("/") + downstream_path

        # Forward query parameters
        if request.url.query:
            target_url += f"?{request.url.query}"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                forwarded = await client.request(
                    method=request.method,
                    url=target_url,
                    headers={
                        k: v for k, v in request.headers.items()
                        if k.lower() not in ("host", "authorization")
                    },
                    content=await request.body()
                )

            latency_ms = int((time.time() - start_time) * 1000)

            # Update last_used_at
            api_key.last_used_at = datetime.utcnow()
            db.commit()

            # Step 5: Log to MongoDB
            await _log_request(
                api_key=api_key_value,
                api_id=api.id,
                user_id=api_key.user_id,
                endpoint=downstream_path,
                method=request.method,
                status_code=forwarded.status_code,
                latency_ms=latency_ms
            )

            # Step 6: Return response
            return Response(
                content=forwarded.content,
                status_code=forwarded.status_code,
                headers=dict(forwarded.headers),
                media_type=forwarded.headers.get("content-type")
            )

        except httpx.TimeoutException:
            latency_ms = int((time.time() - start_time) * 1000)
            await _log_request(
                api_key=api_key_value,
                endpoint=downstream_path,
                method=request.method,
                status_code=504,
                latency_ms=latency_ms,
                error="Upstream timeout"
            )
            return JSONResponse(status_code=504, content={"error": "Upstream API timed out"})

        except httpx.RequestError as e:
            return JSONResponse(status_code=502, content={"error": f"Could not reach upstream API: {str(e)}"})

    finally:
        db.close()


async def _check_rate_limit(api_key: str, limit: int = 60) -> dict:
    try:
        redis_key = f"rate:{api_key}"
        current = await redis_client.incr(redis_key)
        if current == 1:
            await redis_client.expire(redis_key, 60)
        if current > limit:
            return {"allowed": False, "limit": limit, "current": current}
        return {"allowed": True, "limit": limit, "current": current}
    except Exception:
        return {"allowed": True, "limit": limit, "current": 0}


async def _log_request(
    api_key: str,
    endpoint: str,
    method: str,
    status_code: int,
    latency_ms: int,
    api_id: int = None,
    user_id: int = None,
    error: str = None
):
    try:
        log = {
            "api_key":     api_key,
            "api_id":      api_id,
            "user_id":     user_id,
            "endpoint":    endpoint,
            "method":      method,
            "status_code": status_code,
            "latency_ms":  latency_ms,
            "timestamp":   datetime.utcnow(),
            "error":       error,
            "success":     status_code < 400
        }
        await usage_logs.insert_one(log)
    except Exception as e:
        print(f"[Gateway] MongoDB log failed: {e}")