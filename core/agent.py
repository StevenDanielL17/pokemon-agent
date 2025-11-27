import time
from datetime import datetime
from integrations.twitter import TwitterClient
from integrations.gemini_client import GeminiClient
from config.prompts import STAGE_PROMPTS
from utils.logger import logger
import json
import os

class PolyPuffAgent:
    """
    Main agent logic - the brain of PolyPuff
    """
    
    def __init__(self):
        # Initialize clients
        self.twitter = TwitterClient()
        self.ai = GeminiClient()
        
        # Agent state
        self.stage = "egg"  # Start as egg
        self.balance = 0.0
        self.tweet_count = 0
        
        # Load previous state if exists
        self.load_state()
        
        logger.info(f"🥚 PolyPuff initialized! Current stage: {self.stage}")
    
    def think_and_tweet(self):
        """
        Main action loop - called every hour
        """
        logger.info("🧠 PolyPuff is thinking...")
        
        try:
            # Build context for AI
            context = {
                "balance": self.balance,
                "stage": self.stage,
                "recent_activity": "No transactions yet",  # Will add wallet check on Day 3
                "time_of_day": self.get_time_of_day(),
                "tweet_count": self.tweet_count
            }
            
            # Generate tweet using AI
            tweet_text = self.ai.generate_tweet(self.stage, context)
            
            # Get image for current stage
            image_path = STAGE_PROMPTS[self.stage].get("image")
            if image_path and not os.path.exists(image_path):
                image_path = None  # Don't use image if file missing
            
            # Post to Twitter
            success = self.twitter.post_tweet(tweet_text, image_path)
            
            if success:
                self.tweet_count += 1
                self.save_state()
                logger.info(f"✅ Tweet #{self.tweet_count} posted!")
            
        except Exception as e:
            logger.error(f"❌ Error in think_and_tweet: {str(e)}")
    
    def get_time_of_day(self) -> str:
        """
        Determine time of day for context
        """
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def save_state(self):
        """
        Save agent state to JSON file
        """
        state = {
            "stage": self.stage,
            "balance": self.balance,
            "tweet_count": self.tweet_count,
            "last_updated": datetime.now().isoformat()
        }
        
        os.makedirs("data", exist_ok=True)
        with open("data/state.json", "w") as f:
            json.dump(state, f, indent=2)
        
        logger.info("💾 State saved")
    
    def load_state(self):
        """
        Load previous state if exists
        """
        try:
            if os.path.exists("data/state.json"):
                with open("data/state.json", "r") as f:
                    state = json.load(f)
                
                self.stage = state.get("stage", "egg")
                self.balance = state.get("balance", 0.0)
                self.tweet_count = state.get("tweet_count", 0)
                
                logger.info(f"📂 Previous state loaded: {self.stage}, {self.tweet_count} tweets")
        except Exception as e:
            logger.error(f"⚠️ Could not load previous state: {str(e)}")


# Test function
def test_agent():
    """
    Test the agent without running continuous loop
    """
    agent = PolyPuffAgent()
    
    print("\n🧪 Testing single tweet cycle...\n")
    agent.think_and_tweet()
    print("\n✅ Test complete! Check Twitter for the tweet.")


if __name__ == "__main__":
    test_agent()