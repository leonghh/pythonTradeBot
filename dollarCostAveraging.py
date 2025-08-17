from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.credentials import broker
from lumibot.credentials import IS_BACKTESTING
from lumibot.strategies import Strategy
from lumibot.traders import Trader

class dollarCostAveraging(Strategy):

    def initialize(self):
        self.sleeptime = "30D"  # Execute trades every 30 days
        self.monthly_investment = self.cash // 12  # Divide total cash into 12 equal parts

    def on_trading_iteration(self):
        symbol = "SPY"
        price = self.get_last_price(symbol)

        if price is None:
            self.log_message(f"Price for {symbol} is unavailable. Skipping iteration.", level="ERROR")
            return

        # Calculate the quantity to buy with the monthly investment
        quantity = self.monthly_investment // price

        if quantity > 0:
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)
        else:
            self.log_message(f"Insufficient funds to buy {symbol}. Skipping iteration.", level="WARNING")


if __name__ == "__main__":
    if IS_BACKTESTING:
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        dollarCostAveraging.backtest(
            YahooDataBacktesting,
            start,
            end
        )
    else:
        strategy = dollarCostAveraging(broker=broker)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()