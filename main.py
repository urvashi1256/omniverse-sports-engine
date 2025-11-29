# main.py
import time
import signal
import sys
from datetime import datetime
from scraper import MatchTracker
from decision_engine import UnderdogDetector
from executor import TradingExecutor
from config import (
    POLL_INTERVAL,
    LEAGUES,
    UNDERDOG_THRESHOLD,
    INITIAL_BALANCE,
    MAX_POSITION_SIZE
)

# Initialize components
tracker = MatchTracker(leagues=LEAGUES)
detector = UnderdogDetector(underdog_threshold=UNDERDOG_THRESHOLD)
executor = TradingExecutor(initial_balance=INITIAL_BALANCE, max_position_size=MAX_POSITION_SIZE)

# Global flag for graceful shutdown
running = True


def signal_handler(sig, frame):
    """Handle Ctrl+C for graceful shutdown"""
    global running
    print("\n\n🛑 Shutting down engine...")
    running = False


def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("  OMNIVERSE FOOTBALL UNDERDOG TRADING ENGINE")
    print("="*60)
    print(f"  Tracking Leagues: {len(LEAGUES)} major European leagues")
    print(f"  Underdog Threshold: {UNDERDOG_THRESHOLD}x odds")
    print(f"  Poll Interval: {POLL_INTERVAL} seconds")
    print(f"  Initial Balance: ${INITIAL_BALANCE}")
    print(f"  Max Position Size: ${MAX_POSITION_SIZE}")
    print("="*60 + "\n")


def process_goal(goal_event):
    """Process a goal event through the trading pipeline"""
    print(f"\n{'='*60}")
    print(f"⚽ GOAL EVENT DETECTED")
    print(f"{'='*60}")
    print(f"Fixture ID: {goal_event['fixture_id']}")
    print(f"Scoring Team: {goal_event['scoring_team']} ({goal_event['team_type']})")
    print(f"Score: {goal_event['home_score']}-{goal_event['away_score']}")
    print(f"Minute: {goal_event['minute']}'")
    print(f"{'='*60}\n")
    
    # Analyze the goal and get trading signal
    print("🔍 Analyzing goal event...")
    signal = detector.analyze_goal_signal(goal_event)
    
    if signal["action"] == "PASS":
        print(f"⏭️  PASS - {signal['reason']}\n")
        return
    
    # Execute the trade
    print(f"\n📊 TRADING SIGNAL: {signal['action']}")
    print(f"   Team: {signal['team']}")
    print(f"   Odds: {signal['odds']}")
    print(f"   Signal Strength: {signal['signal_strength']:.2%}\n")
    
    result = executor.execute_buy(signal)
    
    if result["status"] == "rejected":
        print(f"❌ Order rejected: {result['reason']}\n")
    
    print()


def main_loop():
    """Main engine loop"""
    print_banner()
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    iteration = 0
    
    print(f"🚀 Engine started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ Scanning for live matches every {POLL_INTERVAL} seconds...\n")
    
    while running:
        iteration += 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        print(f"[{timestamp}] Scan #{iteration} - Checking for live matches and goals...")
        
        try:
            # Scan for new goals in live matches
            new_goals = tracker.scan_for_goals()
            
            if new_goals:
                print(f"✅ Found {len(new_goals)} new goal(s)!\n")
                
                # Process each goal
                for goal in new_goals:
                    process_goal(goal)
            else:
                print(f"   No new goals detected.\n")
            
            # Show stats every 10 iterations
            if iteration % 10 == 0:
                executor.print_stats()
            
        except Exception as e:
            print(f"❌ Error during scan: {e}\n")
        
        # Wait before next scan
        if running:
            for remaining in range(POLL_INTERVAL, 0, -1):
                if not running:
                    break
                if remaining % 10 == 0 or remaining <= 5:
                    print(f"   Next scan in {remaining} seconds...", end='\r')
                time.sleep(1)
            print()  # New line after countdown
    
    # Shutdown
    print("\n" + "="*60)
    print("ENGINE STOPPED")
    print("="*60)
    executor.print_stats()
    print("Thank you for using Omniverse Sports Engine!\n")


if __name__ == "__main__":
    main_loop()
