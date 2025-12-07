import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.getcwd())

from core.agent import PolyPuffAgent
from config.settings import settings

def verify_logic():
    print("🧪 Starting Logic Verification...")
    
    # Mock dependencies
    with patch('core.agent.TwitterClient') as MockTwitter, \
         patch('core.agent.GeminiClient') as MockGemini, \
         patch('core.agent.WalletManager') as MockWallet, \
         patch('core.agent.EvolutionManager') as MockEvolution:
        
        # Setup mocks
        mock_twitter = MockTwitter.return_value
        mock_twitter.post_tweet.return_value = True
        
        mock_gemini = MockGemini.return_value
        mock_gemini.generate_tweet.return_value = "Test tweet content"
        
        mock_wallet = MockWallet.return_value
        mock_wallet.get_balance.return_value = 0.0
        
        mock_evolution = MockEvolution.return_value
        mock_evolution.check_evolution.return_value = {
            "should_evolve": False,
            "new_stage": "egg",
            "evolution_message": None,
            "should_devolve": False
        }
        mock_evolution.thresholds = {"beast": 0.02}
        
        # Initialize agent
        print("Initializing Agent...")
        agent = PolyPuffAgent()
        
        # Test think_and_tweet
        print("Testing think_and_tweet()...")
        agent.think_and_tweet()
        
        # Verify tweet was generated
        mock_gemini.generate_tweet.assert_called_once()
        print("✅ Tweet generated")
        
        # Verify tweet was posted
        mock_twitter.post_tweet.assert_called_once()
        print("✅ Tweet posted (mocked)")
        
        print("\n✨ Logic Verification Complete!")

if __name__ == "__main__":
    verify_logic()
