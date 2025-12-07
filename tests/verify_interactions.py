
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.getcwd())

from integrations.interaction_handler import InteractionHandler

def verify_interactions():
    print("🧪 Verifying Interaction Handler...")
    
    # Mock dependencies
    mock_twitter = MagicMock()
    mock_ai = MagicMock()
    
    # Setup mock mentions
    mock_mention = MagicMock()
    mock_mention.id = "12345"
    mock_mention.text = "Hey PolyPuff, how are you?"
    mock_mention.author_id = "user123"
    
    mock_twitter.get_recent_mentions.return_value = [mock_mention]
    mock_twitter.reply_to_tweet.return_value = True
    
    mock_ai.model.generate_content.return_value.text = '"I am doing great! 🥚"'
    
    # Initialize handler
    handler = InteractionHandler(mock_twitter, mock_ai, "egg", 0.0)
    
    # Clear processed tweets for test
    handler.processed_tweets = set()
    
    # Run check
    print("Checking mentions...")
    handler.check_and_respond_to_mentions()
    
    # Verify
    mock_twitter.get_recent_mentions.assert_called_once()
    print("✅ Fetched mentions")
    
    mock_ai.model.generate_content.assert_called_once()
    print("✅ Generated reply")
    
    mock_twitter.reply_to_tweet.assert_called_with("12345", "I am doing great! 🥚")
    print("✅ Replied to tweet")
    
    print("✨ Interaction Verification Complete!")

if __name__ == "__main__":
    verify_interactions()
