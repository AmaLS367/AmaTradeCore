from typing import List, Tuple
from pydantic import BaseModel, Field

class ServerTime(BaseModel):
    serverTime: int

class SymbolInfo(BaseModel):
    symbol: str
    status: str
    baseAsset: str
    quoteAsset: str
    filters: List[dict] = Field(default_factory=list)

class ExchangeInfo(BaseModel):
    timezone: str
    serverTime: int
    rateLimits: List[dict]
    symbols: List[SymbolInfo]

class Kline(BaseModel):
    open_time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: int
    quote_asset_volume: float
    number_of_trades: int
    taker_buy_base_asset_volume: float
    taker_buy_quote_asset_volume: float
    ignore: float = 0.0

    @classmethod
    def from_list(cls, data: list) -> "Kline":
        """
        Parse Binance API array format into Kline model.
        """
        return cls(
            open_time=int(data[0]),
            open=float(data[1]),
            high=float(data[2]),
            low=float(data[3]),
            close=float(data[4]),
            volume=float(data[5]),
            close_time=int(data[6]),
            quote_asset_volume=float(data[7]),
            number_of_trades=int(data[8]),
            taker_buy_base_asset_volume=float(data[9]),
            taker_buy_quote_asset_volume=float(data[10]),
            ignore=float(data[11]) if len(data) > 11 else 0.0
        )

class Trade(BaseModel):
    id: int
    price: float
    qty: float
    quoteQty: float
    time: int
    isBuyerMaker: bool
    isBestMatch: bool

class OrderBook(BaseModel):
    lastUpdateId: int
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]
