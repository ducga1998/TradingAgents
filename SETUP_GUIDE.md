# TradingAgents Setup Guide

## Quick Setup (5 minutes)

### 1. Create Virtual Environment
```bash
cd /Users/nguyenminhduc/Desktop/TradingAgents
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -e .
pip install -r requirements.txt
```

### 3. Set Up API Keys
Create a `.env` file in the project root:
```bash
# Required
OPENAI_API_KEY=your_openai_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Optional (for crypto features)
GLASSNODE_API_KEY=your_glassnode_key_here
MESSARI_API_KEY=your_messari_key_here
```

Or export them in your shell:
```bash
export OPENAI_API_KEY=your_openai_key_here
export ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### 4. Run the Crypto CLI

**Easiest Way:**
```bash
./run_crypto_cli.sh
```

**Alternative:**
```bash
PYTHONPATH=$(pwd) venv/bin/python cli/main_crypto.py
```

## Verified Setup

✅ Virtual environment created at: `venv/`
✅ Package installed in development mode
✅ All dependencies installed (including `ccxt` and `glassnode`)
✅ Wrapper script created: `run_crypto_cli.sh`

## What Was Fixed

The original error:
```
ModuleNotFoundError: No module named 'tradingagents'
```

Was caused by:
1. Missing `ccxt` and `glassnode` dependencies
2. PYTHONPATH not including project root

**Solutions implemented:**
1. ✅ Created `run_crypto_cli.sh` wrapper that sets PYTHONPATH automatically
2. ✅ Updated `pyproject.toml` to include missing dependencies
3. ✅ Updated documentation with correct setup instructions

## Testing Your Setup

```bash
# Test 1: Check if tradingagents can be imported
./run_crypto_cli.sh --help

# Expected output:
# Usage: main_crypto.py [OPTIONS]
# Run cryptocurrency analysis with multi-agent LLM framework

# Test 2: Verify dependencies
venv/bin/python -c "import ccxt; import glassnode; print('Dependencies OK')"

# Test 3: Check API keys (if set)
venv/bin/python -c "import os; print('OPENAI_API_KEY:', 'set' if os.getenv('OPENAI_API_KEY') else 'not set')"
```

## Next Steps

1. **Run your first analysis:**
   ```bash
   ./run_crypto_cli.sh
   ```
   
2. **Select options in the interactive prompts:**
   - Crypto Symbol: BTC
   - Analysis Date: Today's date
   - Analysts: Select all (Technical, OnChain, Sentiment, Fundamentals)
   - Exchange: Binance
   - Research Depth: Medium
   - LLM Provider: OpenAI
   - Models: gpt-4o-mini (quick), o4-mini (deep)

3. **View results:**
   ```bash
   ls results/crypto_BTC/$(date +%Y-%m-%d)/
   ```

## Additional Resources

- **Crypto CLI Documentation:** `cli/CRYPTO_CLI_README.md`
- **Crypto Quick Start:** `CRYPTO_QUICKSTART.md`
- **Example Scripts:** `crypto_trading/examples/`
- **Paper Trading:** `crypto_trading/scripts/run_paper_trading.py`

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution:** Always use `./run_crypto_cli.sh` or set PYTHONPATH:
```bash
PYTHONPATH=$(pwd) venv/bin/python cli/main_crypto.py
```

### Issue: Missing API keys
**Solution:** Set environment variables or create `.env` file:
```bash
export OPENAI_API_KEY=your_key
```

### Issue: Import errors for crypto analysts
**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt
```

## Support

- GitHub Issues: https://github.com/TauricResearch/TradingAgents/issues
- Documentation: See `cli/CRYPTO_CLI_README.md`

