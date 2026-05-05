import razorpay
import hmac
import hashlib
from config.settings import settings

# Initialize Razorpay client
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def create_order(amount: float, currency: str = "INR", notes: dict = {}) -> dict:
    """
    Create a Razorpay order.
    Amount is in rupees — we convert to paise (x100).
    """
    data = {
        "amount": int(amount * 100),  # Convert to paise
        "currency": currency,
        "notes": notes
    }
    order = client.order.create(data=data)
    return order


def verify_payment(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Verify Razorpay payment signature.
    This is critical — never skip verification!
    """
    message = f"{order_id}|{payment_id}"
    generated_signature = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(generated_signature, signature)