# Security & Rate Limiting Update

## ✅ Changes Implemented

### 1. **API Key Security**
- ✅ Removed all hardcoded API keys from source code
- ✅ Moved API configuration to `.env` file (gitignored)
- ✅ Added validation to ensure API key is set before running
- ✅ Updated `.env.example` to show required configuration

**Before:**
```python
API_KEY = os.getenv("API_FOOTBALL_KEY", "hardcoded_api_key")
BASE_URL = "https://v3.football.api-sports.io"
```

**After:**
```python
from config import API_FOOTBALL_KEY, API_BASE_URL
# Raises error if API_FOOTBALL_KEY not set in .env
```

### 2. **Intelligent Rate Limiting**
- ✅ Implemented rolling 60-second request tracking
- ✅ Automatic waiting when approaching API limits
- ✅ Configurable rate limit via `API_RATE_LIMIT` in `.env`
- ✅ Real-time feedback when rate limiting kicks in

**How it works:**
```python
def rate_limit_wait():
    """Waits if we've hit the rate limit (default: 10 req/min)"""
    - Tracks timestamps of all requests in last 60 seconds
    - If at limit, waits until oldest request expires
    - Automatically called before each API request
```

### 3. **Configuration Management**
All API and application settings now in `.env`:

```bash
# .env file
API_FOOTBALL_KEY=your_key_here        # Required
API_BASE_URL=https://...              # Optional (has default)
API_RATE_LIMIT=10                     # Requests per minute
INITIAL_BALANCE=10000
MAX_POSITION_SIZE=100
UNDERDOG_THRESHOLD=2.5
POLL_INTERVAL=30
LEAGUES=39,140,135,78,61
BOOKMAKER_ID=8
```

---

## 🔒 Security Improvements

### Before
- ❌ API key hardcoded in source files
- ❌ Could be accidentally committed to git
- ❌ Visible in code reviews and shared repos
- ❌ No central configuration

### After
- ✅ API key only in `.env` (gitignored)
- ✅ Cannot be committed (protected by `.gitignore`)
- ✅ Clean source code without secrets
- ✅ Centralized configuration management
- ✅ Example file (`.env.example`) for easy setup

---

## 📊 Rate Limiting Benefits

### Prevents API Errors
**Before:** Could hit rate limit and get errors like:
```json
{"errors": {"rateLimit": "Too many requests. Your rate limit is 10 requests per minute."}}
```

**After:** Automatically manages requests:
```
⏳ Rate limit reached. Waiting 45.2 seconds...
```

### Smart Request Management
- Tracks requests in rolling 60-second window
- Respects API limits automatically
- No manual intervention needed
- Provides clear feedback to user

### Demo Results
```
📊 Current API requests: 6/10
Status: ✅ Within limits
```

---

## 🚀 Files Modified

1. **`config.py`**
   - Now requires `API_FOOTBALL_KEY` from `.env`
   - Added `API_BASE_URL` and `API_RATE_LIMIT` config
   - Raises error if API key missing

2. **`scraper.py`**
   - Removed hardcoded API key and URL
   - Added `rate_limit_wait()` function
   - Implemented request tracking with deque
   - Applied rate limiting to all API calls

3. **`decision_engine.py`**
   - Removed hardcoded API key and URL
   - Imports rate limiting from scraper
   - Applied rate limiting to odds fetching

4. **`.env`** (new)
   - Contains actual API key and configuration
   - Gitignored for security

5. **`.env.example`**
   - Template for configuration
   - Shows all available options
   - Safe to commit (no real keys)

---

## 📋 Setup Instructions

### For New Users

1. **Clone the repository**
   ```bash
   git clone https://github.com/urvashi1256/omniverse-sports-engine.git
   cd omniverse-sports-engine
   ```

2. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

3. **Add your API key**
   ```bash
   # Edit .env and replace 'your_api_key_here' with your actual key
   nano .env
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the engine**
   ```bash
   python demo_live.py  # or python main.py
   ```

---

## 🧪 Testing Rate Limiting

Run the rate limiting demo:
```bash
python demo_rate_limit.py
```

This will:
- Make multiple API calls
- Show request count in real-time
- Demonstrate automatic waiting when needed
- Confirm everything works within limits

---

## ⚙️ Configuration Options

### API Rate Limit Tiers

| Tier | Requests/Minute | Requests/Day | Set in .env |
|------|-----------------|--------------|-------------|
| Free | 10 | 100 | `API_RATE_LIMIT=10` |
| Basic | 300 | 10,000 | `API_RATE_LIMIT=300` |
| Pro | 900 | 30,000 | `API_RATE_LIMIT=900` |

Update `API_RATE_LIMIT` in `.env` based on your API-Football subscription tier.

---

## 🔍 Monitoring Rate Limiting

The engine provides feedback:

```python
# When approaching limit
⏳ Rate limit reached. Waiting 45.2 seconds...

# Current status
📊 API requests used: 6/10

# In demo
Status: ✅ Within limits
```

---

## ✨ Benefits Summary

### Security
- ✅ No API keys in source code
- ✅ Safe to share repository
- ✅ Protected by `.gitignore`
- ✅ Easy key rotation (just update `.env`)

### Reliability
- ✅ Prevents rate limit errors
- ✅ Automatic request management
- ✅ No manual intervention needed
- ✅ Graceful handling of API limits

### Maintainability
- ✅ Centralized configuration
- ✅ Easy to update settings
- ✅ Clear separation of code and config
- ✅ Better for different environments (dev/prod)

---

## 🎯 Next Steps

1. ✅ Configuration secured in `.env`
2. ✅ Rate limiting implemented
3. ✅ All tests passing
4. ✅ Demo working correctly

**Ready to use!** Just run:
```bash
python main.py
```

The engine will now:
- Load configuration from `.env`
- Respect API rate limits automatically
- Operate safely and reliably
- Never expose API keys in code
