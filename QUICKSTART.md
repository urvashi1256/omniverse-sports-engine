# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure (Optional)
```bash
cp .env.example .env
# Edit .env to customize settings
```

### 3. Run!
```bash
# Try the demo first
python demo_live.py

# Then start the full engine
python main.py
```

---

## 📋 What to Expect

### Demo Output
- Shows today's fixtures from 5 major leagues
- Displays betting odds for each match
- Identifies underdog teams
- Simulates what happens when underdogs score

### Full Engine
- Runs continuously (press Ctrl+C to stop)
- Checks for live matches every 30 seconds
- Detects goals in real-time
- Executes trades when underdogs score
- Shows performance stats

---

## 🎯 Trading Logic

**The engine automatically buys when:**
1. A live match has a goal scored
2. The scoring team is an underdog (odds ≥ 2.5x)
3. We don't already have a position in that match
4. We have sufficient balance

**Position sizing:**
- Scales with how big of an underdog (higher odds = larger position)
- Maximum 2% of balance per trade
- Capped at MAX_POSITION_SIZE ($100 default)

---

## 🛠 Configuration Options

Edit `.env` to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `API_FOOTBALL_KEY` | Provided | Your API key |
| `UNDERDOG_THRESHOLD` | 2.5 | Minimum odds to be considered underdog |
| `INITIAL_BALANCE` | 10000 | Starting balance in USD |
| `MAX_POSITION_SIZE` | 100 | Maximum amount per trade |
| `POLL_INTERVAL` | 30 | Seconds between scans |
| `LEAGUES` | 39,140,135,78,61 | League IDs to track |

### Popular League IDs
- 39 = Premier League (England)
- 140 = La Liga (Spain)
- 135 = Serie A (Italy)
- 78 = Bundesliga (Germany)
- 61 = Ligue 1 (France)
- 2 = Champions League
- 3 = Europa League

---

## 📊 Understanding the Output

### When a Goal is Detected:
```
⚽ GOAL! Osasuna scored! Score: 0-1
🔍 Analyzing goal event...
✓ AWAY team is underdog (odds: 3.4 >= 2.5)
📊 TRADING SIGNAL: BUY
   Team: Osasuna
   Odds: 3.4
   Signal Strength: 68.00%
✅ BUY ORDER FILLED
   Order ID: #1
   Amount: $68.00
   Remaining Balance: $9,932.00
```

### Performance Stats:
```
==================================================
TRADING PERFORMANCE
==================================================
Initial Balance:  $10000.00
Current Balance:  $9932.00
Total P&L:        $-68.00
Total Trades:     1
Winning Trades:   0
Losing Trades:    0
Win Rate:         0.0%
Open Positions:   1
==================================================
```

---

## ⚠️ Important Notes

1. **API Rate Limits**: Free tier = 10 requests/minute
   - Engine caches odds to minimize calls
   - If you hit limits, wait 1 minute

2. **Simulated Trading**: All trades are simulated
   - No real money involved
   - Perfect for testing and learning

3. **Live Matches**: Engine only trades during live matches
   - Check fixture schedules on API-Football
   - Most matches on weekends

4. **No Position Closing**: Currently positions stay open
   - In production, you'd close when match ends
   - This would require result tracking

---

## 🧪 Testing

Run the test suite to verify everything works:
```bash
python test_engine.py
```

Should see:
```
Passed: 5/5
✅ All tests passed!
```

---

## 🐛 Troubleshooting

### "No fixtures found"
- Check if there are matches today in tracked leagues
- Try adding more league IDs to `.env`

### "API Error: rateLimit"
- You've hit the 10 requests/minute limit
- Wait 60 seconds and try again
- Engine will recover automatically

### "No odds available"
- Some matches don't have odds yet
- Try fixtures closer to kickoff time
- Some bookmakers may not cover all matches

### "Module not found"
- Make sure virtual environment is activated: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

---

## 💡 Tips for Success

1. **Run during peak times**: Weekends 12pm-6pm (European time)
2. **Watch big underdogs**: Odds above 4.0 create bigger signals
3. **Monitor API usage**: Check your dashboard at api-football.com
4. **Start with demo**: Get familiar before running full engine

---

## 🎓 Learn More

- Read `README.md` for detailed documentation
- Check `IMPLEMENTATION.md` to understand the code
- Explore individual files:
  - `scraper.py` - How match tracking works
  - `decision_engine.py` - Underdog detection logic
  - `executor.py` - Trading execution
  - `main.py` - Main engine loop

---

## ⚡ Ready to Start?

```bash
# Activate environment
source .venv/bin/activate

# Run the live demo
python demo_live.py

# Start trading!
python main.py
```

Press Ctrl+C anytime to stop and view your performance stats.

Good luck! 🍀⚽️
