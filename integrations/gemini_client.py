import google.generativeai as genai
import os
import random
from dotenv import load_dotenv
from config.prompts import STAGE_PROMPTS, FALLBACK_TWEETS
from config.settings import settings
from utils.logger import logger

load_dotenv()

class GeminiClient:
    """
    Handles interactions with Google's Gemini API
    """
    
    def __init__(self):
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.tweet_history = []
            self.last_tweet_type = None
            logger.info("Gemini client initialized")
        except Exception as e:
            logger.error(f"Error initializing Gemini: {e}")
            self.model = None

    def generate_tweet(self, stage: str, context: dict) -> str:
        """
        Generate a tweet based on stage and context
        
        Args:
            stage: Current evolution stage
            context: Dictionary with balance, recent_activity, etc.
        
        Returns:
            Generated tweet text
        """
        try:
            # Get personality prompt for current stage
            personality = STAGE_PROMPTS[stage]["personality"]
            
            # Build enhanced context
            balance = context.get('balance', 0)
            recent_activity = context.get('recent_activity', 'None')
            time_of_day = context.get('time_of_day', 'unknown')
            tweet_count = context.get('tweet_count', 0)
            
            # Add variety instructions
            variety_note = ""
            if self.last_tweet_type:
                variety_note = f"\n\nIMPORTANT: Your last tweet was about {self.last_tweet_type}. DO NOT repeat the same type. Pick a different style from the TWEET VARIETY section!"
            
            # Build context string
            context_str = f"""
{personality}

Current Status:
- Balance: {balance:.4f} ETH
- Stage: {stage}
- Recent activity: {recent_activity}
- Time: {time_of_day}
- Tweet #{tweet_count}
{variety_note}

Generate ONE short tweet (50-200 characters) that:
1. Matches the personality
2. Includes 1-2 emojis
3. Feels natural and spontaneous
4. Is DIFFERENT from recent tweets
5. Does NOT use hashtags

IMPORTANT: Reply with ONLY the tweet text, nothing else. No quotes, no explanation.
"""
            
            # Call Gemini API
            response = self.model.generate_content(
                context_str,
                generation_config={
                    'temperature': 1.0,  # Max creativity
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 100,
                }
            )
            
            tweet = response.text.strip()
            
            # Clean up
            tweet = tweet.strip('"').strip("'").strip('`').strip()
            
            # Remove "Tweet:" prefix if AI added it
            if tweet.lower().startswith('tweet:'):
                tweet = tweet[6:].strip()
            
            # Ensure it's not too long
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            # Track variety
            self._track_tweet_type(tweet)
            
            # Save to history
            self.tweet_history.append(tweet)
            if len(self.tweet_history) > 10:
                self.tweet_history.pop(0)  # Keep last 10
            
            logger.info(f"Generated tweet: {tweet}")
            return tweet
            
        except Exception as e:
            logger.error(f"Error generating tweet: {str(e)}")
            raise # Re-raise for retry logic
    
    def _track_tweet_type(self, tweet: str):
        """
        Identify tweet type for variety tracking
        """
        tweet_lower = tweet.lower()
        
        if any(word in tweet_lower for word in ['?', 'anyone', 'can u', 'can you']):
            self.last_tweet_type = "question"
        elif any(word in tweet_lower for word in ['thank', 'grateful', 'appreciate']):
            self.last_tweet_type = "gratitude"
        elif any(word in tweet_lower for word in ['need', 'help', 'feed', 'hungry']):
            self.last_tweet_type = "begging"
        elif any(word in tweet_lower for word in ['balance', 'eth', 'wallet']):
            self.last_tweet_type = "status"
        elif any(word in tweet_lower for word in ['hunting', 'searching', 'looking']):
            self.last_tweet_type = "hunting"
        else:
            self.last_tweet_type = "general"
    
    def _get_fallback_tweet(self, stage: str) -> str:
        """
        Get a random fallback tweet if AI fails
        """
        fallbacks = FALLBACK_TWEETS.get(stage, FALLBACK_TWEETS["egg"])
        tweet = random.choice(fallbacks)
        logger.info(f"Using fallback tweet: {tweet}")
        return tweet
    
    def generate_evolution_announcement(self, from_stage: str, to_stage: str) -> str:
        """
        Generate special evolution announcement tweet
        """
        from config.prompts import EVOLUTION_ANNOUNCEMENTS
        
        key = f"{from_stage}_to_{to_stage}"
        
        if key in EVOLUTION_ANNOUNCEMENTS:
            announcements = EVOLUTION_ANNOUNCEMENTS[key]
            tweet = random.choice(announcements)
            logger.info(f"Evolution announcement: {from_stage} -> {to_stage}")
            return tweet
        
        # Fallback generic announcement
        return f"⚡ EVOLUTION ⚡\n\n{from_stage} → {to_stage}\n\nthank u for believing in me! 🔥✨"


# Quick test function
def test_gemini():
    """
    Test Gemini connection and tweet generation with variety
    """
    client = GeminiClient()
    
    test_context = {
        "balance": 0.001,
        "recent_activity": "No transactions",
        "time_of_day": "morning",
        "tweet_count": 1
    }
    
    print("\nTesting tweet generation with variety...\n")
    
    # Generate 5 tweets for same stage to test variety
    for i in range(5):
        try:
            tweet = client.generate_tweet("egg", test_context)
            print(f"Tweet {i+1}: {tweet}\n")
            test_context["tweet_count"] += 1
        except Exception as e:
            print(f"Tweet generation failed: {e}")
            # Fallback
            print(f"Fallback: {client._get_fallback_tweet('egg')}\n")
    
    # Test evolution announcement
    print("Testing evolution announcement:\n")
    evo = client.generate_evolution_announcement("egg", "slime")
    print(f"{evo}\n")


if __name__ == "__main__":
    test_gemini()