import time
import redis
from fastapi import Depends
from app.config import get_settings

settings = get_settings()

redis_client = redis.Redis.from_url(settings.REDIS_URL)


def rate_limiter(request=None):
    """
    Sliding‑window rate limiter.
    Allows RATE_LIMIT_REQUESTS per RATE_LIMIT_WINDOW seconds.
    """

    # Extract user phone from Twilio webhook
    if request:
        form = request.form()
        user_phone = form.get("From", "unknown")
    else:
        user_phone = "unknown"

    key = f"rate_limit:{user_phone}"
    now = time.time()

    # Add current timestamp
    redis_client.zadd(key, {now: now})

    # Remove old timestamps
    redis_client.zremrangebyscore(
        key,
        0,
        now - settings.RATE_LIMIT_WINDOW
    )

    # Count remaining requests
    count = redis_client.zcard(key)

    if count > settings.RATE_LIMIT_REQUESTS:
        return True  # rate limited

    return False
