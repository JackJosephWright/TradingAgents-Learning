# RTX 3500 Ada Setup Guide for Local LLMs

Guide for running TradingAgents with local LLMs on NVIDIA RTX 3500 Ada (12GB VRAM).

## Hardware Specifications

**NVIDIA RTX 3500 Ada Generation:**
- **VRAM**: 12GB GDDR6
- **CUDA Cores**: 5,120
- **Architecture**: Ada Lovelace
- **TDP**: 140W
- **Performance Tier**: Professional workstation GPU

**Verdict for TradingAgents**: ✅ **GOOD ENOUGH** for hybrid approach (local quick-thinking + cloud deep-thinking)

## What Your RTX 3500 Can Run

### ✅ Recommended Models (Will Run Well)

| Model | Size | VRAM Usage | Speed | Quality | Use Case |
|-------|------|------------|-------|---------|----------|
| Llama 3.3 | 8B | 8-10GB | Fast | Excellent | **Best choice for analysts** |
| Qwen 2.5 | 7B | 7-9GB | Very Fast | Excellent | Alternative to Llama |
| Mistral | 7B | 7-9GB | Fast | Good | Fallback option |
| Phi-3 Medium | 14B (Q4) | 10-11GB | Medium | Excellent | If you need more reasoning |

### ⚠️ Marginal Models (Will Work But Slow)

| Model | Size | VRAM Usage | Speed | Quality |
|-------|------|------------|-------|---------|
| Llama 3.3 | 8B (FP16) | 11-12GB | Slow | Best | Use Q5 quantization instead |
| Qwen 2.5 | 14B (Q4) | 11GB | Slow | Excellent | Only if you need the quality |

### ❌ Models You Cannot Run

| Model | Size | VRAM Needed | Why Not |
|-------|------|-------------|---------|
| Llama 3.1 | 70B | 48GB+ | Way too large |
| Qwen 2.5 | 32B | 24GB+ | Exceeds VRAM |
| DeepSeek R1 | 32B+ | 24GB+ | Too large |
| Any model | >14B | 12GB+ | VRAM limitation |

## Recommended Configuration

### Hybrid Approach (Best for RTX 3500)

This is the **optimal configuration** for your hardware:

```python
# config.py or main.py
DEFAULT_CONFIG = {
    # Use Ollama for fast, frequent analyst calls
    "llm_provider": "ollama",
    "quick_think_llm": "llama3.3:8b",  # LOCAL on RTX 3500
    "backend_url": "http://localhost:11434",

    # Use OpenAI for deep, critical manager decisions
    "deep_think_llm": "gpt-4o-mini",  # CLOUD API

    # Rest of config...
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
}
```

**What Runs Where:**
- ✅ **Local (RTX 3500)**: 4 Analyst agents, Bull/Bear researchers
- ☁️ **Cloud (OpenAI)**: Research Manager, Risk Manager (critical decisions)

**Performance Estimate:**
- Analyst calls: 3-5 seconds each (local)
- Manager calls: 1-2 seconds each (API)
- Total pipeline: **2-4 minutes per trading decision**

**Cost Estimate:**
- API calls: Only 2-3 manager decisions per run
- Cost per decision: **$0.20-$0.40** (50-60% savings vs full cloud)

## Installation Steps

### Step 1: Install Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Mac
brew install ollama

# Windows
# Download from https://ollama.com/download
```

Verify installation:
```bash
ollama --version
```

### Step 2: Download Llama 3.3 8B

```bash
# Download the model (this will take 5-10 minutes)
ollama pull llama3.3:8b

# Test it
ollama run llama3.3:8b "What is 2+2?"
```

### Step 3: Verify GPU Detection

```bash
# Check if Ollama sees your GPU
ollama ps

# Should show your RTX 3500
nvidia-smi
```

Expected output from `nvidia-smi`:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.x       Driver Version: 535.x       CUDA Version: 12.x     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        TCC/WDDM | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA RTX 3500...  On  | 00000000:01:00.0  On |                  N/A |
|  0%   40C    P8    15W / 140W |   8192MiB / 12288MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

### Step 4: Configure TradingAgents

Edit `main.py` or create a custom config:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

load_dotenv()

# Hybrid configuration for RTX 3500
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "ollama"
config["quick_think_llm"] = "llama3.3:8b"  # Local
config["deep_think_llm"] = "gpt-4o-mini"   # Cloud
config["backend_url"] = "http://localhost:11434"
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

### Step 5: Test Your Setup

```bash
# Start Ollama service (if not auto-started)
ollama serve &

