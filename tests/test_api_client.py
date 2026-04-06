import pytest
from unittest.mock import AsyncMock, patch

from src.api.client import BinanceAsyncClient
from src.models.market import (
    BookTicker,
    ExchangeInfo,
    Kline,
    OrderBook,
    ServerTime,
    Trade,
)


@pytest.fixture
def client():
    return BinanceAsyncClient()


def test_client_uses_configured_base_url_and_api_key():
    client = BinanceAsyncClient(
        api_key="key-123",
        api_secret="secret-456",
        base_url="https://testnet.binance.vision",
    )

    assert str(client.client.base_url) == "https://testnet.binance.vision"
    assert client.client.headers["X-MBX-APIKEY"] == "key-123"
    assert client.api_secret == "secret-456"


@pytest.mark.asyncio
async def test_get_server_time(client):
    mock_response = AsyncMock()
    mock_response.json.return_value = {"serverTime": 1618900000000}
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        server_time = await client.get_server_time()

    mock_get.assert_called_once_with("/api/v3/time", params=None)
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
                "filters": [{"filterType": "PRICE_FILTER"}],
            }
        ],
    }
    mock_response = AsyncMock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        exchange_info = await client.get_exchange_info("BTCUSDT")

    mock_get.assert_called_once_with(
        "/api/v3/exchangeInfo", params={"symbol": "BTCUSDT"}
    )
    assert isinstance(exchange_info, ExchangeInfo)
    assert len(exchange_info.symbols) == 1
    assert exchange_info.symbols[0].symbol == "BTCUSDT"


@pytest.mark.asyncio
async def test_get_klines(client):
    mock_data = [
        [
            1499040000000,
            "0.01634790",
            "0.80000000",
            "0.01575800",
            "0.01577100",
            "148976.11427815",
            1499644799999,
            "2434.19055334",
            308,
            "1756.87402397",
            "28.46694368",
            "0",
        ]
    ]
    mock_response = AsyncMock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        klines = await client.get_klines("BTCUSDT", "1m", limit=1)

    mock_get.assert_called_once_with(
        "/api/v3/klines", params={"symbol": "BTCUSDT", "interval": "1m", "limit": 1}
    )
    assert isinstance(klines, list)
    assert len(klines) == 1
    assert isinstance(klines[0], Kline)
    assert klines[0].open_time == 1499040000000
    assert klines[0].open == 0.01634790


@pytest.mark.asyncio
async def test_get_recent_trades(client):
    mock_response = AsyncMock()
    mock_response.json.return_value = [
        {
            "id": 28457,
            "price": "4.00000100",
            "qty": "12.00000000",
            "quoteQty": "48.000012",
            "time": 1499865549590,
            "isBuyerMaker": True,
            "isBestMatch": True,
        }
    ]
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        trades = await client.get_recent_trades("BTCUSDT", limit=1)

    mock_get.assert_called_once_with(
        "/api/v3/trades", params={"symbol": "BTCUSDT", "limit": 1}
    )
    assert len(trades) == 1
    assert isinstance(trades[0], Trade)
    assert trades[0].price == 4.000001


@pytest.mark.asyncio
async def test_get_order_book(client):
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "lastUpdateId": 1027024,
        "bids": [["4.00000000", "431.00000000"]],
        "asks": [["4.00000200", "12.00000000"]],
    }
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        order_book = await client.get_order_book("BTCUSDT", limit=5)

    mock_get.assert_called_once_with(
        "/api/v3/depth", params={"symbol": "BTCUSDT", "limit": 5}
    )
    assert isinstance(order_book, OrderBook)
    assert order_book.bids[0] == (4.0, 431.0)


@pytest.mark.asyncio
async def test_get_book_ticker(client):
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "symbol": "BTCUSDT",
        "bidPrice": "4.00000000",
        "bidQty": "431.00000000",
        "askPrice": "4.00000200",
        "askQty": "12.00000000",
    }
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        book_ticker = await client.get_book_ticker("BTCUSDT")

    mock_get.assert_called_once_with(
        "/api/v3/ticker/bookTicker", params={"symbol": "BTCUSDT"}
    )
    assert isinstance(book_ticker, BookTicker)
    assert book_ticker.ask_price == 4.000002
