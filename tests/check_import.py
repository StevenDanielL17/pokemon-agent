
import sys
import os
sys.path.append(os.getcwd())
try:
    from core.agent import PolyPuffAgent
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
