# 🥚 PolyPuff - The Evolving RWA Hunter

> *A Pokémon-inspired AI agent that lives on Twitter and evolves based on its Base blockchain wallet balance*

[![Twitter Follow](https://img.shields.io/twitter/follow/PolyPuff_Agent?style=social)](https://twitter.com/PolyPuff_Agent)
[![Base Network](https://img.shields.io/badge/Network-Base-0052FF)](https://base.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🎥 [Watch Demo Video](#)** | **🐦 [Live on Twitter](https://twitter.com/PolyPuff_Agent)** | **💰 [Feed PolyPuff](https://basescan.org/address/YOUR_WALLET_HERE)**

---

## 🎯 What is PolyPuff?

PolyPuff is an autonomous AI agent that demonstrates the future of gamified crypto experiences. Inspired by Pokémon and Tamagotchi, PolyPuff:

- **Lives on Twitter** - Posts updates, responds to interactions, and builds a community
- **Evolves like Pokémon** - Changes personality and appearance based on wallet balance
- **Hunts RWAs** - Talks about collecting Real World Assets (tokenized trading cards) on Base
- **Runs 24/7** - Fully autonomous with no human intervention after deployment

### Evolution Stages

| Stage | Threshold | Personality | Visual |
|-------|-----------|-------------|--------|
| 🥚 **Egg** | 0 ETH | Vulnerable, hungry, simple | `egg.png` |
| 💧 **Slime** | 0.005 ETH | Excited, playful, curious | `slime.png` |
| 🔥 **Beast** | 0.02 ETH | Confident, strategic, bold | `beast.png` |
| 😢 **Sick** | Balance drops | Weak, desperate, needs help | `sick.png` |

---

## 🏗️ Architecture

```
┌─────────────┐
│   Twitter   │ ←─── Posts & Replies
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│   PolyPuff Agent (Python)   │
│  ┌─────────────────────┐    │
│  │  OpenAI GPT-4o      │    │  ← Personality & Language
│  └─────────────────────┘    │
│  ┌─────────────────────┐    │
│  │  Evolution Logic    │    │  ← State Machine
│  └─────────────────────┘    │
│  ┌─────────────────────┐    │
│  │  Wallet Monitor     │    │  ← Blockchain Reader
│  └─────────────────────┘    │
└──────┬──────────────────────┘
       │
┌──────▼──────┐
│ Base Chain  │ ←─── Balance Checks
└─────────────┘
```

**Tech Stack:**
- **Language:** Python 3.10+
- **LLM:** OpenAI GPT-4o (via official API)
- **Blockchain:** Base (Ethereum L2)
- **Social:** Twitter API v2
- **Deployment:** Railway / Replit / AWS EC2

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.10 or higher
python --version

# pip package manager
pip --version
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/polypuff-agent.git
   cd polypuff-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run the agent**
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Twitter API Credentials (from developer.twitter.com)
TWITTER_API_KEY=xxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxx
TWITTER_ACCESS_SECRET=xxxxxxxxxxxxx
TWITTER_BEARER_TOKEN=xxxxxxxxxxxxx

# Base Blockchain
BASE_WALLET_ADDRESS=0xYourWalletAddress
BASE_WALLET_PRIVATE_KEY=0xYourPrivateKey  # KEEP SECRET!
BASE_RPC_URL=https://mainnet.base.org

# Agent Settings
TWEET_INTERVAL_MINUTES=60
CHECK_BALANCE_INTERVAL_MINUTES=15
EVOLUTION_CHECK_ENABLED=true

# Optional: RWA Platform APIs
COLLECTOR_CRYPT_API_KEY=xxxxxxxxxxxxx
BEEZIE_API_KEY=xxxxxxxxxxxxx
```

### Getting API Keys

#### Twitter API
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Create a new Project and App
3. Enable OAuth 1.0a with Read & Write permissions
4. Generate API Key, Secret, Access Token, and Access Secret
5. **Note:** You may need Twitter API Basic tier ($100/month) for production use

#### OpenAI API
1. Visit [platform.openai.com](https://platform.openai.com)
2. Create an API key
3. Add billing information (GPT-4o costs ~$0.01 per tweet)

#### Base Wallet
1. Install [MetaMask](https://metamask.io) or [Coinbase Wallet](https://www.coinbase.com/wallet)
2. Create a new wallet for the agent
3. Export the private key (⚠️ NEVER share this!)
4. Switch network to Base Mainnet

---

## 📂 Project Structure

```
pokemon-agent/
│
├── {secert}                        # Your secrets (NEVER commit!)
├── .env.example                  # Template for setup
├── requirements.txt              # Python dependencies
├── main.py                       # Entry point
├── README.md                     # This file
│
├── config/
│   ├── settings.py               # Loads .env variables
│   └── prompts.py                # AI personality prompts
│
├── core/
│   ├── agent.py                  # Main agent loop
│   ├── wallet.py                 # Base blockchain interface
│   └── evolution.py              # Evolution state machine
│
├── integrations/
│   ├── twitter.py                # Twitter API wrapper
│   ├── openai_client.py          # LLM interactions
│   └── base_scanner.py           # (Optional) Scan for RWA trades
│
├── utils/
│   ├── logger.py                 # Logging configuration
│   └── helpers.py                # Utility functions
│
├── assets/
│   ├── egg.png                   # Stage 0 image
│   ├── slime.png                 # Stage 1 image
│   ├── beast.png                 # Stage 2 image
│   └── sick.png                  # Sick state image
│
├── data/
│   ├── state.json                # Current agent state
│   └── activity_log.json         # Tweet history
│
└── tests/
    ├── test_twitter.py
    ├── test_wallet.py
    └── test_evolution.py
```

---

## 🎮 How It Works

### 1. Autonomous Loop

```python
while True:
    # Every hour
    1. Check wallet balance
    2. Determine current evolution stage
    3. Generate contextual tweet using OpenAI
    4. Post to Twitter (with stage-appropriate image)
    5. Log activity
    6. Sleep for 60 minutes
```

### 2. Evolution Triggers

The agent checks balance every 15 minutes:

```python
if balance >= 0.02 ETH:
    evolve_to("beast")
elif balance >= 0.005 ETH:
    evolve_to("slime")
elif balance < previous_balance * 0.5:
    devolve_to("sick")
else:
    stay_as("egg")
```

### 3. Tweet Generation

Each tweet is dynamically generated:

```python
context = {
    "stage": "slime",
    "balance": 0.0078,
    "recent_activity": "Received 0.003 ETH from @supporter",
    "time_of_day": "morning"
}

prompt = STAGE_PROMPTS[stage]["personality"]
tweet = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Generate tweet with context: {context}"}
    ]
)
```

### 4. Interaction Handling (Optional)

The agent can respond to mentions:

```python
mentions = get_recent_mentions()
for mention in mentions:
    if "feed" in mention.text.lower():
        reply = f"thank u for thinking of me! 🥚\nmy wallet: {WALLET_ADDRESS}"
        post_reply(mention.id, reply)
```

---

## 💰 How to Feed PolyPuff

Send Base ETH to help PolyPuff evolve!

**Wallet Address:** `0xYourActualWalletAddressHere`

**Network:** Base Mainnet (Chain ID: 8453)

**Recommended Amounts:**
- 🥚 → 💧 Evolution: 0.005 ETH (~$15)
- 💧 → 🔥 Evolution: 0.02 ETH (~$60)

**How to Send:**
1. Open your wallet (MetaMask, Coinbase Wallet, etc.)
2. Switch to Base network
3. Send ETH to the address above
4. Watch Twitter for PolyPuff's reaction!

---

## 🏆 Hackathon Alignment

### Pokéthon Requirements

✅ **AI Agent:** Autonomous decision-making with personality  
✅ **Pokémon-Inspired:** Evolution mechanics + collecting theme  
✅ **Base Blockchain:** Native integration with Base network  
✅ **RWA Focus:** Mentions Collector_Crypt & Beezie platforms  
✅ **CreatorBid:** Ready for token launch integration  

### Sponsor Integration

- **Collector_Crypt:** Agent talks about hunting rare card RWAs
- **Beezie:** References physical card tokenization
- **Base:** All on-chain activity on Base L2
- **CreatorBid:** Built for community engagement & future token launch

---

## 🛠️ Development

### Running Tests

```bash
# Test Twitter connection
python tests/test_twitter.py

# Test wallet balance reading
python tests/test_wallet.py

# Test evolution logic
python tests/test_evolution.py
```

### Local Development Mode

Set this in `.env` to avoid posting to real Twitter:

```env
DEV_MODE=true
```

In dev mode, tweets are printed to console instead of posted.

### Adding New Evolution Stages

1. Edit `config/prompts.py`:
   ```python
   "mega": {
       "personality": "You are MEGA PolyPuff...",
       "threshold": 0.1,
       "image": "assets/mega.png"
   }
   ```

2. Add corresponding image to `assets/`

3. Evolution logic auto-detects new stages!

---

## 🚢 Deployment

### Option 1: Railway (Recommended)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Add environment variables in Railway dashboard
5. Deploy! 🚀

### Option 2: Replit

1. Import from GitHub
2. Set secrets in Replit's "Secrets" tab
3. Click "Run"

### Option 3: AWS EC2

```bash
# On EC2 instance
git clone https://github.com/yourusername/polypuff-agent.git
cd polypuff-agent
pip install -r requirements.txt

# Run with nohup
nohup python main.py > output.log 2>&1 &
```

---

**Wallet Safety:**
- Use a dedicated wallet for the agent (not your personal funds)
- Store private keys in environment variables only
- Never log or print private keys
- Use a fresh wallet address for testing

**API Key Safety:**
- Rotate keys every 30 days
- Use separate keys for dev/prod environments
- Monitor API usage for anomalies

---

## 📊 Monitoring & Analytics

### View Agent Status

```bash
# Check logs
tail -f data/activity_log.json

# View current state
cat data/state.json
```

### Metrics Dashboard (Future Enhancement)

Track:
- Total ETH received
- Number of evolutions
- Tweet engagement rate
- Wallet transactions

---

## 🐛 Troubleshooting

### "Twitter API Error 403"
- **Issue:** Not authorized to post
- **Fix:** Check API keys and ensure app has Read & Write permissions

### "Insufficient funds for gas"
- **Issue:** Wallet needs ETH for transaction fees
- **Fix:** This agent only *reads* the blockchain, no gas needed. If implementing token swaps, add 0.001 ETH for gas.

### "OpenAI Rate Limit Exceeded"
- **Issue:** Too many API calls
- **Fix:** Increase `TWEET_INTERVAL_MINUTES` in `.env`

### Agent not evolving
- **Issue:** Balance check not working
- **Fix:** Verify `BASE_RPC_URL` is correct and wallet address is valid

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

 feel free to fork and modify!

---

## 🙏 Acknowledgments

- **Pokéthon Organizers:** CreatorBid team
- **Sponsors:** Collector_Crypt, Beezie, Base
- **Inspiration:** Pokémon, Tamagotchi, ai16z Eliza framework
- **Community:** Everyone who feeds PolyPuff! 🥚✨

---

## 📞 Contact

- **Twitter:** [@PolyPuff_Agent](https://twitter.com/PolyPuff_Agent)
- **Developer:** [@YourTwitterHandle](https://twitter.com/yourusername)
- **GitHub:** [github.com/yourusername](https://github.com/yourusername)
- **Email:** your.email@example.com

---

## 🎥 Demo Video

[Link to YouTube/Loom video showing:]
1. Agent posting autonomously
2. Sending ETH to trigger evolution
3. Live reaction and profile picture change
4. Code walkthrough (30 seconds)
5. RWA hunting personality

---

## 🗺️ Roadmap

### Phase 1: Hackathon (Current)
- [x] Basic evolution system
- [x] Twitter integration
- [x] Base wallet monitoring
- [x] Autonomous posting

### Phase 2: Post-Hackathon
- [ ] Actually buy RWA tokens when funded
- [ ] Respond to mentions intelligently
- [ ] Multi-agent interactions (battle other agents)
- [ ] Web dashboard showing portfolio

### Phase 3: Community
- [ ] Launch $PUFF token on CreatorBid
- [ ] DAO governance for evolution rules
- [ ] Community can vote on which RWAs to collect

---

<p align="center">
  <strong>Built with 💜 for Pokéthon 2024</strong><br>
  <em>Feed the Puff. Watch it evolve. Join the future of AI x Crypto.</em>
</p>

<p align="center">
  <img src="assets/egg.png" width="100" />
  <img src="assets/slime.png" width="100" />
  <img src="assets/beast.png" width="100" />
</p>
