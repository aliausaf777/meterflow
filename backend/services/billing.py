from sqlalchemy.orm import Session
from config.database import usage_logs
from models.user import User
from datetime import datetime, timedelta


# ── Pricing Plans ─────────────────────────────────────────────
PLANS = {
    "free": {
        "free_requests": 1000,
        "price_per_100": 0.0,
        "monthly_price": 0.0,
    },
    "pro": {
        "free_requests": 5000,
        "price_per_100": 0.5,
        "monthly_price": 499.0,
    },
    "enterprise": {
        "free_requests": 50000,
        "price_per_100": 0.2,
        "monthly_price": 2999.0,
    }
}


async def calculate_bill(user_id: int, plan: str = "free") -> dict:
    """
    Calculate billing for a user for the current month.
    
    Steps:
    1. Get current billing period (start of month → now)
    2. Count total requests from MongoDB
    3. Subtract free tier
    4. Apply pricing
    5. Return invoice data
    """

    # Step 1: Billing period = current month
    now = datetime.utcnow()
    period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    period_end = now

    # Step 2: Count requests this month from MongoDB
    total_requests = await usage_logs.count_documents({
        "user_id": user_id,
        "timestamp": {
            "$gte": period_start,
            "$lte": period_end
        }
    })

    # Count successful requests only
    successful_requests = await usage_logs.count_documents({
        "user_id": user_id,
        "success": True,
        "timestamp": {
            "$gte": period_start,
            "$lte": period_end
        }
    })

    # Step 3: Apply free tier
    plan_config = PLANS.get(plan, PLANS["free"])
    free_requests = plan_config["free_requests"]
    billable_requests = max(0, total_requests - free_requests)

    # Step 4: Calculate cost
    # Price is per 100 requests
    usage_cost = (billable_requests / 100) * plan_config["price_per_100"]
    base_cost = plan_config["monthly_price"]
    total_amount = round(base_cost + usage_cost, 2)

    # Step 5: Per-endpoint breakdown from MongoDB
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "timestamp": {"$gte": period_start, "$lte": period_end}
            }
        },
        {
            "$group": {
                "_id": "$endpoint",
                "count": {"$sum": 1},
                "avg_latency": {"$avg": "$latency_ms"},
                "errors": {
                    "$sum": {"$cond": [{"$eq": ["$success", False]}, 1, 0]}
                }
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    endpoint_breakdown = await usage_logs.aggregate(pipeline).to_list(10)

    # Clean up MongoDB _id field
    for item in endpoint_breakdown:
        item["endpoint"] = item.pop("_id")
        item["avg_latency"] = round(item["avg_latency"] or 0, 2)

    return {
        "user_id":            user_id,
        "plan":               plan,
        "billing_period": {
            "start":          str(period_start.date()),
            "end":            str(period_end.date()),
        },
        "usage": {
            "total_requests":      total_requests,
            "successful_requests": successful_requests,
            "failed_requests":     total_requests - successful_requests,
            "free_requests":       free_requests,
            "free_used":           min(total_requests, free_requests),
            "billable_requests":   billable_requests,
        },
        "cost": {
            "base_monthly":   base_cost,
            "usage_cost":     round(usage_cost, 2),
            "total_amount":   total_amount,
            "currency":       "INR",
        },
        "endpoint_breakdown": endpoint_breakdown,
        "generated_at":       str(now),
    }


async def get_usage_summary(user_id: int, days: int = 30) -> dict:
    """
    Get usage summary for the last N days.
    Used for the dashboard graph.
    """
    now = datetime.utcnow()
    since = now - timedelta(days=days)

    # Daily request counts
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "timestamp": {"$gte": since}
            }
        },
        {
            "$group": {
                "_id": {
                    "year":  {"$year": "$timestamp"},
                    "month": {"$month": "$timestamp"},
                    "day":   {"$dayOfMonth": "$timestamp"}
                },
                "total":   {"$sum": 1},
                "success": {"$sum": {"$cond": ["$success", 1, 0]}},
                "avg_latency": {"$avg": "$latency_ms"}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    daily_data = await usage_logs.aggregate(pipeline).to_list(days)

    # Format for frontend chart
    chart_data = []
    for d in daily_data:
        chart_data.append({
            "date": f"{d['_id']['year']}-{d['_id']['month']:02d}-{d['_id']['day']:02d}",
            "total":       d["total"],
            "success":     d["success"],
            "failed":      d["total"] - d["success"],
            "avg_latency": round(d["avg_latency"] or 0, 2)
        })

    total = sum(d["total"] for d in chart_data)
    success = sum(d["success"] for d in chart_data)

    return {
        "period_days":    days,
        "total_requests": total,
        "success_rate":   f"{round((success/total)*100, 1)}%" if total > 0 else "0%",
        "chart_data":     chart_data
    }