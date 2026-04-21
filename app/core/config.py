import os

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
EMAIL_TO_SENT = os.getenv("EMAIL_TO_SENT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
REDIS_URL = os.getenv("REDIS_URL")
#REDIS_URL = os.getenv("RABBITMQ_URL")
REDIS_CACHE = os.getenv("REDIS_CACHE")

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")