from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db, usage_logs
from utils.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/gateway", tags=["API Gateway"])


@router.get("/info")
async def gateway_info():
    """
    Gateway info endpoint.
    Shows how to use the MeterFlow gateway.
    """
    return {
        "message": "MeterFlow API Gateway",
        "usage": "Make requests to /gateway/{your_api_key}/{endpoint}",
        "example": "/gateway/mf_abc123.../pokemon/ditto",
        "docs": "Every request is logged, rate limited, and billed"
    }


@router.get("/my-usage")
async def my_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get usage stats for the current user from MongoDB.
    Returns total requests, success rate, and per-endpoint breakdown.
    """
    try:
        # Total requests by this user
        total = await usage_logs.count_documents({"user_id": current_user.id})

        # Successful requests
        success = await usage_logs.count_documents({
            "user_id": current_user.id,
            "success": True
        })

        # Failed requests
        failed = await usage_logs.count_documents({
            "user_id": current_user.id,
            "success": False
        })

        # Average latency
        pipeline = [
            {"$match": {"user_id": current_user.id}},
            {"$group": {
                "_id": None,
                "avg_latency": {"$avg": "$latency_ms"},
                "max_latency": {"$max": "$latency_ms"}
            }}
        ]
        latency_result = await usage_logs.aggregate(pipeline).to_list(1)
        avg_latency = round(latency_result[0]["avg_latency"], 2) if latency_result else 0
        max_latency = latency_result[0]["max_latency"] if latency_result else 0

        # Recent 5 requests
        recent = await usage_logs.find(
            {"user_id": current_user.id},
            {"_id": 0}  # Exclude MongoDB _id
        ).sort("timestamp", -1).limit(5).to_list(5)

        # Convert datetime to string for JSON
        for r in recent:
            if "timestamp" in r:
                r["timestamp"] = str(r["timestamp"])

        return {
            "user_id":      current_user.id,
            "total_requests": total,
            "successful":   success,
            "failed":       failed,
            "success_rate": f"{round((success/total)*100, 1)}%" if total > 0 else "0%",
            "avg_latency_ms": avg_latency,
            "max_latency_ms": max_latency,
            "recent_requests": recent
        }

    except Exception as e:
        return {"error": str(e)}