from abc import ABC, abstractmethod
import importlib
import json
import os

import pandas as pd

# A general abstract class for Order and Strategy of any kind with any broker

class Order(ABC):
    side: str
    entry_price: float
    take_profit: float | None
    stop_loss: float | None
    trailing_stop_loss: float | None
    use_trailing: bool
    order_size: float

    def __init__(self, 
        side, 
        entry_price, 
        order_size, 
        take_profit=None,
        stop_loss=None,
        trailing_stop_loss=None,
        use_trailing=False,
    ):
        self.side = side
        self.take_profit = take_profit
        self.entry_price = entry_price
        self.stop_loss = stop_loss
        self.trailing_stop_loss = trailing_stop_loss
        self.use_trailing = use_trailing
        self.order_size = order_size

    @abstractmethod
    def place_order(self):
        pass

    @abstractmethod
    def close_order(self):
        pass

    @abstractmethod
    def check_close_conditions(self, log=print, **kwargs) -> bool:
        """
        returns True if the conditions were met and the order was closed
        """
        pass



class Strategy(ABC):
    account_balance: float
    active_orders: list[Order]
    data: pd.DataFrame | None

    def __init__(self):
        self.load_metadata()
        self.data = self.gather_data()


    def _serialize(self, value, csv_filename: str):
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value

        if isinstance(value, pd.DataFrame):
            return {"__type__": "dataframe_csv", "path": csv_filename}

        if isinstance(value, dict):
            return {key: self._serialize(val, csv_filename) for key, val in value.items()}

        if isinstance(value, list):
            return [self._serialize(item, csv_filename) for item in value]

        if isinstance(value, tuple):
            return {
                "__type__": "tuple",
                "items": [self._serialize(item, csv_filename) for item in value],
            }

        if isinstance(value, set):
            return {
                "__type__": "set",
                "items": [self._serialize(item, csv_filename) for item in value],
            }

        if isinstance(value, Order) or hasattr(value, "__dict__"):
            class_path = f"{value.__class__.__module__}.{value.__class__.__name__}"
            return {
                "__type__": "object",
                "class": class_path,
                "state": self._serialize(value.__dict__, csv_filename),
            }

        return {"__type__": "repr", "value": repr(value)}

    def _deserialize(self, value):
        if isinstance(value, list):
            return [self._deserialize(item) for item in value]

        if not isinstance(value, dict):
            return value

        value_type = value.get("__type__")
        if value_type == "dataframe_csv":
            path = value.get("path")
            if path and os.path.exists(path):
                return pd.read_csv(path)
            return pd.DataFrame()

        if value_type == "tuple":
            return tuple(self._deserialize(item) for item in value.get("items", []))

        if value_type == "set":
            return set(self._deserialize(item) for item in value.get("items", []))

        if value_type == "object":
            class_path = value.get("class")
            state = self._deserialize(value.get("state", {}))
            try:
                module_name, class_name = class_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                cls = getattr(module, class_name)
                instance = cls.__new__(cls)
                if isinstance(state, dict):
                    for key, val in state.items():
                        setattr(instance, key, val)
                return instance
            except Exception:
                return {"__unresolved_class__": class_path, "state": state}

        if value_type == "repr":
            return value.get("value")

        return {key: self._deserialize(val) for key, val in value.items()}

    def save_data(self, csv_filename: str, metadata_filename: str) -> None:
        """
        Saves information about current strategy to a json file,
        also saves the self.data into a csv
        """
        if isinstance(getattr(self, "data", None), pd.DataFrame):
            self.data.to_csv(csv_filename, index=False)

        payload = {
            key: self._serialize(val, csv_filename)
            for key, val in self.__dict__.items()
        }

        if "data" in payload:
            payload["data"] = {"__type__": "dataframe_csv", "path": csv_filename}

        with open(metadata_filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def load_metadata(self, filename: str) -> None:
        """
        Loads metadata of a strategy from a json file, fills a new object with it
        """
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as f:
            payload = json.load(f)

        for key, val in payload.items():
            setattr(self, key, self._deserialize(val))


    @abstractmethod
    def gather_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def fetch_new_data(self) -> None:
        """
        updates self.data with one row of new fetched data
        """
        pass

    @abstractmethod
    def update_indicators(self):
        """
        Updates the indicators deciding if a trade should be made
        """
        pass

    @abstractmethod
    def calculate_order_size(self, **kwargs):
        """
        Calculates the order size based on broker requirements 
        and maybe some oether specifications
        """
        pass

    @abstractmethod
    def entry_logic(self):
        """
        A complete entry logic of the strategy.
        Should create an Order object and add it to active_orders if conditions are met
        """
        pass

    @abstractmethod
    def run(self):
        """
        Starts running the strategy. Due to the generalisation this can mean connection to websocket
        for depth data, starting multiple threads for price gathering, just getting ohlcv data every 
        15mins or anything else.
        """
        pass
