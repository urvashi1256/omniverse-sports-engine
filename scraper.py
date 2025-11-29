# scraper.py
from collections import defaultdict

matches = defaultdict(dict)

def record_goal(match_id, team):
    matches[match_id]["last_goal"] = {"team": team}
