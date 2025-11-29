# main.py
import time
from scraper import matches, record_goal
from decision_engine import is_underdog
from executor import execute_buy

print("Starting Omniverse sports engine (demo mode)...")

def process_matches():
    for match_id, data in list(matches.items()):
        team = data.get("last_goal", {}).get("team")
        if not team:
            continue
        if is_underdog(match_id, team):
            execute_buy(match_id)
        else:
            print(f"No trade for {match_id}: {team} not underdog.")
        matches[match_id] = {}

# inject once
record_goal("live_demo_match", "underdog_fc")

while True:
    print("Engine tick...")
    process_matches()
    time.sleep(5)
