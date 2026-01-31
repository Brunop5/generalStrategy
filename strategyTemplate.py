from abc import ABC, abstractmethod

import pandas as pd

# A general abstract class for Order and Strategy of any kind with any broker

class Order(ABC):
    side: str
    entry_price: float
    take_profit: float | None = None
    stop_loss: float | None = None
    trailing_stop_loss: float | None = None
    use_trailing: bool = False
    order_size: float

    @abstractmethod
    def place_order(self):
        pass

    @abstractmethod
    def close_order(self):
        pass

    @abstractmethod
    def check_close_conditions(self):
        pass



class Strategy(ABC):
    account_balance: float
    active_orders: list[Order]
    data: 