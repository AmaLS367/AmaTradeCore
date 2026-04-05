from typing import List, Optional, Tuple
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
    symbol: Optional[str] = None
    interval: Optional[str] = None
    ignore: float = 0.0

    @classmethod
    def from_list(cls, data: list) -> "Kline":
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

    @classmethod
    def from_stream_payload(cls, payload: dict) -> "Kline":
        kline = payload["k"]
        return cls(
            open_time=int(kline["t"]),
            open=float(kline["o"]),
            high=float(kline["h"]),
            low=float(kline["l"]),
            close=float(kline["c"]),
            volume=float(kline["v"]),
            close_time=int(kline["T"]),
            quote_asset_volume=float(kline["q"]),
            number_of_trades=int(kline["n"]),
            taker_buy_base_asset_volume=float(kline["V"]),
            taker_buy_quote_asset_volume=float(kline["Q"]),
            symbol=kline.get("s") or payload.get("s"),
            interval=kline.get("i"),
        )


class Trade(BaseModel):
    id: int
    price: float
    qty: float
    quoteQty: float
    time: int
    isBuyerMaker: bool
    isBestMatch: bool
    symbol: Optional[str] = None
    event_time: Optional[int] = None

    @classmethod
    def from_stream_payload(cls, payload: dict) -> "Trade":
        return cls(
            id=int(payload["t"]),
            price=float(payload["p"]),
            qty=float(payload["q"]),
            quoteQty=float(payload.get("p", 0.0)) * float(payload["q"]),
            time=int(payload["T"]),
            isBuyerMaker=bool(payload["m"]),
            isBestMatch=bool(payload.get("M", True)),
            symbol=payload.get("s"),
            event_time=payload.get("E"),
        )


class OrderBook(BaseModel):
    lastUpdateId: int
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]


class BookTicker(BaseModel):
    symbol: str
    bid_price: float
    bid_qty: float
    ask_price: float
    ask_qty: float
    update_id: Optional[int] = None

    @classmethod
    def from_rest_payload(cls, payload: dict) -> "BookTicker":
        return cls(
            symbol=payload["symbol"],
            bid_price=float(payload["bidPrice"]),
            bid_qty=float(payload["bidQty"]),
            ask_price=float(payload["askPrice"]),
            ask_qty=float(payload["askQty"]),
        )

    @classmethod
    def from_stream_payload(cls, payload: dict) -> "BookTicker":
        return cls(
            symbol=payload["s"],
            bid_price=float(payload["b"]),
            bid_qty=float(payload["B"]),
            ask_price=float(payload["a"]),
            ask_qty=float(payload["A"]),
            update_id=int(payload["u"]),
        )


class DepthUpdate(BaseModel):
    symbol: str
    event_time: int
    first_update_id: int
    final_update_id: int
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]

    @classmethod
    def from_stream_payload(cls, payload: dict) -> "DepthUpdate":
        return cls(
            symbol=payload["s"],
            event_time=int(payload["E"]),
            first_update_id=int(payload["U"]),
            final_update_id=int(payload["u"]),
            bids=payload["b"],
            asks=payload["a"],
        )
