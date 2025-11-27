"""
Quick test to verify Twitter connection
"""

from integrations.twitter import TwitterClient
from utils.logger import logger
from config.settings import settings

def test_connection():
    print("\n🧪 Testing Twitter Connection...\n")
    
    if settings.DEV_MODE:
        print("⚠️  DEV_MODE is enabled - tweet will not actually post")
    
    client = TwitterClient()
    
    # Test: Post a simple tweet
    test_tweet = "🧪 test tweet from PolyPuff development. beep boop! 🥚"
    success = client.post_tweet(test_tweet)
    
    if success:
        print("\n✅ SUCCESS!")
        if settings.DEV_MODE:
            print("Check logs to see the test tweet content")
        else:
            print("Check your @PolyPuffAgent Twitter account to see the tweet!")
    else:
        print("\n❌ FAILED! Check logs for errors.")
    
    return success


if __name__ == "__main__":
    test_connection()