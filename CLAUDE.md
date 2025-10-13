# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TradingAgents is a multi-agent LLM financial trading framework built with LangGraph that mirrors real-world trading firm dynamics. The framework uses specialized LLM agents (analysts, researchers, traders, and risk managers) to collaboratively evaluate market conditions and make informed trading decisions.

**Research Paper**: arXiv:2412.20138

## Core Architecture

### Multi-Agent Pipeline Flow

The system follows a sequential pipeline mimicking institutional trading:

```
Analyst Team → Research Team → Trader → Risk Management → Portfolio Manager
```

### Agent Teams Structure

**1. Analyst Team** (`tradingagents/agents/analysts/`)

For **Equities**:
- `market_analyst.py` - Technical analysis using MACD, RSI, price patterns
- `social_media_analyst.py` - Sentiment analysis from social media
- `news_analyst.py` - Global news and macroeconomic indicators
- `fundamentals_analyst.py` - Company financials and intrinsic values

For **Cryptocurrency** (crypto-specific agents):
- `crypto_technical_analyst.py` - 24/7 market technical analysis, order book depth
- `onchain_analyst.py` - Blockchain metrics, whale activity, exchange flows
- `crypto_sentiment_analyst.py` - Crypto community sentiment, fear/greed index
- `crypto_fundamentals_analyst.py` - Tokenomics, protocol fundamentals, development activity

**2. Research Team** (`tradingagents/agents/researchers/`)
- `bull_researcher.py` - Bullish perspective analysis
- `bear_researcher.py` - Bearish perspective analysis
- `research_manager.py` - Debate moderator and final decision maker

**3. Trading Team** (`tradingagents/agents/trader/`)
- `trader.py` - Composes reports and makes trading decisions

**4. Risk Management** (`tradingagents/agents/risk_mgmt/`)
- `aggresive_debator.py` - High-risk tolerance perspective
- `conservative_debator.py` - Low-risk tolerance perspective
- `neutral_debator.py` - Balanced risk perspective

**5. Portfolio Management** (`tradingagents/agents/managers/`)
- `risk_manager.py` - Final approval/rejection of trades

### State Management

States are defined in `tradingagents/agents/utils/agent_states.py`:

- **AgentState**: Main state flowing through the graph (company, date, reports, decisions)
- **InvestDebateState**: Research team debate state (bull/bear history, judge decision)
- **RiskDebateState**: Risk management debate state (risky/safe/neutral perspectives)

### Graph Orchestration

The LangGraph workflow is managed in `tradingagents/graph/`:

- `trading_graph.py` - Main orchestration class (`TradingAgentsGraph`)
- `setup.py` - Graph construction and node configuration (`GraphSetup`)
- `propagation.py` - State initialization and execution (`Propagator`)
- `conditional_logic.py` - Routing logic between nodes (`ConditionalLogic`)
- `reflection.py` - Learning from past decisions (`Reflector`)
- `signal_processing.py` - Extract trading signals from decisions (`SignalProcessor`)

### Data Layer

Data flows through an abstraction layer in `tradingagents/dataflows/`:

**Configuration System**:
- `config.py` - Global config management with `set_config()` and `get_config()`
- `default_config.py` - Default settings including data vendors
- `crypto_config.py` - Crypto-specific configuration (24/7 markets, higher volatility, exchange settings)

**Vendor Implementations**:
- `alpha_vantage*.py` - Alpha Vantage API (fundamental, news, stock data)
- `y_finance.py` / `yfin_utils.py` - Yahoo Finance API (market data, indicators)
- `google.py` / `googlenews_utils.py` - Google News (alternative news source)
- `ccxt_vendor.py` - CCXT exchange integration for cryptocurrency data
- `messari_vendor.py` - Messari API for crypto fundamentals and news
- `glassnode_vendor.py` - Glassnode for on-chain metrics (whale tracking, exchange flows)
- `local.py` - Local data vendor for offline testing
- `openai.py` - LLM-based data vendor for fundamental/news analysis

