# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://v3.football.api-sports.io")

if not API_FOOTBALL_KEY:
    raise ValueError("API_FOOTBALL_KEY not found in .env file. Please set it.")

# Trading Configuration
INITIAL_BALANCE = float(os.getenv("INITIAL_BALANCE", "10000"))
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "100"))
UNDERDOG_THRESHOLD = float(os.getenv("UNDERDOG_THRESHOLD", "2.5"))

# Polling Configuration
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))

# Rate Limiting
API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", "10"))  # requests per minute

# League Configuration
LEAGUES_STR = os.getenv("LEAGUES", "39,140,135,78,61")
LEAGUES = [int(x.strip()) for x in LEAGUES_STR.split(",")]

# Bookmaker Configuration
BOOKMAKER_ID = int(os.getenv("BOOKMAKER_ID", "8"))

# League Names (for display)
LEAGUE_NAMES = {
    39: "Premier League",
    140: "La Liga",
    135: "Serie A",
    78: "Bundesliga",
    61: "Ligue 1",
    2: "UEFA Champions League",
    3: "UEFA Europa League"
}
