# loading content from .env file

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    RATE_LIMIT_COUNT = int(os.getenv("RATE_LIMIT_COUNT", "10"))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "300"))

settings = Config()