# Run TradingAgents
python main.py
```

Monitor GPU usage while running:
```bash
watch -n 1 nvidia-smi
```

## Performance Tuning

### Optimization 1: Adjust Concurrency

If you have available RAM, enable parallel processing:

```python
config["max_workers"] = 2  # Run 2 analysts in parallel
```

### Optimization 2: Use Q5 Quantization

For slightly faster inference with minimal quality loss:

```bash
ollama pull llama3.3:8b-q5_k_m
```

Update config:
```python
config["quick_think_llm"] = "llama3.3:8b-q5_k_m"
```

### Optimization 3: Reduce Context Length

If running out of VRAM:

```python
config["max_tokens"] = 2048  # Reduce from default 4096
```

### Optimization 4: Monitor Temperature

Keep GPU cool for sustained performance:
```bash
# Check temperature every 5 seconds
watch -n 5 "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader"
```

Optimal operating temp: 50-75°C

## Advanced: Full Local Setup (Experimental)

If you want to try running everything locally (not recommended for RTX 3500):

```python
config = {
    "llm_provider": "ollama",
    "quick_think_llm": "llama3.3:8b",
    "deep_think_llm": "llama3.3:8b",  # Same model for everything
    "backend_url": "http://localhost:11434",
}
```

**Expected issues:**
- Slower inference (5-7 sec per call)
- Lower quality manager decisions
- Total pipeline time: 4-7 minutes
- May hit VRAM limits with long conversations

## Troubleshooting

### Issue 1: "CUDA out of memory"

**Solution 1**: Use smaller quantization
```bash
ollama pull llama3.3:8b-q4_k_m  # Smaller VRAM footprint
```

**Solution 2**: Close other GPU applications
```bash
# Check what's using GPU
nvidia-smi

# Kill other processes using GPU (be careful!)
kill <PID>
```

**Solution 3**: Reduce context window
```python
config["max_tokens"] = 1024
```

### Issue 2: Slow Performance

**Check 1**: Verify GPU is being used
```bash
# While running TradingAgents, check GPU usage
nvidia-smi
```

GPU-Util should show 80-100% during inference.

**Check 2**: Ensure Ollama uses GPU
```bash
# Check Ollama logs
journalctl -u ollama -f
```

Should see messages about CUDA initialization.

**Check 3**: CPU bottleneck
```bash
htop
```

If CPU is maxed out, reduce parallel workers:
```python
config["max_workers"] = 1
```

### Issue 3: Model Not Found

**Error**:
```
Error: model 'llama3.3:8b' not found
```

**Solution**:
```bash
# List downloaded models
ollama list

# Re-download if missing
ollama pull llama3.3:8b
```

### Issue 4: Ollama Connection Failed

**Error**:
```
Connection refused to http://localhost:11434
```

**Solution**:
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama service
ollama serve

# Or enable auto-start (Linux systemd)
sudo systemctl enable ollama
sudo systemctl start ollama
```

## Benchmarks for RTX 3500

Based on community testing:

| Model | Tokens/Second | Time per Call | Quality Score |
|-------|---------------|---------------|---------------|
| Llama 3.3 8B (Q5) | 25-35 tok/s | 3-4s | 9/10 |
| Llama 3.3 8B (FP16) | 15-25 tok/s | 4-6s | 10/10 |
| Qwen 2.5 7B (Q5) | 30-40 tok/s | 2-3s | 8.5/10 |
| Mistral 7B (Q5) | 30-40 tok/s | 2-3s | 8/10 |
| Phi-3 14B (Q4) | 12-18 tok/s | 5-8s | 9/10 |

**Comparison to Cloud:**
- GPT-4o-mini API: 50-100 tok/s (faster)
- GPT-4o-mini latency: 1-2s (network + processing)
- RTX 3500 local: 3-4s (no network overhead)

## Cost Analysis

See [COST_ANALYSIS.md](COST_ANALYSIS.md) for detailed breakdown.

**Quick Summary for RTX 3500 Hybrid:**
- **Hardware**: One-time $1,800 (RTX 3500)
- **Electricity**: ~$0.02 per decision (140W TDP)
- **API costs**: ~$0.25 per decision (managers only)
- **Break-even**: ~1,500 decisions vs full cloud GPT-4

## Alternative Models to Try

If Llama 3.3 doesn't meet your needs:

### For Speed (Fastest on RTX 3500)
```bash
ollama pull qwen2.5:7b
```

### For Code Understanding
```bash
ollama pull deepseek-coder:6.7b
```

### For Reasoning (Slower but Better)
```bash
ollama pull phi3:14b-q4_k_m
```

### For Finance-Specific Tasks
```bash
# No finance-specific 8B model yet
# Best bet: Fine-tune Llama 3.3 8B on financial data
```

## Next Steps

1. ✅ Get hybrid setup working first (easiest)
2. Run test decision: `python main.py`
3. Monitor performance with `nvidia-smi`
4. Compare outputs to cloud-only results
5. Experiment with different models
6. Consider fine-tuning for your trading strategy

## Learning Resources

- [Ollama Documentation](https://ollama.com/docs)
- [Llama 3 Model Card](https://huggingface.co/meta-llama/Llama-3.3-70B)
- [Qwen 2.5 Benchmarks](https://qwen.readthedocs.io/)
- [LangChain Ollama Integration](https://python.langchain.com/docs/integrations/llms/ollama)

## Community & Support

- [Ollama Discord](https://discord.gg/ollama)
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/)
- [RTX 3500 Benchmarks](https://www.techpowerup.com/gpu-specs/rtx-3500-ada-generation.c4032)
