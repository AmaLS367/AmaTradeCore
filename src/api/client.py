import httpx
import inspect
from typing import Any, List, Optional

from ..models.market import (
    BookTicker,
    ExchangeInfo,
    Kline,
    OrderBook,
    ServerTime,
    Trade,
)


class BinanceAsyncClient:
    BASE_URL = "https://api.binance.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        headers = {}
        if api_key:
            headers["X-MBX-APIKEY"] = api_key

        self.api_secret = api_secret
        self.client = httpx.AsyncClient(
            base_url=base_url or self.BASE_URL,
            headers=headers,
            timeout=10.0,
        )

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _resolve(self, value: Any) -> Any:
        if inspect.isawaitable(value):
            return await value
        return value

    async def _get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        response = await self.client.get(path, params=params)
        await self._resolve(response.raise_for_status())
        return await self._resolve(response.json())

    async def get_server_time(self) -> ServerTime:
        return ServerTime(**await self._get("/api/v3/time"))

    async def get_exchange_info(self, symbol: Optional[str] = None) -> ExchangeInfo:
        params = {"symbol": symbol} if symbol else None
        return ExchangeInfo(**await self._get("/api/v3/exchangeInfo", params=params))

    async def get_klines(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
        startTime: Optional[int] = None,
        endTime: Optional[int] = None
    ) -> List[Kline]:
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime

        data = await self._get("/api/v3/klines", params=params)
        return [Kline.from_list(k) for k in data]

    async def get_recent_trades(self, symbol: str, limit: int = 500) -> List[Trade]:
        params = {"symbol": symbol, "limit": limit}
        data = await self._get("/api/v3/trades", params=params)
        return [Trade(**t) for t in data]

    async def get_order_book(self, symbol: str, limit: int = 100) -> OrderBook:
        params = {"symbol": symbol, "limit": limit}
        return OrderBook(**await self._get("/api/v3/depth", params=params))

    async def get_orderbook(self, symbol: str, limit: int = 100) -> OrderBook:
        return await self.get_order_book(symbol, limit=limit)

    async def get_book_ticker(self, symbol: str) -> BookTicker:
        params = {"symbol": symbol}
        return BookTicker.from_rest_payload(
            await self._get("/api/v3/ticker/bookTicker", params=params)
        )
