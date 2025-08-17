from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.credentials import broker
from lumibot.credentials import IS_BACKTESTING
from lumibot.strategies import Strategy
from lumibot.traders import Trader

class BuyHold(Strategy):

    def initialize(self):
        self.sleeptime = "10S"


    def on_trading_iteration(self):
        if self.first_iteration:
            symbol = "SPY"
            price = self.get_last_price(symbol)
            quantity = self.cash // price
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)


if __name__ == "__main__":
    if IS_BACKTESTING:
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        BuyHold.backtest(
            YahooDataBacktesting,
            start,
            end
        )
    else:
        strategy = BuyHold(broker=broker)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()      