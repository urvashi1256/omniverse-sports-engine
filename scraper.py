# scraper.py
import requests
from datetime import datetime, timezone
from typing import Dict, List, Optional
import time
from collections import deque

try:
    from config import API_FOOTBALL_KEY, API_BASE_URL, API_RATE_LIMIT
except ImportError:
    # Fallback for standalone usage
    import os
    from dotenv import load_dotenv
    load_dotenv()
    API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://v3.football.api-sports.io")
    API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "10"))

if not API_FOOTBALL_KEY:
    raise ValueError("API_FOOTBALL_KEY not set in .env file")

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

# In-memory storage for matches
matches: Dict[int, Dict] = {}
processed_goals: set = set()  # Track goals we've already processed

# Rate limiting
request_timestamps = deque(maxlen=API_RATE_LIMIT)


def rate_limit_wait():
    """Implement rate limiting to stay under API_RATE_LIMIT requests per minute"""
    now = time.time()
    
    # Remove timestamps older than 60 seconds
    while request_timestamps and now - request_timestamps[0] > 60:
        request_timestamps.popleft()
    
    # If we've hit the limit, wait until we can make another request
    if len(request_timestamps) >= API_RATE_LIMIT:
        oldest_request = request_timestamps[0]
        wait_time = 60 - (now - oldest_request)
        if wait_time > 0:
            print(f"⏳ Rate limit reached. Waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time + 0.1)  # Add small buffer
    
    # Record this request
    request_timestamps.append(time.time())


class MatchTracker:
    """Tracks live football matches and detects new goals"""
    
    def __init__(self, leagues: List[int] = None):
        """
        Initialize the match tracker
        Args:
            leagues: List of league IDs to monitor (defaults to top European leagues)
        """
        # Default to top leagues: Premier League (39), La Liga (140), Serie A (135), 
        # Bundesliga (78), Ligue 1 (61)
        self.leagues = leagues or [39, 140, 135, 78, 61]
    
    def get_live_fixtures(self) -> List[Dict]:
        """Fetch all live fixtures from tracked leagues"""
        try:
            rate_limit_wait()
            url = f"{API_BASE_URL}/fixtures"
            params = {"live": "all"}
            
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("errors"):
                print(f"API Error: {data['errors']}")
                return []
            
            # Filter for our tracked leagues
            fixtures = [
                f for f in data.get("response", [])
                if f["league"]["id"] in self.leagues
            ]
            
            print(f"Found {len(fixtures)} live matches in tracked leagues")
            return fixtures
            
        except Exception as e:
            print(f"Error fetching live fixtures: {e}")
            return []
    
    def get_fixtures_by_date(self, date: str = None) -> List[Dict]:
        """
        Fetch fixtures for a specific date
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        try:
            rate_limit_wait()
            if not date:
                date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            
            url = f"{API_BASE_URL}/fixtures"
            params = {"date": date}
            
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("errors"):
                print(f"API Error: {data['errors']}")
                return []
            
            # Filter for our tracked leagues
            fixtures = [
                f for f in data.get("response", [])
                if f["league"]["id"] in self.leagues
            ]
            
            print(f"Found {len(fixtures)} fixtures on {date} in tracked leagues")
            return fixtures
            
        except Exception as e:
            print(f"Error fetching fixtures for {date}: {e}")
            return []
    
    def update_match_state(self, fixture: Dict) -> Optional[Dict]:
        """
        Update match state and detect new goals
        Returns: Dict with goal info if a new goal was detected, None otherwise
        """
        fixture_id = fixture["fixture"]["id"]
        home_team = fixture["teams"]["home"]["name"]
        away_team = fixture["teams"]["away"]["name"]
        home_score = fixture["goals"]["home"] or 0
        away_score = fixture["goals"]["away"] or 0
        status = fixture["fixture"]["status"]["short"]
        
        # Check if match is live
        if status not in ["1H", "HT", "2H", "ET", "BT", "P"]:
            return None
        
        total_goals = home_score + away_score
        
        # Initialize match if new
        if fixture_id not in matches:
            matches[fixture_id] = {
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "league": fixture["league"]["name"]
            }
            print(f"Started tracking: {home_team} vs {away_team} ({status})")
            return None
        
        # Check for new goals
        old_home = matches[fixture_id]["home_score"]
        old_away = matches[fixture_id]["away_score"]
        
        new_goal = None
        
        # Home team scored
        if home_score > old_home:
            goal_key = f"{fixture_id}_{home_score}_{away_score}_home"
            if goal_key not in processed_goals:
                processed_goals.add(goal_key)
                new_goal = {
                    "fixture_id": fixture_id,
                    "scoring_team": home_team,
                    "team_type": "home",
                    "minute": fixture["fixture"]["status"]["elapsed"],
                    "home_score": home_score,
                    "away_score": away_score,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                print(f"⚽ GOAL! {home_team} scored! Score: {home_score}-{away_score}")
        
        # Away team scored
        if away_score > old_away:
            goal_key = f"{fixture_id}_{home_score}_{away_score}_away"
            if goal_key not in processed_goals:
                processed_goals.add(goal_key)
                new_goal = {
                    "fixture_id": fixture_id,
                    "scoring_team": away_team,
                    "team_type": "away",
                    "minute": fixture["fixture"]["status"]["elapsed"],
                    "home_score": home_score,
                    "away_score": away_score,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                print(f"⚽ GOAL! {away_team} scored! Score: {home_score}-{away_score}")
        
        # Update stored state
        matches[fixture_id].update({
            "home_score": home_score,
            "away_score": away_score,
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "status": status
        })
        
        return new_goal
    
    def scan_for_goals(self) -> List[Dict]:
        """Scan all live matches and return list of new goals detected"""
        fixtures = self.get_live_fixtures()
        new_goals = []
        
        for fixture in fixtures:
            goal = self.update_match_state(fixture)
            if goal:
                new_goals.append(goal)
        
        return new_goals