**Tool Abstraction** (`tradingagents/agents/utils/`):
Abstract functions automatically route to configured vendor:
- `core_stock_tools.py` - `get_stock_data()`, `get_indicators()` for market data
- `fundamental_data_tools.py` - `get_fundamentals()`, `get_balance_sheet()`, `get_cashflow()`, `get_income_statement()`
- `news_data_tools.py` - `get_news()`, `get_global_news()`
- `technical_indicators_tools.py` - Technical indicator calculations
- `crypto_tools.py` - Crypto-specific tools (on-chain metrics, exchange data, whale tracking)

## Installation and Setup

### Environment Setup

```bash
# Clone and create virtual environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt

# Install package in development mode (REQUIRED for running CLI)
pip install -e .
```

**Important**: The `pip install -e .` step is **required** to register the `tradingagents` module with Python's import system. Without this, CLI scripts will fail with `ModuleNotFoundError`.

### API Keys Configuration

**Required APIs**:
- OpenAI API (for LLM agents)
- Alpha Vantage API (for fundamental and news data - default config for equities)

**Optional APIs** (for crypto):
- Glassnode API (on-chain metrics)
- Messari API (crypto fundamentals)
- Exchange APIs (Binance, Coinbase, etc. - for live trading)

**Setup via environment variables**:
```bash
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
export ALPHA_VANTAGE_API_KEY=$YOUR_ALPHA_VANTAGE_API_KEY

# Optional for crypto
export GLASSNODE_API_KEY=$YOUR_GLASSNODE_API_KEY
export MESSARI_API_KEY=$YOUR_MESSARI_API_KEY
```

**Setup via .env file**:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### Data Vendor Configuration

**For Equities** - Modify `tradingagents/default_config.py`:

```python
"data_vendors": {
    "core_stock_apis": "yfinance",       # yfinance, alpha_vantage, local
    "technical_indicators": "yfinance",  # yfinance, alpha_vantage, local
    "fundamental_data": "alpha_vantage", # openai, alpha_vantage, local
    "news_data": "alpha_vantage",        # openai, alpha_vantage, google, local
}
```

**For Cryptocurrency** - Uses `tradingagents/crypto_config.py` (CRYPTO_CONFIG):

```python
"data_vendors": {
    "core_stock_apis": "ccxt",        # CCXT for crypto OHLCV data
    "technical_indicators": "ccxt",   # CCXT for crypto technical indicators
    "fundamental_data": "messari",    # Messari for crypto fundamentals
    "news_data": "messari",           # Messari for crypto news
    "onchain_data": "glassnode",      # Glassnode for on-chain metrics
}
```

## Running the Framework

### CLI Mode - Equities (Interactive)

```bash
python -m cli.main
```

This launches an interactive CLI with:
- Ticker selection (e.g., NVDA, AAPL, SPY)
- Date selection
- Analyst team selection (Market, Social, News, Fundamentals)
- Research depth configuration (debate rounds)
- LLM provider and model selection
- Real-time progress tracking

### CLI Mode - Cryptocurrency (Interactive)

```bash
python -m cli.main_crypto
```

This launches the crypto-focused CLI with:
- Crypto symbol selection (e.g., BTC, ETH, SOL)
- Date selection
- Crypto analyst team selection (Technical, OnChain, Sentiment, Fundamentals)
- Exchange selection (Binance, Coinbase, Kraken, Bybit, OKX)
- Research depth configuration
- LLM provider and model selection
- Real-time progress tracking

**Key Differences - Crypto vs Equities**:
- **Trading Hours**: 24/7 vs 9:30-16:00 EST
- **Analysts**: Crypto-specific analysts with on-chain analysis
- **Data Sources**: CCXT, Glassnode, Messari vs Alpha Vantage, yFinance
- **Volatility**: ~3x higher for crypto (adjusted risk parameters)
- **Position Sizing**: Max 5% per crypto position vs 10% for stocks

### Python API Mode

**Basic usage - Equities** (`main.py`):
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Run analysis
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

**Basic usage - Cryptocurrency**:
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.crypto_config import CRYPTO_CONFIG

# Initialize with crypto config and crypto analysts
ta = TradingAgentsGraph(
    selected_analysts=["crypto_technical", "crypto_onchain", "crypto_sentiment", "crypto_fundamentals"],
    config=CRYPTO_CONFIG.copy(),
    debug=True
)

