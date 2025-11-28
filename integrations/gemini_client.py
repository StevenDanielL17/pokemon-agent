import google.generativeai as genai
import os
from dotenv import load_dotenv
from config.prompts import STAGE_PROMPTS
from config.settings import settings
from utils.logger import logger
import random

load_dotenv()

class GeminiClient:
    """
    Handles all Google Gemini AI interactions for generating tweets
    """
    
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        # Use gemini-flash-latest as it is explicitly available
        self.model = genai.GenerativeModel('gemini-flash-latest')
        logger.info("Google Gemini client initialized (FREE)")
    
    def generate_tweet(self, stage: str, context: dict) -> str:
        """
        Generate a tweet based on current evolution stage and context
        
        Args:
            stage: Current evolution stage ("egg", "slime", "beast", "sick")
            context: Dictionary with balance, recent_activity, etc.
        
        Returns:
            Generated tweet text
        """
        try:
            # Get personality prompt for current stage
            personality = STAGE_PROMPTS[stage]["personality"]
            
            # Build context string
            context_str = f"""
{personality}

Current Status:
- Balance: {context.get('balance', 0)} ETH
- Stage: {stage}
- Recent activity: {context.get('recent_activity', 'None')}
- Time: {context.get('time_of_day', 'unknown')}

Generate a tweet that:
1. Stays in character
2. Is 50-150 characters (short and punchy)
3. Includes 1-2 relevant emojis
4. Does NOT use hashtags unless specifically about evolution
5. Sounds natural, not robotic

IMPORTANT: Reply with ONLY the tweet text, no quotes, no explanation.
"""
            
            # Call Gemini API
            response = self.model.generate_content(context_str)
            tweet = response.text.strip()
            
            # Remove quotes if AI wrapped the tweet in them
            tweet = tweet.strip('"').strip("'").strip('`')
            
            # Ensure it's not too long
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            logger.info(f"Generated tweet: {tweet}")
            return tweet
            
        except Exception as e:
            logger.error(f"Error generating tweet: {str(e)}")
            # Fallback tweet if AI fails
            fallbacks = {
                "egg": [
                    "still here... still smol...",
                    "waiting to hatch...",
                    "warm and cozy in my shell...",
                    "dreaming of the moon..."
                ],
                "slime": [
                    "just vibing on the blockchain",
                    "fluid like liquidity",
                    "bloop bloop...",
                    "sliding through the mempool"
                ],
                "beast": [
                    "building my empire, one block at a time",
                    "roaring at the charts",
                    "hunting for alpha",
                    "unstoppable force"
                ],
                "sick": [
                    "not feeling good...",
                    "need some medicine...",
                    "system error...",
                    "recovering..."
                ]
            }
            options = fallbacks.get(stage, ["..."])
            return random.choice(options)


# Quick test function
def test_gemini():
    """
    Test Gemini connection and tweet generation
    """
    client = GeminiClient()
    
    test_context = {
        "balance": 0.001,
        "stage": "egg",
        "recent_activity": "No recent transactions",
        "time_of_day": "morning"
    }
    
    print("\nTesting tweet generation for all stages...\n")
    
    for stage in ["egg", "slime", "beast", "sick"]:
        tweet = client.generate_tweet(stage, test_context)
        print(f"{stage.upper():8} | {tweet}\n")


if __name__ == "__main__":
    test_gemini()