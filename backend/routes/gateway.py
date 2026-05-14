from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.database import get_db, usage_logs
from utils.dependencies import get_current_user
from models.user import User
from models.api_key import APIKey
from models.api import API
import httpx
import time

router = APIRouter(prefix="/gateway", tags=["API Gateway"])


@router.get("/info")
async def gateway_info():
    return {
        "message": "MeterFlow API Gateway",
        "usage": "Make requests to /gateway/{your_api_key}/{endpoint}",
        "example": "/gateway/mf_abc123/pokemon/1",
        "docs": "Every request is logged, rate limited, and billed"
    }


@router.get("/my-usage")
async def my_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dashboard analytics using in-memory usage_logs list.
    """

    try:
        user_logs = [
            log for log in usage_logs
            if log["user_id"] == current_user.id
        ]

        total = len(user_logs)

        success = len([
            log for log in user_logs
            if log["success"]
        ])

        failed = total - success

        avg_latency = round(
            sum(log["latency_ms"] for log in user_logs) / total,
            2
        ) if total > 0 else 0

        max_latency = max(
            [log["latency_ms"] for log in user_logs],
            default=0
        )

        recent = user_logs[-5:][::-1]

        return {
            "user_id": current_user.id,
            "total_requests": total,
            "successful": success,
            "failed": failed,
            "success_rate": f"{round((success / total) * 100, 1)}%" if total > 0 else "0%",
            "avg_latency_ms": avg_latency,
            "max_latency_ms": max_latency,
            "recent_requests": recent
        }

    except Exception as e:
        return {"error": str(e)}


@router.api_route("/{api_key_value}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_proxy(
    api_key_value: str,
    path: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Main API Gateway proxy route.
    """

    start = time.time()

    try:
        # Find API key
        api_key = db.query(APIKey).filter(
            APIKey.key_value == api_key_value
        ).first()

        if not api_key:
            return {"error": "Invalid or revoked API key"}

        if api_key.status != "active":
            return {"error": "Invalid or revoked API key"}

        # Find API
        api = db.query(API).filter(
            API.id == api_key.api_id
        ).first()

        if not api:
            return {"error": "API not found"}

        # Build upstream URL
        upstream_url = f"{api.base_url.rstrip('/')}/{path}"

        # Forward request
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=upstream_url,
                params=request.query_params
            )

        latency_ms = round((time.time() - start) * 1000, 2)

        # Log usage
        usage_logs.append({
            "user_id": api.user_id,
            "endpoint": path,
            "method": request.method,
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "latency_ms": latency_ms
        })

        # Return JSON response
        try:
            return response.json()
        except Exception:
            return {
                "status_code": response.status_code,
                "content": response.text
            }

    except Exception as e:
        return {
            "error": f"Could not reach upstream API: {str(e)}"
        }