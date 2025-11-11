#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Variant Test - One stock, direct comparison
"""

import os
import sys
import shutil

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("="*80, flush=True)
print("SIMPLE VARIANT TEST", flush=True)
print("="*80, flush=True)

from datetime import datetime
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import time
from dotenv import load_dotenv

print("\n[INIT] Loading environment...", flush=True)
load_dotenv()

# Test parameters
ANALYSIS_DATE = "2024-05-10"
TEST_STOCK = "WMT"
ACTUAL_RETURN = +70.24

print(f"\n[CONFIG] Testing: {TEST_STOCK}", flush=True)
print(f"[CONFIG] Expected: BUY (actual return: {ACTUAL_RETURN:+.2f}%)", flush=True)

# Back up original
print("\n[SETUP] Backing up original research_manager.py...", flush=True)
original_file = "tradingagents/agents/managers/research_manager.py"
backup_file = "research_manager_test_backup.py"
shutil.copy2(original_file, backup_file)
print("[SETUP] Backup complete", flush=True)

results = []

try:
    # Test 1: Original
    print("\n" + "="*80, flush=True)
    print("TEST 1: ORIGINAL RESEARCH MANAGER", flush=True)
    print("="*80, flush=True)

    config1 = DEFAULT_CONFIG.copy()
    config1["memory_prefix"] = f"simple_test_original_{int(time.time())}"

    print("[TEST 1] Initializing...", flush=True)
    start = time.time()
    ta1 = TradingAgentsGraph(debug=False, config=config1)

    print("[TEST 1] Running analysis...", flush=True)
    final_state_1, decision_1 = ta1.propagate(TEST_STOCK, ANALYSIS_DATE)
    time_1 = time.time() - start

    print(f"\n[RESULT 1] Decision: {decision_1}", flush=True)
    print(f"[RESULT 1] Time: {time_1:.1f}s", flush=True)
    print(f"[RESULT 1] Grade: {'A' if decision_1 == 'BUY' else 'F' if decision_1 == 'SELL' else 'C'}", flush=True)

    results.append(("Original", decision_1, time_1))

    # Test 2: Balanced
    print("\n" + "="*80, flush=True)
    print("TEST 2: BALANCED RESEARCH MANAGER", flush=True)
    print("="*80, flush=True)

    print("[TEST 2] Swapping to balanced version...", flush=True)
    shutil.copy2("tradingagents/agents/managers/research_manager_balanced.py", original_file)

    # Reload modules
    print("[TEST 2] Reloading modules...", flush=True)
    import importlib
    import tradingagents.agents.managers.research_manager
    importlib.reload(tradingagents.agents.managers.research_manager)
    import tradingagents.agents
    importlib.reload(tradingagents.agents)

    config2 = DEFAULT_CONFIG.copy()
    config2["memory_prefix"] = f"simple_test_balanced_{int(time.time())}"

    print("[TEST 2] Initializing...", flush=True)
    start = time.time()
    ta2 = TradingAgentsGraph(debug=False, config=config2)

    print("[TEST 2] Running analysis...", flush=True)
    final_state_2, decision_2 = ta2.propagate(TEST_STOCK, ANALYSIS_DATE)
    time_2 = time.time() - start

    print(f"\n[RESULT 2] Decision: {decision_2}", flush=True)
    print(f"[RESULT 2] Time: {time_2:.1f}s", flush=True)
    print(f"[RESULT 2] Grade: {'A' if decision_2 == 'BUY' else 'F' if decision_2 == 'SELL' else 'C'}", flush=True)

    results.append(("Balanced", decision_2, time_2))

    # Test 3: Pro-Growth
    print("\n" + "="*80, flush=True)
    print("TEST 3: PRO-GROWTH RESEARCH MANAGER", flush=True)
    print("="*80, flush=True)

    print("[TEST 3] Swapping to pro-growth version...", flush=True)
    shutil.copy2("tradingagents/agents/managers/research_manager_growth.py", original_file)

    # Reload modules
    print("[TEST 3] Reloading modules...", flush=True)
    importlib.reload(tradingagents.agents.managers.research_manager)
    importlib.reload(tradingagents.agents)

    config3 = DEFAULT_CONFIG.copy()
    config3["memory_prefix"] = f"simple_test_growth_{int(time.time())}"

    print("[TEST 3] Initializing...", flush=True)
    start = time.time()
    ta3 = TradingAgentsGraph(debug=False, config=config3)

    print("[TEST 3] Running analysis...", flush=True)
    final_state_3, decision_3 = ta3.propagate(TEST_STOCK, ANALYSIS_DATE)
    time_3 = time.time() - start

    print(f"\n[RESULT 3] Decision: {decision_3}", flush=True)
    print(f"[RESULT 3] Time: {time_3:.1f}s", flush=True)
    print(f"[RESULT 3] Grade: {'A' if decision_3 == 'BUY' else 'F' if decision_3 == 'SELL' else 'C'}", flush=True)

    results.append(("Pro-Growth", decision_3, time_3))

finally:
    # Restore original
    print("\n[CLEANUP] Restoring original research_manager.py...", flush=True)
    shutil.copy2(backup_file, original_file)
    os.remove(backup_file)
    print("[CLEANUP] Restoration complete", flush=True)

# Summary
print("\n" + "="*80, flush=True)
print("SUMMARY", flush=True)
print("="*80, flush=True)
print(f"\nStock: {TEST_STOCK} (actual: {ACTUAL_RETURN:+.2f}%, should be BUY)\n", flush=True)

for variant, decision, exec_time in results:
    grade = 'A' if decision == 'BUY' else 'F' if decision == 'SELL' else 'C'
    symbol = '✓' if decision == 'BUY' else '✗'
    print(f"{variant:<15} {decision:>6}  {grade:>4}  ({exec_time:>5.1f}s) {symbol}", flush=True)

# Find best
correct = [v for v, d, t in results if d == 'BUY']
if correct:
    print(f"\n🎯 Correct variants: {', '.join(correct)}", flush=True)
else:
    print(f"\n❌ No variant produced correct decision (BUY)", flush=True)

print("\n" + "="*80, flush=True)
print("TEST COMPLETE", flush=True)
print("="*80, flush=True)
