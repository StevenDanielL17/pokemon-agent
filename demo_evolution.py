import time
import os
from core.agent import PolyPuffAgent
from config.prompts import STAGE_PROMPTS
from utils.logger import logger

def run_demo():
    print("🎬 Starting Evolution Demo...")
    print("This will post 4 tweets (one for each stage) with images.")
    
    agent = PolyPuffAgent()
    
    # Define the demo sequence
    stages = ["egg", "slime", "beast", "sick"]
    
    for stage in stages:
        print(f"\n📸 Demoing Stage: {stage.upper()}")
        
        # Force stage
        agent.stage = stage
        
        # Get image path
        image_path = STAGE_PROMPTS[stage].get("image")
        if not os.path.exists(image_path):
            print(f"⚠️ Image not found for {stage}: {image_path}")
            continue
            
        # Generate a demo tweet
        # We'll use a hardcoded message to clearly indicate it's a demo/test
        # or we could ask AI. Let's ask AI to make it feel dynamic.
        context = {
            "balance": 999.0 if stage == "beast" else 0.0,
            "stage": stage,
            "recent_activity": "Demo Mode",
            "time_of_day": "day",
            "tweet_count": 0,
            "wallet_address": "0xDemo..."
        }
        
        try:
            tweet_text = agent.ai.generate_tweet(stage, context)
            tweet_text += f"\n\n(Demo: {stage} stage check ✅)"
            
            print(f"Tweeting: {tweet_text}")
            print(f"Image: {image_path}")
            
            # Post tweet
            agent.twitter.post_tweet(tweet_text, image_path)
            print("✅ Posted!")
            
            # Update profile pic to match
            agent.twitter.update_profile_image(image_path)
            print("✅ Profile Pic Updated!")
            
            # Wait a bit to avoid rate limits
            print("Waiting 10 seconds...")
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Error in {stage} demo: {e}")

    print("\n🔄 Restoring Normal State...")
    # Force a wallet check to sync back to reality
    agent.check_wallet_and_evolve()
    print(f"Restored to: {agent.stage} (Balance: {agent.balance} ETH)")
    
    print("\n✨ Demo Complete!")

if __name__ == "__main__":
    run_demo()
