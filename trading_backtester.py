#!/usr/bin/env python3
import random
from typing import List, Dict

class Backtester:
    def __init__(self, initial_cash: float = 10000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.position = 0
        self.history: List[Dict[str,float]] = []

    def generate_price_data(self, days: int = 100) -> List[float]:
        prices = [100.0]
        for _ in range(1, days):
            change = random.uniform(-2, 2)
            prices.append(max(1, prices[-1] + change))
        return prices

    def moving_average(self, prices: List[float], period: int) -> List[float]:
        ma = []
        for i in range(len(prices)):
            if i + 1 < period:
                ma.append(None)
            else:
                ma.append(sum(prices[i+1-period:i+1])/period)
        return ma

    def run_strategy(self, prices: List[float], short_period: int = 5, long_period: int = 20):
        short_ma = self.moving_average(prices, short_period)
        long_ma = self.moving_average(prices, long_period)

        for i in range(len(prices)):
            price = prices[i]
            s_ma = short_ma[i]
            l_ma = long_ma[i]

            signal = None
            if s_ma and l_ma:
                if s_ma > l_ma and self.cash > 0:
                    self.position += self.cash / price
                    self.cash = 0
                    signal = "BUY"
                elif s_ma < l_ma and self.position > 0:
                    self.cash += self.position * price
                    self.position = 0
                    signal = "SELL"

            total_value = self.cash + self.position * price
            self.history.append({
                "Day": i+1,
                "Price": round(price,2),
                "Cash": round(self.cash,2),
                "Position": round(self.position,4),
                "Total Value": round(total_value,2),
                "Signal": signal
            })

    def performance_summary(self) -> Dict[str,float]:
        final_value = self.history[-1]["Total Value"] if self.history else self.initial_cash
        profit = final_value - self.initial_cash
        return {
            "Initial Cash": self.initial_cash,
            "Final Portfolio Value": round(final_value,2),
            "Total Profit": round(profit,2),
            "Return %": round((profit/self.initial_cash)*100,2)
        }

def demo():
    backtester = Backtester(initial_cash=10000)
    prices = backtester.generate_price_data(days=100)
    backtester.run_strategy(prices, short_period=5, long_period=20)

    print("Performance Summary:", backtester.performance_summary())
    print("Last 5 days of history:")
    for day in backtester.history[-5:]:
        print(day)

if __name__ == "__main__":
    demo()
