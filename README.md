# Omniverse Sports Engine

Simple underdog-goal trading engine for football prediction markets, built as an assignment for Omniverse Fund.

## Engine name

**Omniverse Football Underdog Engine**

## Markets targeted

- Football / soccer match-winner YES/NO style markets  
- Intended for exchanges similar to Kalshi / Polymarket where contracts track whether a team wins a given match

## Repository structure

- `scraper.py` – minimal match store and goal recording helper (stands in for live scores)
- `decision_engine.py` – underdog detection logic and signal generation
- `executor.py` – simulated order placement
- `main.py` – simple long‑running engine loop
- `demo.py` – one‑shot demo script used in the submission
- `requirements.txt` – Python dependencies
- `index.html` – static project page for the assignment

## How to run

git clone https://github.com/urvashi1256/omniverse-sports-engine.git
cd omniverse-sports-engine
pip install -r requirements.txt


Demo run (single goal → trade):

python demo.py

Engine loop (ticks and reacts to a seeded underdog goal):

python main.py


## Design notes

- The engine keeps an in‑memory dictionary of matches and the last scoring team.
- The decision layer treats teams tagged as `"underdog"` as underdogs; this is the place where implied probabilities from a real exchange API would plug in.
- The executor currently logs BUY orders to stdout but is structured to be swapped with a real Kalshi / Polymarket client.

## Known issues / limitations

- No real-time scraping yet (SofaScore / Livescore scraping is out of scope for this minimal submission).
- No real-money trading; all orders are simulated.
- No persistence layer or dashboard; everything is in-memory and printed.

