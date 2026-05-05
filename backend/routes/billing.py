from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from utils.dependencies import get_current_user
from models.user import User
from services.billing import calculate_bill, get_usage_summary

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("/invoice")
async def get_invoice(
    plan: str = "free",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current month's invoice for the logged-in user.
    Shows total requests, billable requests, and amount due.
    
    Query param: ?plan=free|pro|enterprise
    """
    return await calculate_bill(current_user.id, plan)


@router.get("/usage")
async def get_usage(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get usage summary for the last N days.
    Returns daily breakdown perfect for dashboard charts.
    
    Query param: ?days=7|30|90
    """
    return await get_usage_summary(current_user.id, days)


@router.get("/plans")
async def get_plans():
    """
    Get all available pricing plans.
    No auth required — public endpoint.
    """
    return {
        "plans": [
            {
                "name":             "Free",
                "id":               "free",
                "price":            "₹0/month",
                "free_requests":    1000,
                "price_per_100":    "₹0",
                "rate_limit":       "10 req/min",
                "features": [
                    "1000 free requests/month",
                    "Basic analytics",
                    "1 API key"
                ]
            },
            {
                "name":             "Pro",
                "id":               "pro",
                "price":            "₹499/month",
                "free_requests":    5000,
                "price_per_100":    "₹0.50",
                "rate_limit":       "100 req/min",
                "features": [
                    "5000 free requests/month",
                    "Advanced analytics",
                    "Unlimited API keys",
                    "Priority support"
                ]
            },
            {
                "name":             "Enterprise",
                "id":               "enterprise",
                "price":            "₹2999/month",
                "free_requests":    50000,
                "price_per_100":    "₹0.20",
                "rate_limit":       "1000 req/min",
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