# Omniverse Sports Engine

Automated underdog-goal trading engine for football prediction markets. Monitors live matches via API-Football, detects when underdog teams score using pre-match betting odds, and executes simulated trades on prediction markets.

## Engine name

**Omniverse Football Underdog Engine**

## Markets targeted

- Football / soccer match-winner YES/NO style markets  
- Intended for exchanges similar to Kalshi / Polymarket where contracts track whether a team wins a given match
- Trades are triggered when teams with odds ≥2.5x score goals (configurable threshold)

## Features

✅ **Real-time match tracking** via API-Football  
✅ **Odds-based underdog detection** using pre-match betting data  
✅ **Automated goal detection** with duplicate prevention  
✅ **Trading signal generation** with signal strength calculation  
✅ **Position tracking** and portfolio management  
✅ **Performance analytics** (P&L, win rate, trade history)  
✅ **Risk management** (position sizing, balance checks)  
✅ **Intelligent rate limiting** (auto-manages API request limits)  

## Repository structure

- `scraper.py` – Live match tracking and goal detection via API-Football
- `decision_engine.py` – Odds-based underdog detection and signal generation  
- `executor.py` – Simulated order execution with position tracking
- `main.py` – Main engine loop with continuous monitoring
- `config.py` – Configuration management with .env support
- `demo.py` – Legacy demo (kept for backward compatibility)
- `demo_live.py` – Enhanced demo with real API integration
- `requirements.txt` – Python dependencies
- `index.html` – Static project page

## Setup

```bash
git clone https://github.com/urvashi1256/omniverse-sports-engine.git
cd omniverse-sports-engine
pip install -r requirements.txt
```

### Configuration

**⚠️ IMPORTANT: Set up your `.env` file before running!**

```bash
cp .env.example .env
# Edit .env and add your API-Football API key
```

Key configuration options in `.env`:
- `API_FOOTBALL_KEY` – **REQUIRED** Your API-Football API key (get from api-football.com)
- `API_BASE_URL` – API endpoint (default: https://v3.football.api-sports.io)
- `API_RATE_LIMIT` – Max requests per minute (default: 10 for free tier)
- `INITIAL_BALANCE` – Starting balance (default: $10,000)
- `MAX_POSITION_SIZE` – Maximum per trade (default: $100)
- `UNDERDOG_THRESHOLD` – Minimum odds for underdog (default: 2.5)
- `POLL_INTERVAL` – Seconds between scans (default: 30)
- `LEAGUES` – Comma-separated league IDs to track

## How to run

### Live demo (checks real matches):
```bash
python demo_live.py
```

### Rate limiting demo:
```bash
python demo_rate_limit.py
```

### Continuous monitoring:
```bash
python main.py
```

This will:
1. Poll API-Football every 30 seconds for live matches
2. Detect goals as they happen
3. Fetch pre-match odds to identify underdogs
4. Execute buy orders when underdogs score
5. Track positions and performance

Press `Ctrl+C` to stop and view final stats.

### Legacy demo:
```bash
python demo.py
```

## How it works

1. **Match Tracking**: Fetches live fixtures from 5 major European leagues (Premier League, La Liga, Serie A, Bundesliga, Ligue 1)

2. **Goal Detection**: Monitors score changes and identifies new goals with duplicate prevention

3. **Underdog Analysis**: 
   - Fetches pre-match betting odds from bookmakers
   - Identifies teams with odds ≥ threshold (default 2.5x)
   - Calculates signal strength based on odds magnitude

4. **Trade Execution**:
   - Generates BUY signals when underdogs score
   - Sizes positions based on signal strength (max 2% of balance)
   - Tracks open positions and prevents duplicate trades
   - Records all orders for performance analysis

5. **Risk Management**:
   - Kelly Criterion-inspired position sizing
   - Maximum position limits
   - Balance checks before execution
   - One position per match maximum

## Design notes

- **Live Data**: Uses API-Football for real-time match data and betting odds
- **Underdog Detection**: Based on pre-match odds from bookmakers (default: Bet365)
- **Trading Logic**: Signal strength scales with underdog odds (higher odds = larger position)
- **Execution**: Simulated execution with full order and position tracking
- **State Management**: In-memory storage with deduplication for goal events
- **Extensibility**: Modular design allows easy swap to real exchange APIs (Kalshi/Polymarket)

## API Usage

The engine uses these API-Football endpoints:

- `GET /fixtures?live=all` – Live match data
- `GET /fixtures?date=YYYY-MM-DD` – Scheduled fixtures  
- `GET /odds?fixture={id}&bookmaker={id}&bet=1` – Match winner odds

### Rate Limiting

**Free tier limits**: 10 requests/minute, 100 requests/day

The engine handles this automatically:
- ✅ Tracks API requests in a 60-second rolling window
- ✅ Automatically waits when approaching the limit
- ✅ Prevents API errors from excessive requests
- ✅ Caches odds data (1-hour TTL) to minimize calls
- ✅ Configurable rate limit via `API_RATE_LIMIT` in `.env`

When rate limit is reached, you'll see:
```
⏳ Rate limit reached. Waiting 45.2 seconds...
```

## Performance Tracking

The engine tracks:
- Total P&L (profit/loss)
- Win rate percentage
- Number of winning/losing trades
- Open positions count
- Balance history

View stats with `executor.print_stats()` or at engine shutdown.

## Known limitations

- **Simulated trading only** – No real money execution (by design)
- **No position closing logic** – Positions remain open (would require result tracking)
- **API rate limits** – Free tier limits may restrict frequent polling
- **No historical backtesting** – Engine operates on live data only
- **No persistence** – All state is in-memory (cleared on restart)

## Future enhancements

- Real exchange integration (Kalshi/Polymarket APIs)
- Position auto-closing based on match results
- Database persistence for trade history
- Web dashboard for monitoring
- Backtesting framework
- Advanced risk models (Kelly Criterion, volatility-based sizing)
- Multi-market support (over/under, Asian handicap, etc.)

