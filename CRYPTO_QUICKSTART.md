# 🚀 Crypto Trading CLI - Quick Start Guide

## What's New?

We've successfully built a **cryptocurrency-focused CLI** for the TradingAgents framework! 🎉

### New Features
✅ **4 Crypto-Specific Analysts**:
- Technical Analyst (24/7 markets, order books)
- OnChain Analyst (blockchain metrics, whale tracking)
- Sentiment Analyst (crypto community sentiment)
- Fundamentals Analyst (tokenomics, project health)

✅ **Exchange Support**: Binance, Coinbase, Kraken, Bybit, OKX

✅ **Rich Interactive CLI** with real-time progress tracking

✅ **Crypto-Optimized Config** (higher volatility, 24/7 trading)

---

## Installation & Setup

### Step 1: Install Package
```bash
cd TradingAgents
pip install -e .
```

### Step 2: Set API Keys
```bash
# Required
export OPENAI_API_KEY=your_openai_key
export ALPHA_VANTAGE_API_KEY=your_alphavantage_key

# Optional (for enhanced crypto features)
export GLASSNODE_API_KEY=your_glassnode_key  # On-chain data
export MESSARI_API_KEY=your_messari_key      # Crypto fundamentals
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your keys
```

---

## Usage

### Run the Crypto CLI
```bash
python -m cli.main_crypto
```

### Interactive Prompts
The CLI will guide you through 7 steps:

1. **Crypto Symbol**: `BTC`, `ETH`, `SOL`, etc.
2. **Date**: `2025-10-08` (YYYY-MM-DD)
3. **Analysts**: Select from 4 crypto analysts
4. **Exchange**: Binance, Coinbase, Kraken, etc.
5. **Research Depth**: Shallow (fast) / Medium / Deep (thorough)
6. **LLM Provider**: OpenAI, Anthropic, Google, etc.
7. **Models**: Quick thinker (gpt-4o-mini) + Deep thinker (o4-mini)

### Example Session
```
✓ Symbol: BTC
✓ Date: 2025-10-08
✓ Analysts: [x] Technical Analyst
            [x] OnChain Analyst
            [x] Sentiment Analyst
            [x] Fundamentals Analyst
✓ Exchange: Binance
✓ Depth: Medium (3 rounds)
✓ Provider: OpenAI
✓ Models: gpt-4o-mini / o4-mini
```

---

## Output Structure

Analysis results saved to:
```
results/crypto_BTC/2025-10-08/
├── reports/
│   ├── technical_report.md        # TA: Price action, indicators
│   ├── onchain_report.md          # Whale activity, flows
│   ├── sentiment_report.md        # Social media, fear/greed
│   ├── fundamentals_report.md     # Tokenomics, fundamentals
│   ├── investment_plan.md         # Research team decision
│   ├── trader_investment_plan.md  # Trading strategy
│   └── final_trade_decision.md    # Portfolio manager verdict
└── message_tool.log               # Full execution log
```

---

## What Was Changed?

### New Files Created
1. `cli/main_crypto.py` - Crypto-specific CLI with rich UI
2. `cli/CRYPTO_CLI_README.md` - Detailed documentation
3. `CRYPTO_QUICKSTART.md` - This file!

### Modified Files
1. `tradingagents/agents/__init__.py` - Added crypto analyst imports
2. `tradingagents/graph/setup.py` - Added crypto analyst graph support
3. `tradingagents/graph/conditional_logic.py` - Added crypto conditional logic
4. `tradingagents/graph/trading_graph.py` - Added crypto tool nodes

