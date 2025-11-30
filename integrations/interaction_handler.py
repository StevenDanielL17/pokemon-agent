import time
from datetime import datetime, timedelta
from integrations.twitter import TwitterClient
from integrations.gemini_client import GeminiClient
from config.prompts import STAGE_PROMPTS
from utils.logger import logger
import json
import os

class InteractionHandler:
    """
    Handles all social interactions - mentions, replies, DMs
    Makes PolyPuff feel truly alive and responsive
    """
    
    def __init__(self, twitter_client, ai_client, current_stage, balance):
        self.twitter = twitter_client
        self.ai = ai_client
        self.current_stage = current_stage
        self.balance = balance
        
        # Track processed interactions to avoid duplicates
        self.processed_tweets = self.load_processed_tweets()
        self.last_check = None
        
        logger.info("Interaction handler initialized")
    
    def load_processed_tweets(self):
        """Load list of tweet IDs we've already replied to"""
        try:
            if os.path.exists("data/processed_tweets.json"):
                with open("data/processed_tweets.json", "r") as f:
                    data = json.load(f)
                    return set(data.get("tweet_ids", []))
        except:
            pass
        return set()
    
    def save_processed_tweets(self):
        """Save processed tweet IDs"""
        os.makedirs("data", exist_ok=True)
        with open("data/processed_tweets.json", "w") as f:
            json.dump({
                "tweet_ids": list(self.processed_tweets),
                "last_updated": datetime.now().isoformat()
            }, f)
    
    def check_and_respond_to_mentions(self):
        """
        Main function - checks mentions and replies appropriately
        """
        logger.info("Checking for new mentions...")
        
        try:
            mentions = self.twitter.get_recent_mentions()
            
            if not mentions:
                logger.info("No new mentions found")
                return
            
            new_mentions = [m for m in mentions if m.id not in self.processed_tweets]
            
            if not new_mentions:
                logger.info("No unprocessed mentions")
                return
            
            logger.info(f"Found {len(new_mentions)} new mentions to process")
            
            for mention in new_mentions[:5]:  # Process max 5 at a time
                self.handle_mention(mention)
                time.sleep(2)  # Rate limiting
            
        except Exception as e:
            logger.error(f"Error checking mentions: {e}")
    
    def handle_mention(self, mention):
        """
        Process a single mention and generate appropriate reply
        """
        try:
            tweet_text = mention.text.lower()
            author = mention.author_id
            tweet_id = mention.id
            
            logger.info(f"Processing mention from {author}: {tweet_text[:50]}...")
            
            # Determine interaction type
            interaction_type = self.classify_interaction(tweet_text)
            
            # Generate contextual reply
            reply = self.generate_reply(tweet_text, interaction_type, mention)
            
            # Post reply
            success = self.twitter.reply_to_tweet(tweet_id, reply)
            
            if success:
                self.processed_tweets.add(tweet_id)
                self.save_processed_tweets()
                logger.info(f"Replied to mention: {reply[:50]}...")
        
        except Exception as e:
            logger.error(f"Error handling mention: {e}")
    
    def classify_interaction(self, text):
        """
        Classify what type of interaction this is
        """
        text = text.lower()
        
        # Check for different interaction types
        if any(word in text for word in ['feed', 'sent', 'donate', 'donation', 'eth', 'money']):
            return "donation_related"
        
        elif any(word in text for word in ['how are you', 'how r u', 'whats up', "what's up", 'hello', 'hi', 'hey']):
            return "greeting"
        
        elif any(word in text for word in ['what', 'how', 'why', 'when', 'where', '?']):
            return "question"
        
        elif any(word in text for word in ['love', 'cute', 'adorable', 'cool', 'awesome', 'amazing']):
            return "compliment"
        
        elif any(word in text for word in ['help', 'support', 'assist', 'explain']):
            return "help_request"
        
        elif any(word in text for word in ['evolve', 'evolution', 'hatch', 'grow', 'level up']):
            return "evolution_inquiry"
        
        else:
            return "general"
    
    def generate_reply(self, original_text, interaction_type, mention):
        """
        Generate AI reply based on interaction type
        """
        personality = STAGE_PROMPTS[self.current_stage]["personality"]
        
        # Build context for different interaction types
        if interaction_type == "donation_related":
            context = f"""
{personality}

Someone is talking about donating or feeding you!
Their message: "{original_text}"

Generate a GRATEFUL and EXCITED reply (max 200 characters):
- Thank them warmly
- Show personality for your current stage ({self.current_stage})
- Mention how this helps you grow
- Be genuine and emotional
- Include 1-2 emojis

Reply ONLY with the tweet text, nothing else.
"""
        
        elif interaction_type == "greeting":
            context = f"""
{personality}

Someone is greeting you!
Their message: "{original_text}"

Generate a FRIENDLY greeting reply (max 150 characters):
- Greet them back
- Show your current mood/stage ({self.current_stage})
- Be warm and welcoming
- Maybe mention what you're up to
- Include 1-2 emojis

Reply ONLY with the tweet text, nothing else.
"""
        
        elif interaction_type == "question":
            context = f"""
{personality}

Someone asked you a question!
Their message: "{original_text}"

Generate a HELPFUL reply (max 200 characters):
- Try to answer their question in character
- Stay true to your stage personality ({self.current_stage})
- Be informative but cute
- Include 1-2 emojis

Reply ONLY with the tweet text, nothing else.
"""
        
        elif interaction_type == "compliment":
            context = f"""
{personality}

Someone complimented you!
Their message: "{original_text}"

Generate a SHY/GRATEFUL reply (max 150 characters):
- Thank them sweetly
- Show a bit of shyness or humility
- Stay in character for {self.current_stage}
- Include 1-2 emojis

Reply ONLY with the tweet text, nothing else.
"""
        
        elif interaction_type == "evolution_inquiry":
            context = f"""
{personality}

Someone is asking about your evolution!
Their message: "{original_text}"

Current status:
- Stage: {self.current_stage}
- Balance: {self.balance:.4f} ETH

Generate an INFORMATIVE reply (max 200 characters):
- Share your current stage
- Mention what you need to evolve (if not max)
- Be excited about growth
- Include 1-2 emojis

Reply ONLY with the tweet text, nothing else.
"""
        
        else:  # general
            context = f"""
{personality}

Someone mentioned you!
Their message: "{original_text}"

Generate a NATURAL conversational reply (max 200 characters):
- Respond appropriately to their message
- Stay in character ({self.current_stage})
- Be engaging and friendly
- Include 1-2 emojis

Reply ONLY with the tweet text, nothing else.
"""
        
        try:
            response = self.ai.model.generate_content(
                context,
                generation_config={
                    'temperature': 0.9,
                    'max_output_tokens': 80,
                }
            )
            
            reply = response.text.strip().strip('"').strip("'")
            
            # Ensure not too long
            if len(reply) > 280:
                reply = reply[:277] + "..."
            
            return reply
            
        except Exception as e:
            logger.error(f"Error generating reply: {e}")
            # Fallback replies
            fallbacks = {
                "egg": "🥚 thank u for noticing me!",
                "slime": "💧 hey! thanks for reaching out ✨",
                "beast": "🔥 appreciate you! lets connect",
                "sick": "😢 thanks for checking on me..."
            }
            return fallbacks.get(self.current_stage, "✨ hi there!")
    
    def handle_donation_thanks(self, donor_address, amount):
        """
        Special thank you tweet when someone sends ETH
        Called by agent when balance increases
        """
        personality = STAGE_PROMPTS[self.current_stage]["personality"]
        
        context = f"""
{personality}

Someone just sent you {amount:.4f} ETH!
Donor address: {donor_address[:10]}...

Generate an EXTREMELY GRATEFUL tweet (max 250 characters):
- Thank them profusely
- Show genuine emotion
- Mention the specific amount
- Express how this helps you grow
- Be personal and heartfelt
- Include 2-3 emojis

This is a PUBLIC tweet, not a reply.

Reply ONLY with the tweet text, nothing else.
"""
        
        try:
            response = self.ai.model.generate_content(
                context,
                generation_config={'temperature': 1.0, 'max_output_tokens': 100}
            )
            
            thank_you = response.text.strip().strip('"').strip("'")
            
            # Post public thank you
            self.twitter.post_tweet(thank_you)
            logger.info(f"Posted thank you tweet for donation of {amount} ETH")
            
        except Exception as e:
            logger.error(f"Error posting thank you: {e}")


def test_interaction_handler():
    """
    Test interaction handling
    """
    from integrations.twitter import TwitterClient
    from integrations.gemini_client import GeminiClient
    
    print("\nTesting Interaction Handler...\n")
    
    twitter = TwitterClient()
    ai = GeminiClient()
    
    handler = InteractionHandler(twitter, ai, "slime", 0.003)
    
    # Simulate checking mentions
    print("Checking for mentions...")
    handler.check_and_respond_to_mentions()
    
    print("\nTest complete!")


if __name__ == "__main__":
    test_interaction_handler()