# Analyze Bitcoin
_, decision = ta.propagate("BTC", "2024-10-07")
print(decision)
```

**Custom configuration**:
```python
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"      # Deep thinking model
config["quick_think_llm"] = "gpt-4o-mini"     # Quick thinking model
config["max_debate_rounds"] = 1               # Research debate rounds
config["max_risk_discuss_rounds"] = 1         # Risk debate rounds

# LLM provider options: "openai", "anthropic", "google", "ollama", "openrouter"
config["llm_provider"] = "openai"
config["backend_url"] = "https://api.openai.com/v1"

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("AAPL", "2024-05-10")
```

**Reflection and learning**:
```python
# After getting returns, reflect and update memory
ta.reflect_and_remember(returns_losses=1000)  # Positive returns
```

## LLM Provider Support

The framework supports multiple LLM providers (configured in `tradingagents/graph/trading_graph.py:75-85`):

- **OpenAI**: `llm_provider: "openai"`, backend_url: `https://api.openai.com/v1`
- **Anthropic**: `llm_provider: "anthropic"`
- **Google**: `llm_provider: "google"`
- **Ollama**: `llm_provider: "ollama"` (local models)
- **OpenRouter**: `llm_provider: "openrouter"`

## Key Configuration Parameters

Located in `tradingagents/default_config.py` (equities) or `tradingagents/crypto_config.py` (crypto):

- `results_dir` - Output directory for results (default: `./results`)
- `deep_think_llm` - Model for complex reasoning (default: `o4-mini`)
- `quick_think_llm` - Model for quick tasks (default: `gpt-4o-mini`)
- `max_debate_rounds` - Research team debate rounds (default: `1`)
- `max_risk_discuss_rounds` - Risk team debate rounds (default: `1`)
- `data_vendors` - Data source configuration per category
- `market_type` - "stock" or "crypto" (crypto only)
- `default_exchange` - Default crypto exchange (crypto only)
- `risk_multiplier` - Risk adjustment factor (3.0x for crypto vs 1.0x for stocks)

## Output Structure

**Equities** - Results saved to:
```
results/
└── {TICKER}/
    └── {DATE}/
        ├── reports/
        │   ├── market_report.md
        │   ├── sentiment_report.md
        │   ├── news_report.md
        │   ├── fundamentals_report.md
        │   ├── investment_plan.md
        │   ├── trader_investment_plan.md
        │   └── final_trade_decision.md
        └── message_tool.log

eval_results/
└── {TICKER}/
    └── TradingAgentsStrategy_logs/
        └── full_states_log_{DATE}.json
```

**Cryptocurrency** - Results saved to:
```
results/crypto_{SYMBOL}/
└── {DATE}/
    ├── reports/
    │   ├── technical_report.md           # Price action, indicators
    │   ├── onchain_report.md             # Whale activity, exchange flows
    │   ├── sentiment_report.md           # Social sentiment, fear/greed
    │   ├── fundamentals_report.md        # Tokenomics, protocol health
    │   ├── investment_plan.md            # Research team decision
    │   ├── trader_investment_plan.md     # Trading strategy
    │   └── final_trade_decision.md       # Portfolio manager verdict
    └── message_tool.log                  # Full execution log
```

## Memory System

The framework includes a reflection-based learning system (`tradingagents/agents/utils/memory.py`):

- **FinancialSituationMemory**: Stores past decisions and outcomes
- Memories are agent-specific (bull, bear, trader, judge, risk manager)
- Uses ChromaDB for vector storage
- Enables learning from past trading mistakes

Memory is updated via:
```python
ta.reflect_and_remember(returns_losses)
```

## Testing and Development

**Cost-saving for testing**:
- Use `gpt-4o-mini` or `gpt-4.1-mini` instead of `o1-preview`/`gpt-4o`
- Set `max_debate_rounds: 1` to reduce API calls
- Use `local` data vendor with pre-downloaded data
- For crypto: Select fewer analysts (e.g., just Technical + OnChain)

