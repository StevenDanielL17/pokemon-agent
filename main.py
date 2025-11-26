import os
from config import settings
from core.agent import Agent

def main():
    print("Starting Pokemon Agent...")
    agent = Agent()
    agent.run()

if __name__ == "__main__":
    main()
