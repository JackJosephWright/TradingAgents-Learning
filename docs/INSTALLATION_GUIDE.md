# TradingAgents Installation Guide

A beginner-friendly guide to setting up TradingAgents for learning and experimentation.

## Prerequisites

- **Python**: Version 3.10 or higher
- **Git**: For cloning the repository
- **API Keys** (optional for first exploration):
  - OpenAI API key (for cloud LLMs)
  - Alpha Vantage API key (for financial data)
- **Hardware**: See [RTX3500_SETUP.md](RTX3500_SETUP.md) for local LLM requirements

## Quick Start (Recommended for Beginners)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/TradingAgents-Learning.git
cd TradingAgents-Learning
```

### Step 2: Set Up Python Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies (The Easy Way)

**Use our minimal requirements file** to avoid dependency conflicts:

```bash
pip install -r requirements-minimal.txt
```

This installs only the core dependencies needed to run TradingAgents. Installation should complete in 2-5 minutes.

### Step 4: Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite text editor
nano .env
```

Add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

**Getting API Keys:**
- **OpenAI**: Sign up at [platform.openai.com](https://platform.openai.com)
- **Alpha Vantage**: Free key at [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

### Step 5: Test Your Installation

```bash
python main.py
```

This will run a sample trading analysis for NVDA stock. Expected runtime: 2-5 minutes.

## Troubleshooting

### Problem 1: Dependency Resolution Takes Forever

**Symptoms:**
- `pip install -r requirements.txt` runs for 30+ minutes
- Messages like "INFO: pip is looking at multiple versions..."
- Stuck in endless version resolution loop

**Solution:**
Use `requirements-minimal.txt` instead:
```bash
pip install -r requirements-minimal.txt
```

**Why this happens:**
The full `requirements.txt` includes `langchain-experimental` which has conflicting version constraints with newer LangChain packages. Our minimal requirements skip problematic packages while keeping core functionality.

### Problem 2: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Solution:**
Make sure your virtual environment is activated:
```bash
# Check if venv is active (should see (venv) in prompt)
which python  # Should point to your venv directory

# If not activated:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Problem 3: API Key Errors

**Symptoms:**
```
openai.error.AuthenticationError: Invalid API key
```

**Solution:**
1. Check `.env` file has correct keys (no quotes needed)
2. Verify API keys are valid at provider websites
3. Make sure `.env` is in the correct directory (TradingAgents root)
4. Restart your Python session after editing `.env`

### Problem 4: Rate Limiting

**Symptoms:**
```
Rate limit exceeded
```

**Solution:**
- **OpenAI**: Upgrade to paid tier or wait for rate limit reset
- **Alpha Vantage**: Free tier allows 5 calls/minute, 500/day
- Consider using local models (see [RTX3500_SETUP.md](RTX3500_SETUP.md))

### Problem 5: Out of Memory (OOM)

**Symptoms:**
```
CUDA out of memory
```

**Solution:**
This happens when trying to run local LLMs. See [RTX3500_SETUP.md](RTX3500_SETUP.md) for:
- Recommended model sizes for your GPU
- Quantization strategies
- Hybrid cloud/local configurations

## Advanced Installation Options

### Option 1: Full Dependencies (Not Recommended)

If you need all optional features:

```bash
pip install -r requirements.txt
```

Warning: This may take 30+ minutes and could fail due to version conflicts.

### Option 2: Development Installation

For contributing or modifying the code:

```bash
pip install -e .
```

### Option 3: Using uv (Faster)

If you have `uv` installed:

```bash
uv sync
```

## Verifying Your Installation

Run these commands to verify everything is working:

```bash
# Check Python version
python --version  # Should be 3.10+

# Check key packages
python -c "import langchain; print(langchain.__version__)"
python -c "import langgraph; print(langgraph.__version__)"
python -c "import openai; print(openai.__version__)"

# List all installed packages
pip list
```

## Next Steps

1. Read [LEARNING_PATH.md](LEARNING_PATH.md) for recommended learning order
2. Explore [TRADINGAGENTS_DEEP_DIVE.md](../TRADINGAGENTS_DEEP_DIVE.md) for architecture details
3. Check [COST_ANALYSIS.md](COST_ANALYSIS.md) to understand API costs
4. Try [RTX3500_SETUP.md](RTX3500_SETUP.md) for local LLM setup

## Getting Help

If you run into issues:

1. Check this troubleshooting section
2. Review the [original TradingAgents repo](https://github.com/TauricResearch/TradingAgents) issues
3. Read the deep dive documentation
4. Open an issue in this repository

## Common Questions

**Q: Can I run this without API keys?**
A: Not yet out of the box. You need either OpenAI API access or to configure Ollama for local models. See RTX3500_SETUP.md for local setup.

**Q: How much will API calls cost?**
A: Approximately $0.50-$2.00 per trading decision with GPT-4. See COST_ANALYSIS.md for detailed breakdown and cost-saving strategies.

**Q: Can I use this for real trading?**
A: This is an educational and research framework. DO NOT use it for live trading without extensive testing and risk management.

**Q: Why minimal requirements instead of full requirements.txt?**
A: The full requirements.txt includes experimental packages that conflict with stable LangChain versions. Minimal requirements provide core functionality with reliable installation.