### Existing Crypto Infrastructure (Already Present)
- `tradingagents/crypto_config.py` - Crypto-specific configuration
- `tradingagents/agents/utils/crypto_tools.py` - Crypto data tools
- `tradingagents/agents/analysts/crypto_*.py` - Crypto analyst agents
- `tradingagents/dataflows/ccxt_vendor.py` - CCXT exchange integration
- `tradingagents/dataflows/messari_vendor.py` - Messari API integration

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI: cli/main_crypto.py                  │
│  Interactive prompts → Config selection → Live UI tracking  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              TradingAgentsGraph (Crypto Mode)               │
│  Selected Analysts: [crypto_technical, crypto_onchain, ...] │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Analyst Team Pipeline                    │
│  Technical → OnChain → Sentiment → Fundamentals             │
│         ↓                                                   │
│  Research Team (Bull vs Bear Debate)                        │
│         ↓                                                   │
│  Trader (Investment Plan)                                   │
│         ↓                                                   │
│  Risk Management (3-way debate)                             │
│         ↓                                                   │
│  Portfolio Manager (Final Decision)                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Crypto Data Sources (via Tools)                │
│  CCXT → Exchange price data                                 │
│  Glassnode → On-chain metrics                               │
│  Messari → Fundamentals & news                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Crypto vs Stock Comparison

| Feature | Stock CLI (`main.py`) | Crypto CLI (`main_crypto.py`) |
|---------|----------------------|------------------------------|
| **Trading Hours** | 9:30-16:00 EST | 24/7 |
| **Analysts** | Market, Social, News, Fundamentals | Technical, OnChain, Sentiment, Fundamentals |
| **Data Sources** | Alpha Vantage, yFinance | CCXT, Glassnode, Messari |
| **Typical Volatility** | 1-2% daily | 5-10% daily |
| **Position Sizing** | 10% max per trade | 5% max (higher risk) |
| **Unique Features** | Insider trading data | On-chain metrics, whale tracking |

---

## Testing

### Quick Test (No API calls)
```bash
# Test imports
python -c "from tradingagents.agents import create_crypto_technical_analyst, create_onchain_analyst; print('✓ All imports successful!')"

# Test CLI help
python -m cli.main_crypto --help
```

### Full Test (Requires API keys)
```bash
# Run full analysis
python -m cli.main_crypto

# Select minimal config to save API costs:
# - Analysts: [x] Technical Analyst only
# - Depth: Shallow (1 round)
# - Models: gpt-4o-mini / gpt-4o-mini
```

---

## Cost Optimization

For testing and development:

1. **Use cheaper models**:
   - Quick: `gpt-4o-mini` or `gpt-4.1-mini`
   - Deep: `gpt-4o-mini` (instead of `o4-mini` or `o1`)

2. **Reduce research depth**:
   - Shallow: 1 debate round (fastest)
   - Medium: 3 rounds (balanced)
   - Deep: 5 rounds (thorough but expensive)

3. **Select fewer analysts**:
   - Minimum: Technical + OnChain
   - Full analysis: All 4 analysts

4. **Use free tier APIs**:
   - CCXT: Free exchange data
   - Messari: Free tier available
   - Glassnode: Limited free tier

---

## Troubleshooting

### Issue: ModuleNotFoundError
```bash
# Solution: Install package in dev mode
cd TradingAgents
pip install -e .
```

### Issue: Missing API keys
```bash
# Check environment
echo $OPENAI_API_KEY

# Or use .env file
cp .env.example .env
vim .env  # Add your keys
```

### Issue: Import errors for crypto analysts
```python
# Test specific imports
from tradingagents.agents import (
    create_crypto_technical_analyst,
    create_onchain_analyst,
    create_crypto_sentiment_analyst,
    create_crypto_fundamentals_analyst
)
```

---

## Next Steps

1. **Run your first analysis**:
   ```bash
   python -m cli.main_crypto
   ```

2. **Review the reports**:
   ```bash
   ls -la results/crypto_BTC/2025-10-08/reports/
   cat results/crypto_BTC/2025-10-08/reports/final_trade_decision.md
   ```

3. **Experiment with different cryptos**:
   - Large cap: BTC, ETH
   - Mid cap: SOL, ADA, DOT
   - Small cap: Any altcoin

4. **Try different analyst combinations**:
   - Day trading: Technical + Sentiment
   - Long-term: Fundamentals + OnChain
   - Swing trading: All 4 analysts

---

## Support & Resources

- **Main README**: `README.md`
- **Crypto CLI Docs**: `cli/CRYPTO_CLI_README.md`
- **Research Paper**: arXiv:2412.20138
- **GitHub**: https://github.com/TauricResearch/TradingAgents

---

**🎉 You're all set! Happy crypto trading analysis!**

*Disclaimer: This framework is for research purposes only. Not financial advice.*
