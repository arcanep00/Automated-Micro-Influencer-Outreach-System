import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL", "")
NICHE = os.getenv("NICHE", "fitness")

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "influencers.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

MIN_FOLLOWERS = 5000
MAX_FOLLOWERS = 100000
MIN_ENGAGEMENT_RATE = 2.0
MIN_INFLUENCERS_REQUIRED = 50
