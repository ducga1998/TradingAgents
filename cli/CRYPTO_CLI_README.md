# TradingAgents Crypto CLI

Multi-agent LLM framework for cryptocurrency trading analysis with 24/7 market support.

## Features

### Crypto-Specific Analysts
- **Technical Analyst**: Price action, indicators, order book analysis for 24/7 markets
- **OnChain Analyst**: Blockchain metrics, whale activity, exchange flows
- **Sentiment Analyst**: Social media, fear/greed index, crypto community sentiment
- **Fundamentals Analyst**: Tokenomics, project health, development activity

### Exchange Support
- Binance (default)
- Coinbase
- Kraken
- Bybit
- OKX

### Workflow
```
Analyst Team → Research Team → Trader → Risk Management → Portfolio Manager
```

## Quick Start

### Prerequisites
```bash
# Install TradingAgents package
cd TradingAgents
pip install -e .

# Set up API keys (required)
export OPENAI_API_KEY=your_key
export ALPHA_VANTAGE_API_KEY=your_key

# Optional: Crypto-specific API keys
export GLASSNODE_API_KEY=your_key  # For on-chain metrics
export MESSARI_API_KEY=your_key    # For crypto fundamentals
```

### Run Crypto CLI
```bash
python -m cli.main_crypto
```

### Interactive Workflow
The CLI will guide you through:
1. **Crypto Symbol** (e.g., BTC, ETH, SOL)
2. **Analysis Date** (YYYY-MM-DD format)
3. **Analyst Selection** (Technical, OnChain, Sentiment, Fundamentals)
4. **Exchange Selection** (Binance, Coinbase, Kraken, etc.)
5. **Research Depth** (Shallow/Medium/Deep)
6. **LLM Provider** (OpenAI, Anthropic, Google, etc.)
7. **Thinking Agents** (Quick and Deep thinkers)

## Output

Results are saved to:
```
results/crypto_{SYMBOL}/{DATE}/
├── reports/
│   ├── technical_report.md        # Technical analysis
│   ├── onchain_report.md          # On-chain metrics
│   ├── sentiment_report.md        # Sentiment analysis
│   ├── fundamentals_report.md     # Tokenomics & fundamentals
│   ├── investment_plan.md         # Research team decision
│   ├── trader_investment_plan.md  # Trading plan
│   └── final_trade_decision.md    # Portfolio manager decision
└── message_tool.log               # Full execution log
```

## Example Usage

```bash
# Run crypto analysis
python -m cli.main_crypto

# In the prompts:
# - Symbol: BTC
# - Date: 2025-10-08
# - Analysts: [x] All
# - Exchange: Binance
# - Depth: Medium
# - Provider: OpenAI
# - Models: gpt-4o-mini (quick), o4-mini (deep)
```

## Configuration

### Crypto Config
The framework uses `tradingagents/crypto_config.py` with:
- 24/7 trading hours
- Higher volatility risk multipliers
- Crypto-specific position sizing
- Exchange-specific fee structures
- On-chain analysis settings

### LLM Models
Recommended for crypto analysis:
- **Quick thinking**: gpt-4o-mini, claude-3-5-haiku-latest
- **Deep thinking**: o4-mini, claude-sonnet-4-0

### Data Vendors
- **Price data**: CCXT (exchange data)
- **On-chain**: Glassnode (requires API key)
- **Fundamentals**: Messari (requires API key)
- **News**: Messari, crypto-specific news sources

## Crypto vs Stock Analysis

| Feature | Stock CLI | Crypto CLI |
|---------|-----------|------------|
| Trading Hours | 9:30-16:00 EST | 24/7 |
| Analysts | Market, Social, News, Fundamentals | Technical, OnChain, Sentiment, Fundamentals |
| Data Sources | Alpha Vantage, yFinance | CCXT, Glassnode, Messari |
| Volatility | 1-2% daily | 5-10% daily |
| Position Sizing | 10% max | 5% max (higher risk) |

## Troubleshooting

### ModuleNotFoundError
```bash
# Make sure package is installed in dev mode
cd TradingAgents
pip install -e .
```

### API Key Issues
```bash
# Check environment variables
echo $OPENAI_API_KEY
echo $GLASSNODE_API_KEY

# Or use .env file
cp .env.example .env
# Edit .env with your keys
```

### Missing Crypto Analysts
If you get import errors:
```python
# Test imports
python -c "from tradingagents.agents import create_crypto_technical_analyst"
```

## Advanced Usage

### Custom Analyst Selection
You can select specific analysts programmatically:
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.crypto_config import CRYPTO_CONFIG

# Select only technical and on-chain analysts
config = CRYPTO_CONFIG.copy()
analysts = ["crypto_technical", "crypto_onchain"]

graph = TradingAgentsGraph(
    selected_analysts=analysts,
    config=config,
    debug=True
)

# Run analysis
_, decision = graph.propagate("BTC", "2025-10-08")
```

### Batch Analysis
```python
from cli.main_crypto import run_crypto_analysis

cryptos = ["BTC", "ETH", "SOL", "ADA"]
for crypto in cryptos:
    selections = {
        "crypto": crypto,
        "analysis_date": "2025-10-08",
        "analysts": ["Technical Analyst", "OnChain Analyst"],
        "exchange": "binance",
        # ... other settings
    }
    run_crypto_analysis()
```

## Notes

- **Real-time data**: CCXT provides real-time exchange data
- **On-chain data**: Glassnode requires paid API for full features
- **24/7 markets**: No weekend gaps, continuous analysis possible
- **Higher volatility**: Risk management adjusted for crypto markets
- **Research purpose**: Not financial advice, for research only

## Support

- Documentation: [TradingAgents GitHub](https://github.com/TauricResearch/TradingAgents)
- Issues: [GitHub Issues](https://github.com/TauricResearch/TradingAgents/issues)
- Research Paper: arXiv:2412.20138
