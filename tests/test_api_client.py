import pytest
from unittest.mock import AsyncMock, patch
from amatradecore.api.client import BinanceAsyncClient
from amatradecore.models.market import ServerTime, ExchangeInfo, Kline, Trade, OrderBook

@pytest.fixture
def client():
    return BinanceAsyncClient()

@pytest.mark.asyncio
async def test_get_server_time(client):
    mock_response = AsyncMock()
    mock_response.json.return_value = {"serverTime": 1618900000000}
    mock_response.raise_for_status = AsyncMock()

    with patch('httpx.AsyncClient.get', return_value=mock_response) as mock_get:
        server_time = await client.get_server_time()
        
        mock_get.assert_called_once_with("/api/v3/time")
        assert isinstance(server_time, ServerTime)
        assert server_time.serverTime == 1618900000000

@pytest.mark.asyncio
async def test_get_exchange_info(client):
    mock_data = {
        "timezone": "UTC",
        "serverTime": 1618900000000,
        "rateLimits": [],
        "symbols": [
            {
                "symbol": "BTCUSDT",
                "status": "TRADING",
                "baseAsset": "BTC",
                "quoteAsset": "USDT",
                "filters": [{"filterType": "PRICE_FILTER"}]
            }
        ]
    }
    mock_response = AsyncMock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status = AsyncMock()

    with patch('httpx.AsyncClient.get', return_value=mock_response) as mock_get:
        exchange_info = await client.get_exchange_info("BTCUSDT")
        
        mock_get.assert_called_once_with("/api/v3/exchangeInfo", params={"symbol": "BTCUSDT"})
        assert isinstance(exchange_info, ExchangeInfo)
        assert len(exchange_info.symbols) == 1
        assert exchange_info.symbols[0].symbol == "BTCUSDT"

@pytest.mark.asyncio
async def test_get_klines(client):
    mock_data = [
        [
            1499040000000, "0.01634790", "0.80000000", "0.01575800", "0.01577100",
            "148976.11427815", 1499644799999, "2434.19055334", 308,
            "1756.87402397", "28.46694368", "0"
        ]
    ]
    mock_response = AsyncMock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status = AsyncMock()

    with patch('httpx.AsyncClient.get', return_value=mock_response) as mock_get:
        klines = await client.get_klines("BTCUSDT", "1m", limit=1)
        
        mock_get.assert_called_once_with("/api/v3/klines", params={"symbol": "BTCUSDT", "interval": "1m", "limit": 1})
        assert isinstance(klines, list)
        assert len(klines) == 1
        assert isinstance(klines[0], Kline)
        assert klines[0].open_time == 1499040000000
        assert klines[0].open == 0.01634790
