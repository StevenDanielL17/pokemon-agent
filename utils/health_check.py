"""
Health check to ensure bot is running properly
"""
from datetime import datetime, timedelta
import json
import os
from utils.logger import logger

def check_agent_health() -> dict:
    """
    Check if agent is healthy
    
    Returns:
        dict with status info
    """
    health = {
        "status": "healthy",
        "issues": [],
        "last_tweet": None,
        "tweet_count": 0
    }
    
    # Check if state file exists
    if not os.path.exists("data/state.json"):
        health["issues"].append("No state file found")
        health["status"] = "unhealthy"
        return health
    
    # Load state
    try:
        with open("data/state.json", "r") as f:
            state = json.load(f)
        
        health["tweet_count"] = state.get("tweet_count", 0)
        last_updated = state.get("last_updated")
        
        if last_updated:
            last_update_time = datetime.fromisoformat(last_updated)
            time_since_update = datetime.now() - last_update_time
            
            # If no update in 2 hours, something is wrong
            if time_since_update > timedelta(hours=2):
                health["issues"].append(f"No activity for {time_since_update.seconds // 3600} hours")
                health["status"] = "warning"
            
            health["last_tweet"] = last_updated
        
    except Exception as e:
        health["issues"].append(f"Error reading state: {str(e)}")
        health["status"] = "unhealthy"
    
    return health


if __name__ == "__main__":
    health = check_agent_health()
    print(f"\nAgent Health Check:")
    print(f"Status: {health['status']}")
    print(f"Tweet Count: {health['tweet_count']}")
    print(f"Last Tweet: {health['last_tweet']}")
    if health['issues']:
        print(f"Issues: {', '.join(health['issues'])}")
