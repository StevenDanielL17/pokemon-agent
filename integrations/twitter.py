import tweepy
import os
from dotenv import load_dotenv
from utils.logger import logger
from typing import Optional

load_dotenv()

class TwitterClient:
    """
    Handles all Twitter API interactions
    """
    
    def __init__(self):
        # Load credentials from .env
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        
        # Initialize Tweepy Client (v2 API)
        if self.api_key and self.api_secret and self.access_token and self.access_secret:
             self.client = tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret
            )
             
             # Initialize API v1.1 for media uploads (images)
             auth = tweepy.OAuth1UserHandler(
                self.api_key, 
                self.api_secret,
                self.access_token,
                self.access_secret
            )
             self.api_v1 = tweepy.API(auth)
             logger.info("✅ Twitter client initialized successfully")
        else:
            logger.warning("⚠️ Twitter credentials missing in .env")
            self.client = None
            self.api_v1 = None

    
    def post_tweet(self, text: str, image_path: Optional[str] = None) -> bool:
        """
        Post a tweet with optional image
        
        Args:
            text: Tweet content (max 280 characters)
            image_path: Path to image file (optional)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("❌ Twitter client not initialized")
            return False

        try:
            # Validate tweet length
            if len(text) > 280:
                logger.error(f"❌ Tweet too long: {len(text)} characters")
                text = text[:277] + "..."  # Truncate with ellipsis
            
            # Handle image upload if provided
            media_id = None
            if image_path and os.path.exists(image_path):
                media = self.api_v1.media_upload(filename=image_path)
                media_id = media.media_id
                logger.info(f"📸 Image uploaded: {image_path}")
            
            # Post tweet
            if media_id:
                response = self.client.create_tweet(
                    text=text,
                    media_ids=[media_id]
                )
            else:
                response = self.client.create_tweet(text=text)
            
            tweet_id = response.data['id']
            logger.info(f"✅ Tweet posted successfully! ID: {tweet_id}")
            logger.info(f"📝 Content: {text}")
            
            return True
            
        except tweepy.TweepyException as e:
            logger.error(f"❌ Twitter API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error posting tweet: {str(e)}")
            return False
    
    def get_mentions(self, limit: int = 10):
        """
        Get recent mentions of the bot
        (For Day 4 - mention handling)
        """
        if not self.client:
             return []

        try:
            mentions = self.client.get_users_mentions(
                id=self.get_my_user_id(),
                max_results=limit
            )
            return mentions.data if mentions.data else []
        except Exception as e:
            logger.error(f"❌ Error fetching mentions: {str(e)}")
            return []
    
    def get_my_user_id(self) -> str:
        """
        Get the authenticated user's Twitter ID
        """
        if not self.client:
            return None

        try:
            user = self.client.get_me()
            return user.data.id
        except Exception as e:
            logger.error(f"❌ Error getting user ID: {str(e)}")
            return None
    
    def update_profile_image(self, image_path: str) -> bool:
        """
        Update profile picture (for evolution events)
        """
        if not self.api_v1:
            return False

        try:
            self.api_v1.update_profile_image(filename=image_path)
            logger.info(f"✅ Profile image updated: {image_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating profile image: {str(e)}")
            return False


# Quick test function
def test_twitter_connection():
    """
    Test if Twitter credentials work
    """
    try:
        client = TwitterClient()
        test_tweet = "🥚 beep boop... testing my circuits... im alive! (test tweet, pls ignore)"
        # Only try to post if client is initialized
        if client.client:
            success = client.post_tweet(test_tweet)
            
            if success:
                print("✅ Twitter connection SUCCESS!")
                print("Check your Twitter account to see the test tweet")
            else:
                print("❌ Twitter connection FAILED")
                print("Check your credentials in .env file")
        else:
             print("❌ Twitter client not initialized (missing credentials?)")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    # Run this file directly to test
    test_twitter_connection()
