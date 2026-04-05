import httpx
from typing import List, Optional
from amatradecore.models.market import ServerTime, ExchangeInfo, Kline, Trade, OrderBook

class BinanceAsyncClient:
    BASE_URL = "https://api.binance.com"

    def __init__(self, api_key: Optional[str] = None):
        headers = {}
        if api_key:
            headers["X-MBX-APIKEY"] = api_key
        
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=headers,
            timeout=10.0
        )

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_server_time(self) -> ServerTime:
        """Fetch server time from /api/v3/time"""
        response = await self.client.get("/api/v3/time")
        response.raise_for_status()
        return ServerTime(**response.json())

    async def get_exchange_info(self, symbol: Optional[str] = None) -> ExchangeInfo:
        """Fetch exchange info from /api/v3/exchangeInfo"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        response = await self.client.get("/api/v3/exchangeInfo", params=params)
        response.raise_for_status()
        return ExchangeInfo(**response.json())

    async def get_klines(
        self, 
        symbol: str, 
        interval: str, 
        limit: int = 500, 
        startTime: Optional[int] = None, 
        endTime: Optional[int] = None
    ) -> List[Kline]:
        """Fetch klines from /api/v3/klines"""
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime
            
        response = await self.client.get("/api/v3/klines", params=params)
        response.raise_for_status()
        data = response.json()
        return [Kline.from_list(k) for k in data]

    async def get_recent_trades(self, symbol: str, limit: int = 500) -> List[Trade]:
        """Fetch recent trades from /api/v3/trades"""
        params = {"symbol": symbol, "limit": limit}
        response = await self.client.get("/api/v3/trades", params=params)
        response.raise_for_status()
        data = response.json()
        return [Trade(**t) for t in data]

    async def get_orderbook(self, symbol: str, limit: int = 100) -> OrderBook:
        """Fetch order book from /api/v3/depth"""
        params = {"symbol": symbol, "limit": limit}
        response = await self.client.get("/api/v3/depth", params=params)
        response.raise_for_status()
        return OrderBook(**response.json())
