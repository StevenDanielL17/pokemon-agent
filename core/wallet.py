from web3 import Web3
from config.settings import settings
from utils.logger import logger
from typing import Optional

class WalletManager:
    """
    Manages blockchain wallet interactions (Base network)
    """
    
    def __init__(self):
        # Connect to Base network
        print(f"Connecting to RPC: {settings.BASE_RPC_URL}")
        self.w3 = Web3(Web3.HTTPProvider(settings.BASE_RPC_URL))
        
        if self.w3.is_connected():
            chain_id = self.w3.eth.chain_id
            print(f"Connected! Chain ID: {chain_id}")
        
        self.address = Web3.to_checksum_address(settings.BASE_WALLET_ADDRESS)
        print(f"Checking address: {self.address}")
        
        # Verify connection
        if self.w3.is_connected():
            logger.info("Connected to Base blockchain")
        else:
            logger.error("Failed to connect to Base blockchain")
            raise ConnectionError("Cannot connect to Base RPC")
        
        # Verify address format
        if not self.w3.is_address(self.address):
            logger.error(f"Invalid wallet address: {self.address}")
            raise ValueError("Invalid wallet address format")
        
        logger.info(f"Wallet initialized: {self.address[:10]}...{self.address[-8:]}")
    
    def get_balance(self) -> float:
        """
        Get current wallet balance in ETH
        
        Returns:
            Balance in ETH (e.g., 0.005)
        """
        try:
            # Get balance in Wei (smallest unit)
            balance_wei = self.w3.eth.get_balance(self.address)
            print(f"Balance in Wei: {balance_wei}")
            
            # Convert Wei to ETH
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            logger.info(f"Current balance: {balance_eth} ETH")
            return float(balance_eth)
            
        except Exception as e:
            logger.error(f"Error reading balance: {str(e)}")
            return 0.0
    
    def get_recent_transactions(self, limit: int = 5) -> list:
        """
        Get recent transactions (simplified version)
        Note: Full transaction history requires external API (Basescan)
        
        Returns:
            List of transaction info (for now, just checks if balance changed)
        """
        try:
            current_block = self.w3.eth.block_number
            logger.info(f"Current block: {current_block}")
            
            # For hackathon: we'll just track balance changes
            # Full implementation would use Basescan API
            return []
            
        except Exception as e:
            logger.error(f"Error getting transactions: {str(e)}")
            return []
    
    def get_shortened_address(self) -> str:
        """
        Get shortened wallet address for tweets
        
        Returns:
            Format: 0x742d...95f0
        """
        if not self.address:
            return "No wallet"
        return f"{self.address[:6]}...{self.address[-4:]}"


# Test function
def test_wallet():
    """
    Test wallet connection and balance reading
    """
    print("\nTesting Wallet Connection...\n")
    
    try:
        wallet = WalletManager()
        print(f"Wallet Address: {wallet.address}")
        print(f"Shortened: {wallet.get_shortened_address()}")
        
        balance = wallet.get_balance()
        print(f"\nCurrent Balance: {balance} ETH")
        
        if balance == 0:
            print("\nWallet is empty (this is normal for a new wallet)")
            print("To test evolution, send some Base ETH to:")
            print(f"  {wallet.address}")
        else:
            print(f"\nWallet has funds! Ready to test evolution.")
        
        print("\nWallet test PASSED!")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nCheck your .env file:")
        print("  - BASE_WALLET_ADDRESS should be a valid Ethereum address")
        print("  - BASE_RPC_URL should be https://mainnet.base.org")


if __name__ == "__main__":
    test_wallet()
