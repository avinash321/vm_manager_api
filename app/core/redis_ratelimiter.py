# app/core/redis_ratelimiter.py

import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from redis import Redis
from app.core.config import REDIS_RATELIMIT


# Redis connection (use your actual URL or env variable)
redis_client = Redis.from_url(REDIS_RATELIMIT)


# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,   # IP-based limiting
    storage_uri=REDIS_RATELIMIT          # Redis backend
)


# Custom rate limit exceeded handler
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Try again later."
        }
    )