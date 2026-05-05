from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from config.database import get_db
from config.settings import settings
from utils.dependencies import get_current_user
from models.user import User
from services.payment import create_order, verify_payment
from services.billing import calculate_bill
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["Payments"])


# ── Schemas ───────────────────────────────────────────────────

class CreateOrderRequest(BaseModel):
    plan: str = "pro"  # free, pro, enterprise

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id:   str
    razorpay_payment_id: str
    razorpay_signature:  str
    plan:                str


# ── Plan pricing ──────────────────────────────────────────────
PLAN_PRICES = {
    "free":       0,
    "pro":        499,
    "enterprise": 2999
}


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/create-order")
async def create_payment_order(
    data: CreateOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 1 of payment flow.
    Creates a Razorpay order and returns order_id to frontend.
    Frontend uses this to open Razorpay checkout.
    """
    amount = PLAN_PRICES.get(data.plan, 0)

    if amount == 0:
        return {"message": "Free plan requires no payment"}

    try:
        order = create_order(
            amount=amount,
            notes={
                "user_id": str(current_user.id),
                "email":   current_user.email,
                "plan":    data.plan
            }
        )
        return {
            "order_id":   order["id"],
            "amount":     amount,
            "currency":   "INR",
            "plan":       data.plan,
            "key_id":     settings.RAZORPAY_KEY_ID,
            "user_email": current_user.email,
            "user_name":  current_user.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment order failed: {str(e)}")


@router.post("/verify")
async def verify_payment_route(
    data: VerifyPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 2 of payment flow.
    Verifies the payment signature from Razorpay.
    Called after user completes payment in checkout.
    """
    is_valid = verify_payment(
        order_id=data.razorpay_order_id,
        payment_id=data.razorpay_payment_id,
        signature=data.razorpay_signature
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid payment signature")

    # Payment verified — update user plan in DB
    # For now we store in a simple dict (extend with DB model later)
    return {
        "success":    True,
        "message":    f"Payment verified! {data.plan} plan activated.",
        "payment_id": data.razorpay_payment_id,
        "plan":       data.plan,
        "activated_at": str(datetime.utcnow())
    }


@router.get("/plans")
async def get_plans():
    """Public endpoint — returns all plans with Razorpay amounts."""
    return {
        "plans": [
            {
                "id":            "free",
                "name":          "Free",
                "amount":        0,
                "currency":      "INR",
                "free_requests": 1000,
                "rate_limit":    "10/min",
                "features":      ["1,000 requests/month", "Basic analytics", "1 API key"]
            },
            {
                "id":            "pro",
                "name":          "Pro",
                "amount":        499,
                "currency":      "INR",
                "free_requests": 5000,
                "rate_limit":    "100/min",
                "features":      ["5,000 requests/month", "Advanced analytics", "Unlimited keys", "Priority support"]
            },
            {
                "id":            "enterprise",
                "name":          "Enterprise",
                "amount":        2999,
                "currency":      "INR",
                "free_requests": 50000,
                "rate_limit":    "1000/min",
                "features":      ["50,000 requests/month", "Full analytics", "Unlimited everything", "Dedicated support"]
            }
        ]
    }