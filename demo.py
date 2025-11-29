#!/usr/bin/env python3
"""
Simple demo showing the basic trading logic with a mock goal event.
For real API integration, use demo_live.py instead.
"""
from decision_engine import UnderdogDetector
from executor import TradingExecutor

print("\n" + "="*60)
print("  BASIC DEMO - Mock Underdog Goal")
print("="*60)
print("  This simulates what happens when an underdog scores.")
print("  For real matches, run: python demo_live.py")
print("="*60 + "\n")

# Initialize components
detector = UnderdogDetector(underdog_threshold=2.5)
executor = TradingExecutor(initial_balance=1000, max_position_size=50)

# Simulate an underdog goal event
mock_goal = {
    "fixture_id": 999999,
    "scoring_team": "Underdog FC",
    "team_type": "away",
    "minute": 23,
    "home_score": 0,
    "away_score": 1,
    "timestamp": "2025-11-29T12:00:00Z"
}

print("⚽ Simulating goal event:")
print(f"   Team: {mock_goal['scoring_team']}")
print(f"   Score: {mock_goal['home_score']}-{mock_goal['away_score']}\n")

# Analyze the goal
print("🔍 Analyzing with UnderdogDetector...")
signal = detector.analyze_goal_signal(mock_goal)

print(f"\n📊 Signal Generated:")
print(f"   Action: {signal['action']}")
print(f"   Reason: {signal['reason']}\n")

if signal["action"] == "BUY":
    print("✅ Would execute trade in real scenario")
    # Note: Won't actually execute since we don't have real odds
else:
    print("⏭️  No trade - team is not underdog")

print("\n" + "="*60)
print("💡 TIP: Run 'python demo_live.py' for real match data!")
print("="*60 + "\n")
