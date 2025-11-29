# decision_engine.py
import requests
from typing import Dict, Optional, List
from datetime import datetime, timezone

try:
    from config import API_FOOTBALL_KEY, API_BASE_URL
except ImportError:
    # Fallback for standalone usage
    import os
    from dotenv import load_dotenv
    load_dotenv()
    API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://v3.football.api-sports.io")

if not API_FOOTBALL_KEY:
    raise ValueError("API_FOOTBALL_KEY not set in .env file")

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

# Import rate limiting from scraper
try:
    from scraper import rate_limit_wait
except ImportError:
    # If scraper not available, create a dummy function
    def rate_limit_wait():
        pass

# Cache for odds data to avoid excessive API calls
odds_cache: Dict[int, Dict] = {}


class UnderdogDetector:
    """Detects underdog teams using betting odds from bookmakers"""
    
    def __init__(self, bookmaker_id: int = 8, underdog_threshold: float = 2.5):
        """
        Initialize underdog detector
        Args:
            bookmaker_id: Bookmaker ID (default 8 = Bet365)
            underdog_threshold: Minimum odds to consider a team underdog (e.g., 2.5 = 2.5x payout)
        """
        self.bookmaker_id = bookmaker_id
        self.underdog_threshold = underdog_threshold
        self.bet_id = 1  # Bet ID 1 = Match Winner
    
    def fetch_match_odds(self, fixture_id: int) -> Optional[Dict]:
        """
        Fetch betting odds for a specific fixture
        Returns dict with home_odds, away_odds, draw_odds
        """
        # Check cache first
        if fixture_id in odds_cache:
            cached_time = odds_cache[fixture_id].get("cached_at")
            if cached_time:
                # Use cached data if less than 1 hour old
                cache_age = (datetime.now(timezone.utc) - datetime.fromisoformat(cached_time)).seconds
                if cache_age < 3600:
                    return odds_cache[fixture_id].get("odds")
        
        try:
            rate_limit_wait()
            url = f"{API_BASE_URL}/odds"
            params = {
                "fixture": fixture_id,
                "bookmaker": self.bookmaker_id,
                "bet": self.bet_id
            }
            
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("errors"):
                print(f"API Error fetching odds for fixture {fixture_id}: {data['errors']}")
                return None
            
            results = data.get("response", [])
            if not results:
                print(f"No odds available for fixture {fixture_id}")
                return None
            
            # Extract odds from first result
            fixture_data = results[0]
            bookmakers = fixture_data.get("bookmakers", [])
            
            if not bookmakers:
                return None
            
            # Get the first bookmaker's data
            bookmaker = bookmakers[0]
            bets = bookmaker.get("bets", [])
            
            if not bets:
                return None
            
            # Match Winner bet should have 3 values: Home, Draw, Away
            bet = bets[0]
            values = bet.get("values", [])
            
            odds_dict = {}
            for value in values:
                label = value.get("value")
                odd = float(value.get("odd", 0))
                
                if label == "Home":
                    odds_dict["home_odds"] = odd
                elif label == "Away":
                    odds_dict["away_odds"] = odd
                elif label == "Draw":
                    odds_dict["draw_odds"] = odd
            
            # Cache the odds
            odds_cache[fixture_id] = {
                "odds": odds_dict,
                "cached_at": datetime.now(timezone.utc).isoformat()
            }
            
            print(f"Fetched odds for fixture {fixture_id}: {odds_dict}")
            return odds_dict
            
        except Exception as e:
            print(f"Error fetching odds for fixture {fixture_id}: {e}")
            return None
    
    def is_team_underdog(self, fixture_id: int, team_type: str) -> bool:
        """
        Check if a team is an underdog based on betting odds
        Args:
            fixture_id: The fixture ID
            team_type: "home" or "away"
        Returns:
            True if team is underdog (odds >= threshold), False otherwise
        """
        odds = self.fetch_match_odds(fixture_id)
        
        if not odds:
            print(f"Cannot determine underdog status - no odds available for fixture {fixture_id}")
            return False
        
        team_odds = odds.get(f"{team_type}_odds", 0)
        
        if team_odds == 0:
            return False
        
        is_underdog = team_odds >= self.underdog_threshold
        
        if is_underdog:
            print(f"✓ {team_type.upper()} team is underdog (odds: {team_odds} >= {self.underdog_threshold})")
        else:
            print(f"✗ {team_type.upper()} team is favorite (odds: {team_odds} < {self.underdog_threshold})")
        
        return is_underdog
    
    def get_implied_probability(self, odds: float) -> float:
        """Convert decimal odds to implied probability"""
        if odds <= 0:
            return 0
        return 1 / odds
    
    def analyze_goal_signal(self, goal_event: Dict) -> Dict:
        """
        Analyze a goal event and generate trading signal
        Args:
            goal_event: Dict with fixture_id, scoring_team, team_type, etc.
        Returns:
            Dict with signal strength and recommended action
        """
        fixture_id = goal_event["fixture_id"]
        team_type = goal_event["team_type"]
        scoring_team = goal_event["scoring_team"]
        
        # Check if scoring team is underdog
        is_underdog = self.is_team_underdog(fixture_id, team_type)
        
        if not is_underdog:
            return {
                "action": "PASS",
                "reason": "Scoring team is not underdog",
                "fixture_id": fixture_id,
                "team": scoring_team
            }
        
        # Get odds for signal strength
        odds = self.fetch_match_odds(fixture_id)
        team_odds = odds.get(f"{team_type}_odds", 0) if odds else 0
        
        # Higher odds = stronger signal
        signal_strength = min(team_odds / 5.0, 1.0)  # Normalize to 0-1
        
        return {
            "action": "BUY",
            "fixture_id": fixture_id,
            "team": scoring_team,
            "team_type": team_type,
            "odds": team_odds,
            "signal_strength": signal_strength,
            "reason": f"Underdog scored (odds: {team_odds})",
            "timestamp": goal_event.get("timestamp")
        }
