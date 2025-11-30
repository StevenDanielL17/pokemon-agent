import time
from datetime import datetime
from integrations.twitter import TwitterClient
from integrations.gemini_client import GeminiClient
from core.wallet import WalletManager
from core.evolution import EvolutionManager
from integrations.interaction_handler import InteractionHandler
from config.prompts import STAGE_PROMPTS
from config.settings import settings
from utils.logger import logger
from utils.helpers import get_progress_bar, format_eth, get_emoji_for_stage
import json
import os
import random

class PolyPuffAgent:
    """
    Main agent logic - the brain of PolyPuff
    Now with blockchain integration and evolution!
    """
    
    def __init__(self):
        # Initialize clients
        self.twitter = TwitterClient()
        self.ai = GeminiClient()
        
        # Initialize blockchain components
        try:
            self.wallet = WalletManager()
            self.evolution = EvolutionManager()
            self.blockchain_enabled = True
            logger.info("Blockchain features ENABLED")
        except Exception as e:
            logger.warning(f"Blockchain disabled: {str(e)}")
            self.wallet = None
            self.evolution = None
            self.blockchain_enabled = False
        
        # Agent state
        self.stage = "egg"
        self.balance = 0.0
        self.previous_balance = 0.0
        self.tweet_count = 0
        self.last_balance_check = None
        
        # Load previous state if exists
        self.load_state()
        
        # Initialize interaction handler
        if self.blockchain_enabled:
            self.interaction_handler = InteractionHandler(
                self.twitter, 
                self.ai, 
                self.stage, 
                self.balance
            )
            logger.info("Interaction handler enabled")
        else:
            self.interaction_handler = None
        
        logger.info(f"PolyPuff initialized! Stage: {self.stage}, Balance: {self.balance} ETH")
    def check_wallet_and_evolve(self):
        """
        Check wallet balance and handle evolution
        Should be called before each tweet
        """
        if not self.blockchain_enabled:
            logger.info("Blockchain disabled - skipping wallet check")
            return
        
        try:
            # Get current balance
            self.previous_balance = self.balance
            self.balance = self.wallet.get_balance()
            self.last_balance_check = datetime.now().isoformat()
            
            # If balance increased, thank the donor
            if self.balance > self.previous_balance:
                increase = self.balance - self.previous_balance
                logger.info(f"Donation received: {increase:.4f} ETH")
                
                if self.interaction_handler:
                    self.interaction_handler.handle_donation_thanks(
                        "anonymous donor",
                        increase
                    )
            
            # Check for evolution
            evolution_result = self.evolution.check_evolution(
                self.stage, 
                self.balance, 
                self.previous_balance
            )
            
            # Handle evolution
            if evolution_result["should_evolve"]:
                old_stage = self.stage
                self.stage = evolution_result["new_stage"]
                
                logger.info(f"EVOLUTION: {old_stage} -> {self.stage}")
                
                # Post evolution announcement
                evolution_tweet = evolution_result["evolution_message"]
                self.twitter.post_tweet(evolution_tweet)
                
                # Update profile picture if image exists
                image_path = STAGE_PROMPTS[self.stage].get("image")
                if image_path and os.path.exists(image_path):
                    self.twitter.update_profile_image(image_path)
                    logger.info(f"Profile picture updated to {self.stage}")
                
                # Save new state
                self.save_state()
                
                # Wait a bit before regular tweet
                time.sleep(30)
            
            # Handle devolution (sickness)
            elif evolution_result["should_devolve"]:
                logger.warning("Agent is sick due to balance drop")
                sick_tweet = evolution_result["evolution_message"]
                self.twitter.post_tweet(sick_tweet)
                time.sleep(30)
                
        except Exception as e:
            logger.error(f"Error in wallet check: {str(e)}")

    def check_interactions(self):
        """
        Check for and respond to social interactions
        """
        if not self.interaction_handler:
            return
        
        try:
            # Update handler with current state
            self.interaction_handler.current_stage = self.stage
            self.interaction_handler.balance = self.balance
            
            # Process mentions
            self.interaction_handler.check_and_respond_to_mentions()
            
        except Exception as e:
            logger.error(f"Error checking interactions: {e}")

    def should_post_progress_update(self) -> bool:
        """
        Decide if this tweet should be a progress update
        Returns True 20% of the time if not yet beast
        """
        if self.stage == "beast":
            return False
        return random.random() < 0.2  # 20% chance

    def generate_progress_tweet(self) -> str:
        """
        Generate a progress update tweet showing evolution progress
        """
        if self.stage == "beast":
            return None
        
        # Get next evolution info
        progress_info = self.evolution.get_progress_to_next_stage(self.stage, self.balance)
        
        next_stage = progress_info["next_stage"]
        needed = progress_info["needed_eth"]
        progress_pct = progress_info["progress_percent"]
        
        # Create progress bar
        progress_bar = get_progress_bar(self.balance, self.evolution.thresholds[next_stage])
        
        # Format tweet
        current_emoji = get_emoji_for_stage(self.stage)
        next_emoji = get_emoji_for_stage(next_stage)
        
        tweet = f"{current_emoji} → {next_emoji} evolution progress:\n\n"
        tweet += f"{progress_bar}\n\n"
        tweet += f"balance: {format_eth(self.balance)}\n"
        tweet += f"need: {format_eth(needed)} more\n\n"
        tweet += f"feed me: {self.wallet.get_shortened_address()}"
        
        return tweet
    
    def think_and_tweet(self):
        """
        Main action loop - now with progress updates!
        """
        logger.info("PolyPuff is thinking...")
        
        try:
            # FIRST: Check wallet and handle evolution
            self.check_wallet_and_evolve()
            
            # Decide tweet type
            if self.should_post_progress_update():
                # Post progress update
                tweet_text = self.generate_progress_tweet()
                image_path = None
                logger.info("Posting progress update")
            else:
                # Normal AI-generated tweet
                context = {
                    "balance": self.balance,
                    "stage": self.stage,
                    "recent_activity": self.get_recent_activity(),
                    "time_of_day": self.get_time_of_day(),
                    "tweet_count": self.tweet_count,
                    "wallet_address": self.wallet.get_shortened_address() if self.wallet else None
                }
                
                tweet_text = self.ai.generate_tweet(self.stage, context)
                
                # Add wallet address occasionally (30% chance if not beast)
                if self.wallet and self.balance < self.evolution.thresholds.get("beast", 0.02):
                    if random.random() < 0.3:
                        tweet_text += f"\n\nfeed me: {self.wallet.get_shortened_address()}"
                
                image_path = STAGE_PROMPTS[self.stage].get("image")
                if image_path and not os.path.exists(image_path):
                    image_path = None
            
            # Post to Twitter
            success = self.twitter.post_tweet(tweet_text, image_path)
            
            if success:
                self.tweet_count += 1
                self.save_state()
                logger.info(f"Tweet #{self.tweet_count} posted!")
            
        except Exception as e:
            logger.error(f"Error in think_and_tweet: {str(e)}")
    
    def get_recent_activity(self) -> str:
        """
        Get summary of recent wallet activity
        """
        if not self.blockchain_enabled:
            return "Blockchain features disabled"
        
        if self.balance > self.previous_balance:
            increase = self.balance - self.previous_balance
            return f"Received {increase:.4f} ETH!"
        elif self.balance < self.previous_balance:
            decrease = self.previous_balance - self.balance
            return f"Balance decreased by {decrease:.4f} ETH"
        else:
            return "No recent transactions"
    
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
            "previous_balance": self.previous_balance,
            "tweet_count": self.tweet_count,
            "last_balance_check": self.last_balance_check,
            "last_updated": datetime.now().isoformat()
        }
        
        os.makedirs("data", exist_ok=True)
        with open("data/state.json", "w") as f:
            json.dump(state, f, indent=2)
        
        logger.info("State saved")
    
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
                self.previous_balance = state.get("previous_balance", 0.0)
                self.tweet_count = state.get("tweet_count", 0)
                self.last_balance_check = state.get("last_balance_check")
                
                logger.info(f"Previous state loaded: {self.stage}, {self.tweet_count} tweets, {self.balance} ETH")
        except Exception as e:
            logger.error(f"Could not load previous state: {str(e)}")


# Test function
def test_agent():
    """
    Test the agent without running continuous loop
    """
    agent = PolyPuffAgent()
    
    print("\nTesting single tweet cycle with blockchain...\n")
    agent.think_and_tweet()
    print("\nTest complete! Check Twitter and logs.")


if __name__ == "__main__":
    test_agent()