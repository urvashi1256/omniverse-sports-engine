#!/usr/bin/env python3
"""
Test script to verify API-Football integration and core functionality
"""
import os
import sys

def test_api_connection():
    """Test 1: API-Football connection"""
    print("\n" + "="*60)
    print("TEST 1: API-Football Connection")
    print("="*60)
    
    try:
        import requests
        from config import API_FOOTBALL_KEY, API_BASE_URL
        
        url = f"{API_BASE_URL}/timezone"
        headers = {"x-apisports-key": API_FOOTBALL_KEY}
        
        print(f"Testing connection to {API_BASE_URL}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("errors"):
            print(f"❌ FAILED: API returned errors: {data['errors']}")
            return False
        
        result_count = len(data.get("response", []))
        print(f"✅ PASSED: Connected successfully")
        print(f"   API returned {result_count} timezones")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_fetch_fixtures():
    """Test 2: Fetch fixtures"""
    print("\n" + "="*60)
    print("TEST 2: Fetch Today's Fixtures")
    print("="*60)
    
    try:
        from scraper import MatchTracker
        from datetime import datetime
        
        tracker = MatchTracker()
        today = datetime.now().strftime("%Y-%m-%d")
        
        print(f"Fetching fixtures for {today}...")
        fixtures = tracker.get_fixtures_by_date(today)
        
        print(f"✅ PASSED: Fetched {len(fixtures)} fixtures")
        
        if fixtures:
            print(f"\n   Sample fixture:")
            f = fixtures[0]
            print(f"   - {f['teams']['home']['name']} vs {f['teams']['away']['name']}")
            print(f"   - League: {f['league']['name']}")
            print(f"   - Status: {f['fixture']['status']['long']}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fetch_odds():
    """Test 3: Fetch betting odds"""
    print("\n" + "="*60)
    print("TEST 3: Fetch Betting Odds")
    print("="*60)
    
    try:
        from decision_engine import UnderdogDetector
        
        detector = UnderdogDetector()
        
        # Try to get a recent fixture ID
        from scraper import MatchTracker
        from datetime import datetime
        
        tracker = MatchTracker()
        fixtures = tracker.get_fixtures_by_date()
        
        if not fixtures:
            print("⚠️  SKIPPED: No fixtures available to test odds fetching")
            return True
        
        fixture_id = fixtures[0]['fixture']['id']
        print(f"Fetching odds for fixture {fixture_id}...")
        
        odds = detector.fetch_match_odds(fixture_id)
        
        if odds:
            print(f"✅ PASSED: Fetched odds successfully")
            print(f"   Home: {odds.get('home_odds', 'N/A')}")
            print(f"   Draw: {odds.get('draw_odds', 'N/A')}")
            print(f"   Away: {odds.get('away_odds', 'N/A')}")
            return True
        else:
            print(f"⚠️  WARNING: No odds available for this fixture")
            print(f"   (This is normal for some matches)")
            return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_executor():
    """Test 4: Trading executor"""
    print("\n" + "="*60)
    print("TEST 4: Trading Executor")
    print("="*60)
    
    try:
        from executor import TradingExecutor
        
        executor = TradingExecutor(initial_balance=1000, max_position_size=50)
        
        # Test buy order
        test_signal = {
            "fixture_id": 99999,
            "team": "Test FC",
            "team_type": "home",
            "odds": 3.5,
            "signal_strength": 0.8
        }
        
        print("Testing buy order execution...")
        result = executor.execute_buy(test_signal)
        
        if result["status"] == "filled":
            print(f"✅ PASSED: Order executed successfully")
            print(f"   Order ID: {result['order_id']}")
            print(f"   Amount: ${result['amount']:.2f}")
            
            # Test performance stats
            stats = executor.get_performance_stats()
            print(f"\n   Performance Stats:")
            print(f"   - Balance: ${stats['current_balance']:.2f}")
            print(f"   - Total Trades: {stats['total_trades']}")
            print(f"   - Open Positions: {stats['open_positions']}")
            
            return True
        else:
            print(f"❌ FAILED: Order rejected: {result.get('reason')}")
            return False
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_goal_detection():
    """Test 5: Goal detection and signal generation"""
    print("\n" + "="*60)
    print("TEST 5: Goal Detection & Signal Generation")
    print("="*60)
    
    try:
        from decision_engine import UnderdogDetector
        
        detector = UnderdogDetector(underdog_threshold=2.5)
        
        # Create a mock goal event
        mock_goal = {
            "fixture_id": 12345,
            "scoring_team": "Underdog FC",
            "team_type": "away",
            "minute": 23,
            "home_score": 0,
            "away_score": 1,
            "timestamp": "2025-11-29T12:00:00Z"
        }
        
        print("Testing signal generation for mock goal event...")
        signal = detector.analyze_goal_signal(mock_goal)
        
        print(f"✅ PASSED: Signal generated")
        print(f"   Action: {signal['action']}")
        print(f"   Reason: {signal['reason']}")
        
        if signal.get('signal_strength'):
            print(f"   Signal Strength: {signal['signal_strength']:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  OMNIVERSE SPORTS ENGINE - TEST SUITE")
    print("="*60)
    
    # Check dependencies
    print("\nChecking dependencies...")
    try:
        import requests
        import bs4
        import pandas
        import dotenv
        print("✅ All dependencies installed\n")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nPlease run: pip install -r requirements.txt\n")
        sys.exit(1)
    
    # Run tests
    tests = [
        test_api_connection,
        test_fetch_fixtures,
        test_fetch_odds,
        test_executor,
        test_goal_detection
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! The engine is ready to run.")
        print("\nNext steps:")
        print("  1. Run demo: python demo_live.py")
        print("  2. Start engine: python main.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    print("="*60 + "\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
