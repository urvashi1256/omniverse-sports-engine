#!/usr/bin/env python3
"""
Enhanced demo script that fetches real live matches and demonstrates the full pipeline
"""
from scraper import MatchTracker
from decision_engine import UnderdogDetector
from executor import TradingExecutor
from datetime import datetime

def demo_live_scan():
    """Demo: Scan for live matches and check for underdog opportunities"""
    print("\n" + "="*70)
    print("  OMNIVERSE SPORTS ENGINE - LIVE DEMO")
    print("="*70)
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    # Initialize components
    tracker = MatchTracker()
    detector = UnderdogDetector(underdog_threshold=2.5)
    executor = TradingExecutor(initial_balance=10000, max_position_size=100)
    
    print("📡 Fetching live fixtures from API-Football...\n")
    
    # Get today's fixtures
    fixtures = tracker.get_fixtures_by_date()
    
    if not fixtures:
        print("❌ No fixtures found for today in tracked leagues.")
        print("\n💡 TIP: The engine is configured to track:")
        print("   - Premier League (ID: 39)")
        print("   - La Liga (ID: 140)")
        print("   - Serie A (ID: 135)")
        print("   - Bundesliga (ID: 78)")
        print("   - Ligue 1 (ID: 61)")
        print("\n   Check if there are matches scheduled today in these leagues.\n")
        return
    
    print(f"✅ Found {len(fixtures)} fixture(s) today\n")
    
    # Display fixtures
    for i, fixture in enumerate(fixtures[:5], 1):  # Show first 5
        home = fixture["teams"]["home"]["name"]
        away = fixture["teams"]["away"]["name"]
        status = fixture["fixture"]["status"]["long"]
        league = fixture["league"]["name"]
        
        home_score = fixture["goals"]["home"] or 0
        away_score = fixture["goals"]["away"] or 0
        
        print(f"{i}. [{league}]")
        print(f"   {home} vs {away}")
        print(f"   Status: {status}")
        print(f"   Score: {home_score} - {away_score}")
        
        # Try to get odds
        fixture_id = fixture["fixture"]["id"]
        odds = detector.fetch_match_odds(fixture_id)
        
        if odds:
            print(f"   Odds - Home: {odds.get('home_odds', 'N/A')}, "
                  f"Draw: {odds.get('draw_odds', 'N/A')}, "
                  f"Away: {odds.get('away_odds', 'N/A')}")
            
            # Check for underdogs
            home_underdog = detector.is_team_underdog(fixture_id, "home")
            away_underdog = detector.is_team_underdog(fixture_id, "away")
            
            if home_underdog or away_underdog:
                print(f"   ⭐ Underdog detected!")
        else:
            print(f"   ⚠️  No odds available")
        
        print()
    
    # Scan for live matches and goals
    print("\n🔍 Scanning for LIVE matches with goals...\n")
    new_goals = tracker.scan_for_goals()
    
    if new_goals:
        print(f"⚽ Found {len(new_goals)} goal event(s)!\n")
        
        for goal in new_goals:
            print(f"Goal in fixture {goal['fixture_id']}")
            print(f"  Scoring team: {goal['scoring_team']} ({goal['team_type']})")
            print(f"  Score: {goal['home_score']}-{goal['away_score']}")
            print(f"  Minute: {goal['minute']}'")
            
            # Analyze the goal
            signal = detector.analyze_goal_signal(goal)
            
            if signal["action"] == "BUY":
                print(f"  ✅ TRADING SIGNAL: BUY")
                print(f"     Signal Strength: {signal['signal_strength']:.2%}")
                result = executor.execute_buy(signal)
            else:
                print(f"  ⏭️  No trade: {signal['reason']}")
            
            print()
    else:
        print("   No live goals detected at this moment.\n")
    
    # Show stats
    executor.print_stats()
    
    print("="*70)
    print("Demo completed! Run `python main.py` for continuous monitoring.")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_live_scan()
