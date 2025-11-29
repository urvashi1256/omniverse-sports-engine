
def execute_buy(market_id, amount: int = 100):
    print(f"Placing BUY order on {market_id} for {amount} units (demo).")
    return {"status": "filled", "market_id": market_id, "amount": amount}
