import redis
import json
from app.core.config import REDIS_CACHE

redis_client = redis.from_url(
    REDIS_CACHE,
    decode_responses=True  # important for string handling
)

print("Redis Initiated")

def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value: dict, ttl: int = 300):
    redis_client.setex(key, ttl, json.dumps(value))

def delete_cache(key: str):
    redis_client.delete(key)


"""
# Local Redis DB Connection
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
"""