**Debug mode**:
```python
ta = TradingAgentsGraph(debug=True, config=config)
```
This enables:
- LangGraph state tracing
- Pretty-printed message outputs
- Detailed logging

**Running tests**:
```bash
# Test imports
python -c "from tradingagents.agents import create_market_analyst; print('✓ Imports successful')"

# Test crypto imports
python -c "from tradingagents.agents import create_crypto_technical_analyst, create_onchain_analyst; print('✓ Crypto imports successful')"

# Run crypto tests (if available)
python crypto_trading/tests/test_crypto_data.py
python crypto_trading/tests/test_crypto_agents.py
```

## Cryptocurrency Trading Module

The framework includes dedicated cryptocurrency trading capabilities with specialized agents and tools:

**Crypto-Specific Features**:
- 24/7 market analysis
- On-chain metrics (whale tracking, exchange flows, network health)
- Multi-exchange support via CCXT (Binance, Coinbase, Kraken, Bybit, OKX)
- Higher volatility risk management (3x multiplier)
- Crypto-specific sentiment analysis (Twitter, Reddit, Telegram, Discord)
- Tokenomics and protocol fundamentals analysis

**Crypto Analyst Team**:
- **Technical Analyst**: Price patterns, indicators adapted for 24/7 markets
- **OnChain Analyst**: Blockchain metrics, whale activity, exchange inflows/outflows
- **Sentiment Analyst**: Crypto community sentiment, fear/greed index
- **Fundamentals Analyst**: Tokenomics, development activity, protocol health

**Exchange Support**:
The framework supports multiple exchanges through CCXT:
- Binance (largest volume)
- Coinbase (US-regulated)
- Kraken (European, good liquidity)
- Bybit (derivatives-focused)
- OKX (global)
- Additional exchanges can be configured in `crypto_config.py`

**Documentation**:
- `CRYPTO_QUICKSTART.md` - Quick start guide for crypto module
- `crypto_config.py` - Detailed crypto configuration reference

## Important Notes

1. **Package Installation**: Always run `pip install -e .` after cloning the repository. This is required for the CLI scripts to import the `tradingagents` module correctly.

2. **API Rate Limits**: The framework makes many API calls. Consider Alpha Vantage Premium for production use. For crypto, be aware of rate limits:
   - CCXT: Varies by exchange (~1200/min for major exchanges)
   - Glassnode: 60 requests/minute
   - Messari: 20 requests/minute (free tier)

3. **Data Vendor Fallbacks**: The system has fallback logic when primary vendors fail (see `tradingagents/agents/utils/core_stock_tools.py:23-45`).

4. **Research Disclaimer**: This framework is designed for research purposes. Trading performance varies based on LLM models, temperature, data quality, and other factors. Not intended as financial advice.

5. **Analyst Selection**: When initializing `TradingAgentsGraph`, you can select specific analysts:
   ```python
   # Equities
   ta = TradingAgentsGraph(
       selected_analysts=["market", "news", "fundamentals"],  # Skip social
       config=config
   )

   # Crypto
   ta = TradingAgentsGraph(
       selected_analysts=["crypto_technical", "crypto_onchain"],  # Minimal crypto setup
       config=CRYPTO_CONFIG
   )
   ```

6. **State Logging**: All states are automatically logged to JSON files for analysis and debugging.

7. **Crypto vs Equities**: The framework supports both traditional equities and cryptocurrency trading. Use `cli.main` for stocks and `cli.main_crypto` for cryptocurrency analysis. Each uses market-appropriate analysts, data sources, and risk parameters.

## Common Commands

```bash
# Install package (required first step)
pip install -e .

# Run equity analysis CLI
python -m cli.main

# Run cryptocurrency analysis CLI
python -m cli.main_crypto

# Run basic equity analysis programmatically
python main.py

# Check environment variables
echo $OPENAI_API_KEY
echo $ALPHA_VANTAGE_API_KEY

# View recent results
ls -la results/
cat results/{TICKER}/{DATE}/reports/final_trade_decision.md

# View crypto results
ls -la results/crypto_BTC/
cat results/crypto_BTC/{DATE}/reports/final_trade_decision.md
```
