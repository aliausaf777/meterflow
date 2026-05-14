from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from utils.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("/invoice")
async def get_invoice(
    plan: str = "free",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Safe invoice endpoint for local/demo setup.
    """

    pricing = {
        "free": {
            "free_requests": 1000,
            "price_per_100": 0
        },
        "pro": {
            "free_requests": 5000,
            "price_per_100": 0.5
        },
        "enterprise": {
            "free_requests": 50000,
            "price_per_100": 0.2
        }
    }

    plan_data = pricing.get(plan, pricing["free"])

    total_requests = 0
    free_requests = plan_data["free_requests"]

    billable_requests = max(
        total_requests - free_requests,
        0
    )

    total_amount = round(
        (billable_requests / 100) * plan_data["price_per_100"],
        2
    )

    return {
        "billing_period": {
            "start": "2026-05-01",
            "end": "2026-05-31"
        },
        "plan": plan,
        "usage": {
            "total_requests": total_requests,
            "free_requests": free_requests,
            "billable_requests": billable_requests
        },
        "cost": {
            "price_per_100": plan_data["price_per_100"],
            "total_amount": total_amount
        }
    }


@router.get("/usage")
async def get_usage(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Safe usage analytics endpoint.
    """

    chart_data = []

    for i in range(days):
        chart_data.append({
            "date": f"2026-05-{str(i + 1).zfill(2)}",
            "total": 0
        })

    return {
        "days": days,
        "chart_data": chart_data,
        "summary": {
            "total_requests": 0,
            "success_rate": "100%",
            "avg_latency_ms": 0
        }
    }


@router.get("/plans")
async def get_plans():
    """
    Get all available pricing plans.
    """

    return {
        "plans": [
            {
                "name": "Free",
                "id": "free",
                "price": "₹0/month",
                "free_requests": 1000,
                "price_per_100": "₹0",
                "rate_limit": "10 req/min",
                "features": [
                    "1000 free requests/month",
                    "Basic analytics",
                    "1 API key"
                ]
            },
            {
                "name": "Pro",
                "id": "pro",
                "price": "₹499/month",
                "free_requests": 5000,
                "price_per_100": "₹0.50",
                "rate_limit": "100 req/min",
                "features": [
                    "5000 free requests/month",
                    "Advanced analytics",
                    "Unlimited API keys",
                    "Priority support"
                ]
            },
            {
                "name": "Enterprise",
                "id": "enterprise",
                "price": "₹2999/month",
                "free_requests": 50000,
                "price_per_100": "₹0.20",
                "rate_limit": "1000 req/min",
                "features": [
                    "50000 free requests/month",
                    "Full analytics + export",
                    "Unlimited everything",
                    "Dedicated support",
                    "Custom rate limits"
                ]
            }
        ]
    }