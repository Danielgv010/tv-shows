"""Central settings. Values come from the .env file (or real environment variables)."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# From .env
COUNTRY = os.getenv("TVMAZE_COUNTRY", "US").upper()
SHOW_COUNT = int(os.getenv("SHOW_COUNT", "20"))
DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Fixed values
TRENDING_TTL = 60 * 60                 # refresh trending hourly
