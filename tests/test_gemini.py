"""
Quick test to verify Gemini AI connection
"""

from integrations.gemini_client import GeminiClient

def test_gemini():
    print("\n🧪 Testing Google Gemini API...\n")
    
    client = GeminiClient()
    
    test_context = {
        "balance": 0.001,
        "recent_activity": "No transactions",
        "time_of_day": "morning"
    }
    
    print("Generating test tweets for all stages:\n")
    
    for stage in ["egg", "slime", "beast", "sick"]:
        print(f"Testing {stage.upper()}...")
        tweet = client.generate_tweet(stage, test_context)
        print(f"  Result: {tweet}\n")
    
    print("✅ All stages tested successfully!")


if __name__ == "__main__":
    test_gemini()