#!/usr/bin/env python3
"""
PolyPuff Agent - Main Entry Point
Runs the agent continuously, tweeting every hour
"""

import os
import sys

# Fix Windows console encoding BEFORE any other imports
if os.name == 'nt':  # Windows only
    try:
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass  # If reconfigure fails, continue anyway

import time
import schedule
import signal
from core.agent import PolyPuffAgent
from utils.logger import logger
from config.settings import settings


def signal_handler(sig, frame):
    """
    Handle Ctrl+C gracefully
    """
    logger.info("\nShutdown signal received...")
    logger.info("Saving state...")
    
    # Save any pending state here
    # (agent already saves on each tweet, so this is just for safety)
    
    logger.info("PolyPuff is going to sleep. Goodnight!")
    sys.exit(0)

def main():
    """
    Main execution loop
    """
    # ASCII art banner (no emojis to avoid encoding issues)
    print("""
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║          POLYPUFF AGENT               ║
    ║       The Evolving RWA Hunter         ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
    """)
    
    logger.info("Starting PolyPuff Agent...")
    
    # Check environment variables
    required_vars = [
        ("GOOGLE_API_KEY", settings.GOOGLE_API_KEY),
        ("TWITTER_API_KEY", settings.TWITTER_API_KEY),
        ("TWITTER_API_SECRET", settings.TWITTER_API_SECRET),
        ("TWITTER_ACCESS_TOKEN", settings.TWITTER_ACCESS_TOKEN),
        ("TWITTER_ACCESS_SECRET", settings.TWITTER_ACCESS_SECRET)
    ]
    
#!/usr/bin/env python3
"""
PolyPuff Agent - Main Entry Point
Runs the agent continuously, tweeting every hour
"""

import os
import sys

# Fix Windows console encoding BEFORE any other imports
if os.name == 'nt':  # Windows only
    try:
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass  # If reconfigure fails, continue anyway

import time
import schedule
import signal
from core.agent import PolyPuffAgent
from utils.logger import logger
from config.settings import settings


def signal_handler(sig, frame):
    """
    Handle Ctrl+C gracefully
    """
    logger.info("\nShutdown signal received...")
    logger.info("Saving state...")
    
    # Save any pending state here
    # (agent already saves on each tweet, so this is just for safety)
    
    logger.info("PolyPuff is going to sleep. Goodnight!")
    sys.exit(0)

def main():
    """
    Main execution loop
    """
    # ASCII art banner (no emojis to avoid encoding issues)
    print("""
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║          POLYPUFF AGENT               ║
    ║       The Evolving RWA Hunter         ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
    """)
    
    logger.info("Starting PolyPuff Agent...")
    
    # Check environment variables
    required_vars = [
        ("GOOGLE_API_KEY", settings.GOOGLE_API_KEY),
        ("TWITTER_API_KEY", settings.TWITTER_API_KEY),
        ("TWITTER_API_SECRET", settings.TWITTER_API_SECRET),
        ("TWITTER_ACCESS_TOKEN", settings.TWITTER_ACCESS_TOKEN),
        ("TWITTER_ACCESS_SECRET", settings.TWITTER_ACCESS_SECRET)
    ]
    
    missing = [var[0] for var in required_vars if not var[1]]
    if missing:
        logger.error(f"Missing environment variables: {', '.join(missing)}")
        logger.error("Please check your .env file")
        return
    
    if settings.DEV_MODE:
        logger.info("Running in DEV MODE - tweets will not be posted to Twitter")
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize agent
    agent = PolyPuffAgent()
    
    # Tweet immediately on startup
    logger.info("Posting initial tweet...")
    agent.think_and_tweet()
    
    # Schedule tweets every hour
    interval = settings.TWEET_INTERVAL_MINUTES
    schedule.every(interval).minutes.do(agent.think_and_tweet)
    
    # Schedule interaction checks (every 5 minutes)
    schedule.every(5).minutes.do(agent.check_interactions)
    
    logger.info("Agent is now running!")
    logger.info(f"Will tweet every {interval} minutes")
    logger.info("Checking interactions every 5 minutes")
    logger.info("Press Ctrl+C to stop")
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        # This block might not be reached if signal_handler catches it first,
        # but it's good as a fallback
        logger.info("\nPolyPuff is going to sleep...")
        logger.info("State saved. Run again to resume!")


if __name__ == "__main__":
    main()