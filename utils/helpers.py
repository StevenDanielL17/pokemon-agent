"""
Helper functions for formatting and display
"""

def get_progress_bar(current: float, target: float, length: int = 10) -> str:
    """
    Generate a text progress bar
    
    Args:
        current: Current value
        target: Target value
        length: Number of characters in bar
    
    Returns:
        Progress bar string like: ▓▓▓▓▓░░░░░ 50%
    """
    if target == 0:
        return "░" * length + " 0%"
    
    percentage = min(100, (current / target) * 100)
    filled = int((percentage / 100) * length)
    empty = length - filled
    
    bar = "▓" * filled + "░" * empty
    return f"{bar} {percentage:.0f}%"


def format_eth(amount: float) -> str:
    """
    Format ETH amount for display
    
    Args:
        amount: ETH amount
    
    Returns:
        Formatted string like "0.0050 ETH"
    """
    return f"{amount:.4f} ETH"


def get_emoji_for_stage(stage: str) -> str:
    """
    Get emoji representation for stage
    """
    emojis = {
        "egg": "🥚",
        "slime": "💧",
        "beast": "🔥",
        "sick": "😢"
    }
    return emojis.get(stage, "❓")


def shorten_address(address: str) -> str:
    """
    Shorten wallet address for display
    
    Args:
        address: Full wallet address
    
    Returns:
        Shortened format: 0x742d...95f0
    """
    if not address or len(address) < 10:
        return address
    return f"{address[:6]}...{address[-4:]}"
