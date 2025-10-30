"""
Test script to diagnose data retrieval issues
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("DATA RETRIEVAL DIAGNOSTICS")
print("=" * 70)

# Test 1: Check API keys
print("\n1. CHECKING API KEYS:")
print("-" * 70)
openai_key = os.getenv("OPENAI_API_KEY")
alpha_key = os.getenv("ALPHA_VANTAGE_API_KEY")

print(f"OpenAI API Key: {'[OK] Found' if openai_key else '[MISSING]'}")
if openai_key:
    print(f"  Starts with: {openai_key[:20]}...")

print(f"Alpha Vantage API Key: {'[OK] Found' if alpha_key else '[MISSING]'}")
if alpha_key:
    print(f"  Value: {alpha_key}")

# Test 2: Check package installations
print("\n2. CHECKING PACKAGE INSTALLATIONS:")
print("-" * 70)
packages = ["yfinance", "stockstats", "pandas", "requests"]
for package in packages:
    try:
        __import__(package)
        print(f"[OK] {package} installed")
    except ImportError:
        print(f"[FAIL] {package} NOT installed")

# Test 3: Test yfinance directly
print("\n3. TESTING YFINANCE:")
print("-" * 70)
try:
    import yfinance as yf
    ticker = yf.Ticker("AAPL")
    data = ticker.history(start="2024-05-01", end="2024-05-10")

    if data.empty:
        print("[FAIL] YFinance returned empty data")
    else:
        print(f"[OK] YFinance working! Got {len(data)} days of data")
        print(f"  Date range: {data.index[0]} to {data.index[-1]}")
        print(f"  Columns: {list(data.columns)}")
        print(f"\n  Sample data (first 3 rows):")
        print(data.head(3))
except Exception as e:
    print(f"[FAIL] YFinance test failed: {type(e).__name__}: {e}")

# Test 4: Test Alpha Vantage API
print("\n4. TESTING ALPHA VANTAGE API:")
print("-" * 70)
if alpha_key:
    try:
        import requests
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={alpha_key}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "Time Series (Daily)" in data:
                print("[OK] Alpha Vantage API working!")
                time_series = data["Time Series (Daily)"]
                print(f"  Got {len(time_series)} days of data")
            elif "Note" in data:
                print("[RATE_LIMIT] Alpha Vantage Rate Limit Hit")
                print(f"  Message: {data['Note']}")
            elif "Error Message" in data:
                print(f"[FAIL] Alpha Vantage Error: {data['Error Message']}")
            else:
                print(f"[FAIL] Unexpected response format")
                print(f"  Keys in response: {list(data.keys())}")
        else:
            print(f"[FAIL] HTTP Error: Status code {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Alpha Vantage test failed: {type(e).__name__}: {e}")
else:
    print("[FAIL] Cannot test - API key not found")

# Test 5: Test framework's data retrieval
print("\n5. TESTING FRAMEWORK DATA RETRIEVAL:")
print("-" * 70)
try:
    from tradingagents.dataflows.interface import route_to_vendor
    from tradingagents.default_config import DEFAULT_CONFIG
    from tradingagents.dataflows.config import set_config

    # Set config
    config = DEFAULT_CONFIG.copy()
    config["data_vendors"] = {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "alpha_vantage",
        "news_data": "alpha_vantage",
    }
    set_config(config)

    print("Testing get_stock_data via framework...")
    result = route_to_vendor("get_stock_data", "AAPL", "2024-05-01", "2024-05-10")

    if "No data found" in str(result):
        print("[FAIL] Framework returned no data")
    elif len(str(result)) > 100:
        print("[OK] Framework get_stock_data working!")
        print(f"  Result length: {len(str(result))} characters")
        print(f"  First 200 chars: {str(result)[:200]}...")
    else:
        print(f"[FAIL] Unexpected result: {result}")

except Exception as e:
    print(f"[FAIL] Framework test failed: {type(e).__name__}: {e}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSTICS COMPLETE")
print("=" * 70)
