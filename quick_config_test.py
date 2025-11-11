#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Configuration Test
Tests one stock with modified debate rounds to validate approach
"""

import os
import sys
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import time
from dotenv import load_dotenv

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

# Test parameters
ANALYSIS_DATE = "2024-05-10"
TEST_STOCK = "WMT"  # Walmart - should be BUY (actually went +70%)

print("="*70)
print("QUICK CONFIGURATION TEST")
print("="*70)
print(f"\nTesting: {TEST_STOCK}")
print(f"Date: {ANALYSIS_DATE}")
print(f"Expected: BUY (actual return: +70.24%)")
print()

# Test 1: Baseline (1 debate round)
print("\n" + "="*70)
print("TEST 1: BASELINE (max_debate_rounds=1)")
print("="*70)

config_baseline = DEFAULT_CONFIG.copy()
config_baseline["max_debate_rounds"] = 1
config_baseline["memory_prefix"] = f"quick_test_baseline_{int(time.time())}"

start = time.time()
ta_baseline = TradingAgentsGraph(debug=False, config=config_baseline)
final_state_1, decision_1 = ta_baseline.propagate(TEST_STOCK, ANALYSIS_DATE)
time_1 = time.time() - start

print(f"\n[RESULT] Baseline Decision: {decision_1}")
print(f"Time: {time_1:.1f}s")

# Test 2: More debate rounds
print("\n" + "="*70)
print("TEST 2: MORE DEBATE (max_debate_rounds=3)")
print("="*70)

config_more_debate = DEFAULT_CONFIG.copy()
config_more_debate["max_debate_rounds"] = 3
config_more_debate["memory_prefix"] = f"quick_test_debate3_{int(time.time())}"

start = time.time()
ta_debate = TradingAgentsGraph(debug=False, config=config_more_debate)
final_state_2, decision_2 = ta_debate.propagate(TEST_STOCK, ANALYSIS_DATE)
time_2 = time.time() - start

print(f"\n[RESULT] More Debate Decision: {decision_2}")
print(f"Time: {time_2:.1f}s")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"\nStock: {TEST_STOCK} (actual: +70.24%, should be BUY)")
print(f"\nBaseline (1 round):      {decision_1:6} ({time_1:.1f}s)")
print(f"More Debate (3 rounds):  {decision_2:6} ({time_2:.1f}s)")

if decision_1 == decision_2:
    print(f"\n⚠️  Same decision - debate rounds didn't change outcome")
else:
    print(f"\n✓ Different decision - debate rounds affected outcome!")

if decision_2 == "BUY":
    print(f"\n🎯 More debate rounds produced correct decision (BUY)!")
elif decision_1 == "BUY":
    print(f"\n🎯 Baseline produced correct decision (BUY)!")
else:
    print(f"\n❌ Neither configuration produced correct decision")

print(f"\nConfiguration testing approach is working!")
print(f"Ready to run full experiment suite if desired.")
