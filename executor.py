# executor.py
from typing import Dict, List, Optional
from datetime import datetime, timezone
import json

# Order history and position tracking
order_history: List[Dict] = []
positions: Dict[int, Dict] = {}  # fixture_id -> position info
order_id_counter = 1


class TradingExecutor:
    """Simulated trading executor for prediction markets"""
    
    def __init__(self, initial_balance: float = 10000, max_position_size: float = 100):
        """
        Initialize trading executor
        Args:
            initial_balance: Starting balance in USD
            max_position_size: Maximum amount per trade
        """
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.max_position_size = max_position_size
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
    
    def calculate_position_size(self, signal_strength: float) -> float:
        """
        Calculate position size based on signal strength and Kelly Criterion principles
        Args:
            signal_strength: Value between 0 and 1
        Returns:
            Position size in USD
        """
        # Use a fraction of max position based on signal strength
        base_size = self.max_position_size * signal_strength
        
        # Don't risk more than 2% of balance per trade
        max_risk = self.balance * 0.02
        
        return min(base_size, max_risk, self.max_position_size)
    
    def execute_buy(self, signal: Dict) -> Dict:
        """
        Execute a buy order based on trading signal
        Args:
            signal: Trading signal dict from decision engine
        Returns:
            Order result dict
        """
        global order_id_counter
        
        fixture_id = signal["fixture_id"]
        team = signal["team"]
        team_type = signal["team_type"]
        odds = signal.get("odds", 0)
        signal_strength = signal.get("signal_strength", 0.5)
        
        # Calculate position size
        position_size = self.calculate_position_size(signal_strength)
        
        # Check if we have enough balance
        if position_size > self.balance:
            print(f"⚠️  Insufficient balance. Required: ${position_size:.2f}, Available: ${self.balance:.2f}")
            return {
                "status": "rejected",
                "reason": "insufficient_balance",
                "order_id": None
            }
        
        # Check if we already have a position in this match
        if fixture_id in positions:
            print(f"⚠️  Already have position in fixture {fixture_id}")
            return {
                "status": "rejected",
                "reason": "position_exists",
                "order_id": None
            }
        
        # Execute the order
        order_id = order_id_counter
        order_id_counter += 1
        
        order = {
            "order_id": order_id,
            "fixture_id": fixture_id,
            "team": team,
            "team_type": team_type,
            "action": "BUY",
            "amount": position_size,
            "odds": odds,
            "signal_strength": signal_strength,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "filled"
        }
        
        # Update balance
        self.balance -= position_size
        
        # Record position
        positions[fixture_id] = {
            "order_id": order_id,
            "team": team,
            "team_type": team_type,
            "entry_amount": position_size,
            "entry_odds": odds,
            "entry_time": order["timestamp"],
            "status": "open"
        }
        
        # Add to order history
        order_history.append(order)
        
        self.total_trades += 1
        
        print(f"✅ BUY ORDER FILLED")
        print(f"   Order ID: #{order_id}")
        print(f"   Fixture: {fixture_id}")
        print(f"   Team: {team} ({team_type})")
        print(f"   Amount: ${position_size:.2f}")
        print(f"   Odds: {odds}")
        print(f"   Signal Strength: {signal_strength:.2%}")
        print(f"   Remaining Balance: ${self.balance:.2f}")
        
        return order
    
    def close_position(self, fixture_id: int, outcome: str, payout: float = 0) -> Optional[Dict]:
        """
        Close a position for a completed match
        Args:
            fixture_id: The fixture ID
            outcome: "win" or "loss"
            payout: Amount returned (for wins)
        Returns:
            Closed position dict
        """
        if fixture_id not in positions:
            print(f"No open position for fixture {fixture_id}")
            return None
        
        position = positions[fixture_id]
        position["status"] = "closed"
        position["close_time"] = datetime.now(timezone.utc).isoformat()
        position["outcome"] = outcome
        position["payout"] = payout
        
        if outcome == "win":
            position["profit"] = payout - position["entry_amount"]
            self.balance += payout
            self.winning_trades += 1
            print(f"✅ Position CLOSED - WIN")
            print(f"   Profit: ${position['profit']:.2f}")
        else:
            position["profit"] = -position["entry_amount"]
            self.losing_trades += 1
            print(f"❌ Position CLOSED - LOSS")
            print(f"   Loss: ${position['entry_amount']:.2f}")
        
        print(f"   New Balance: ${self.balance:.2f}")
        
        del positions[fixture_id]
        return position
    
    def get_performance_stats(self) -> Dict:
        """Get trading performance statistics"""
        total_pnl = self.balance - self.initial_balance
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        
        return {
            "initial_balance": self.initial_balance,
            "current_balance": self.balance,
            "total_pnl": total_pnl,
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": win_rate,
            "open_positions": len(positions)
        }
    
    def print_stats(self):
        """Print performance statistics"""
        stats = self.get_performance_stats()
        
        print("\n" + "="*50)
        print("TRADING PERFORMANCE")
        print("="*50)
        print(f"Initial Balance:  ${stats['initial_balance']:.2f}")
        print(f"Current Balance:  ${stats['current_balance']:.2f}")
        print(f"Total P&L:        ${stats['total_pnl']:+.2f}")
        print(f"Total Trades:     {stats['total_trades']}")
        print(f"Winning Trades:   {stats['winning_trades']}")
        print(f"Losing Trades:    {stats['losing_trades']}")
        print(f"Win Rate:         {stats['win_rate']:.1f}%")
        print(f"Open Positions:   {stats['open_positions']}")
        print("="*50 + "\n")
