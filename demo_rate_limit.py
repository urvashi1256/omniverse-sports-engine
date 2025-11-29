#!/usr/bin/env python3
"""
Demo script to showcase rate limiting functionality
This will make multiple API calls to demonstrate rate limiting
"""
from scraper import MatchTracker, rate_limit_wait, request_timestamps
from decision_engine import UnderdogDetector
from config import API_RATE_LIMIT
from datetime import datetime
import time

def demo_rate_limiting():
    """Demonstrate rate limiting with multiple API calls"""
    print("\n" + "="*70)
    print("  RATE LIMITING DEMO")
    print("="*70)
    print(f"  API Rate Limit: {API_RATE_LIMIT} requests per minute")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    tracker = MatchTracker()
    detector = UnderdogDetector()
    
    # Show initial state
    print(f"📊 Current API requests in last 60s: {len(request_timestamps)}\n")
    
    # Fetch fixtures (1 request)
    print("1️⃣  Fetching today's fixtures...")
    start = time.time()
    fixtures = tracker.get_fixtures_by_date()
    elapsed = time.time() - start
    print(f"   ✅ Fetched {len(fixtures)} fixtures in {elapsed:.2f}s")
    print(f"   📊 API requests used: {len(request_timestamps)}/{API_RATE_LIMIT}\n")
    
    if not fixtures:
        print("No fixtures available for demo.\n")
        return
    
    # Try to fetch odds for multiple matches
    print(f"2️⃣  Fetching odds for {min(5, len(fixtures))} matches...")
    print("   (This will trigger rate limiting if needed)\n")
    
    for i, fixture in enumerate(fixtures[:5], 1):
        fixture_id = fixture['fixture']['id']
        home = fixture['teams']['home']['name']
        away = fixture['teams']['away']['name']
        
        print(f"   Match {i}: {home} vs {away}")
        print(f"   📊 Before: {len(request_timestamps)}/{API_RATE_LIMIT} requests")
        
        start = time.time()
        odds = detector.fetch_match_odds(fixture_id)
        elapsed = time.time() - start
        
        if odds:
            print(f"   ✅ Odds fetched in {elapsed:.2f}s")
            print(f"      Home: {odds.get('home_odds', 'N/A')}, "
                  f"Away: {odds.get('away_odds', 'N/A')}")
        else:
            print(f"   ⚠️  No odds available (took {elapsed:.2f}s)")
        
        print(f"   📊 After: {len(request_timestamps)}/{API_RATE_LIMIT} requests")
        print()
    
    # Final summary
    print("="*70)
    print("RATE LIMITING SUMMARY")
    print("="*70)
    print(f"Total API requests made: {len(request_timestamps)}")
    print(f"Rate limit: {API_RATE_LIMIT} per minute")
    print(f"Status: {'✅ Within limits' if len(request_timestamps) <= API_RATE_LIMIT else '⚠️ Limit enforced'}")
    print("\n💡 The rate limiting automatically waits when approaching limits")
    print("   This prevents API errors and ensures smooth operation.")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_rate_limiting()
