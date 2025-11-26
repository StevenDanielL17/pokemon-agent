import unittest
from core.wallet import Wallet

class TestWallet(unittest.TestCase):
    def test_balance(self):
        wallet = Wallet()
        self.assertEqual(wallet.get_balance(), 0)

if __name__ == '__main__':
    unittest.main()
