import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Configuration settings loaded from environment variables
    """
    
    # Google Gemini API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Twitter API
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    
    # Base Blockchain (will use on Day 3)
    BASE_WALLET_ADDRESS = os.getenv("BASE_WALLET_ADDRESS", "")
    BASE_WALLET_PRIVATE_KEY = os.getenv("BASE_WALLET_PRIVATE_KEY", "")
    BASE_RPC_URL = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
    
    # Agent Settings
    TWEET_INTERVAL_MINUTES = int(os.getenv("TWEET_INTERVAL_MINUTES", 60))
    CHECK_BALANCE_INTERVAL_MINUTES = int(os.getenv("CHECK_BALANCE_INTERVAL_MINUTES", 15))
    DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

settings = Settings()