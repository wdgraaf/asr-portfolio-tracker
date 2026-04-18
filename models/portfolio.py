"""Stores the user's assets and does basic calculations like total value."""

import json
from pathlib import Path


class Portfolio:
    DATA_PATH = Path("data/portfolio.json")

    def __init__(self) -> None:
        self.assets: list[dict] = []
        self._load()

    def add_asset(
        self,
        ticker: str,
        sector: str,
        asset_class: str,
        quantity: float,
        purchase_price: float,
    ) -> dict:
        asset = {
            "ticker": ticker.upper(),
            "sector": sector,
            "asset_class": asset_class,
            "quantity": quantity,
            "purchase_price": purchase_price,
        }
        self.assets.append(asset)
        self._save()
        return asset

    def remove_asset(self, ticker: str) -> None:
        self.assets = [a for a in self.assets if a["ticker"] != ticker.upper()]
        self._save()

    def get_assets(self) -> list[dict]:
        return self.assets

    def calculate_transaction_value(self, asset: dict) -> float:
        return asset["quantity"] * asset["purchase_price"]

    def calculate_current_value(self, asset: dict, current_price: float) -> float:
        return asset["quantity"] * current_price

    def total_portfolio_value(self, current_prices: dict[str, float]) -> float:
        return sum(
            self.calculate_current_value(a, current_prices[a["ticker"]])
            for a in self.assets
            if a["ticker"] in current_prices
        )

    def get_weights_by(
        self, field: str, current_prices: dict[str, float]
    ) -> dict[str, float]:
        total = self.total_portfolio_value(current_prices)
        if total == 0:
            return {}
        weights: dict[str, float] = {}
        for asset in self.assets:
            if asset["ticker"] not in current_prices:
                continue
            key = asset[field]
            value = self.calculate_current_value(asset, current_prices[asset["ticker"]])
            weights[key] = weights.get(key, 0.0) + (value / total) * 100
        return weights

    def _load(self) -> None:
        if self.DATA_PATH.exists():
            with open(self.DATA_PATH) as f:
                self.assets = json.load(f)

    def _save(self) -> None:
        self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(self.DATA_PATH, "w") as f:
            json.dump(self.assets, f, indent=2)
