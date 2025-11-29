# demo.py
from scraper import matches, record_goal
from decision_engine import is_underdog
from executor import execute_buy

print("Demo: Simulating EPL underdog goal...")

# simulate that an underdog just scored
record_goal("demo_match", "underdog_fc")

if is_underdog("demo_match", "underdog_fc"):
    execute_buy("demo_match")
else:
    print("No trade – scoring team not underdog or price above threshold.")
