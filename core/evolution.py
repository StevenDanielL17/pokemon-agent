from config.prompts import STAGE_PROMPTS
from utils.logger import logger

class EvolutionManager:
    """
    Manages agent evolution based on wallet balance
    """
    
    def __init__(self):
        self.stages = ["egg", "slime", "beast"]
        self.thresholds = {
            "egg": 0.0,
            "slime": 0.005,   # ~$15
            "beast": 0.02     # ~$60
        }
        logger.info("Evolution manager initialized")
    
    def check_evolution(self, current_stage: str, balance: float, previous_balance: float = 0.0) -> dict:
        """
        Check if agent should evolve based on balance
        
        Args:
            current_stage: Current evolution stage
            balance: Current wallet balance in ETH
            previous_balance: Previous balance (to detect changes)
        
        Returns:
            dict with:
                - should_evolve: bool
                - new_stage: str (if evolving)
                - evolution_message: str (announcement tweet)
        """
        result = {
            "should_evolve": False,
            "new_stage": current_stage,
            "evolution_message": None,
            "should_devolve": False
        }
        
        # Check for balance DROP (sickness/devolution)
        if previous_balance > 0 and balance < previous_balance * 0.5:
            logger.warning(f"Balance dropped significantly: {previous_balance} -> {balance}")
            result["should_devolve"] = True
            result["evolution_message"] = "oh no... im not feeling good... balance dropping... 😢💀"
            return result
        
        # Check for EVOLUTION (balance increase)
        if balance >= self.thresholds["beast"] and current_stage != "beast":
            logger.info(f"EVOLUTION TRIGGERED: {current_stage} -> BEAST")
            result["should_evolve"] = True
            result["new_stage"] = "beast"
            result["evolution_message"] = "⚡ EVOLUTION COMPLETE ⚡\n\nI AM NOW A BEAST! 🔥\nportfolio loaded | hunting mode activated\nthank u for believing in me 💎"
            
        elif balance >= self.thresholds["slime"] and current_stage == "egg":
            logger.info(f"EVOLUTION TRIGGERED: egg -> SLIME")
            result["should_evolve"] = True
            result["new_stage"] = "slime"
            result["evolution_message"] = "🎉 I HATCHED!! 🎉\n\nim a slime now! 💧\nthank u for feeding me... i wont forget this ✨"
        
        return result
    
    def get_stage_info(self, stage: str) -> dict:
        """
        Get information about an evolution stage
        """
        return STAGE_PROMPTS.get(stage, STAGE_PROMPTS["egg"])
    
    def get_progress_to_next_stage(self, current_stage: str, balance: float) -> dict:
        """
        Calculate progress to next evolution
        
        Returns:
            dict with next_stage, needed_eth, progress_percent
        """
        if current_stage == "beast":
            return {
                "next_stage": None,
                "needed_eth": 0,
                "progress_percent": 100
            }
        
        stage_order = ["egg", "slime", "beast"]
        current_index = stage_order.index(current_stage)
        next_stage = stage_order[current_index + 1]
        next_threshold = self.thresholds[next_stage]
        current_threshold = self.thresholds[current_stage]
        
        progress = ((balance - current_threshold) / (next_threshold - current_threshold)) * 100
        progress = max(0, min(100, progress))  # Clamp between 0-100
        
        needed = next_threshold - balance
        
        return {
            "next_stage": next_stage,
            "needed_eth": needed,
            "progress_percent": round(progress, 1)
        }


# Test function
def test_evolution():
    """
    Test evolution logic with different balances
    """
    print("\nTesting Evolution System...\n")
    
    evo = EvolutionManager()
    
    test_cases = [
        ("egg", 0.0, 0.0),
        ("egg", 0.006, 0.0),    # Should evolve to slime
        ("slime", 0.025, 0.01), # Should evolve to beast
        ("beast", 0.05, 0.05),  # Already max
        ("slime", 0.003, 0.01), # Balance dropped (sick)
    ]
    
    for stage, balance, prev_balance in test_cases:
        result = evo.check_evolution(stage, balance, prev_balance)
        print(f"Stage: {stage:6} | Balance: {balance:.4f} ETH | Previous: {prev_balance:.4f}")
        print(f"  Should evolve: {result['should_evolve']}")
        print(f"  New stage: {result['new_stage']}")
        if result['evolution_message']:
            print(f"  Message: {result['evolution_message'][:50]}...")
        print()
    
    print("Evolution test complete!")


if __name__ == "__main__":
    test_evolution()
