"""Configuration settings"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DATA_PATH = os.getenv("DATA_PATH", "data/")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8501").split(",")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
