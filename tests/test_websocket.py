import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest

from src.api.websocket import BinanceWebSocketManager
from src.models.market import BookTicker, DepthUpdate, Kline, Trade


class FakeWebSocket:
    def __init__(self, messages):
        self._messages = iter(messages)
        self.closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.closed = True

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._messages)
        except StopIteration as exc:
            raise StopAsyncIteration from exc

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_subscribe_trade_dispatches_typed_trade():
    callback = AsyncMock()
    manager = BinanceWebSocketManager()
    message = json.dumps(
        {
            "e": "trade",
            "E": 123456789,
            "s": "BNBBTC",
            "t": 12345,
            "p": "0.001",
            "q": "100",
            "T": 123456785,
            "m": True,
            "M": True,
        }
    )

    with patch("src.api.websocket.websockets.connect", return_value=FakeWebSocket([message])):
        await manager.subscribe_trades("BNBBTC", callback)
        await asyncio.wait_for(manager.tasks["bnbbtc@trade"], timeout=1)

    callback.assert_awaited_once()
    event = callback.await_args.args[0]
    assert isinstance(event, Trade)
    assert event.symbol == "BNBBTC"


@pytest.mark.asyncio
async def test_subscribe_kline_dispatches_typed_kline():
    callback = AsyncMock()
    manager = BinanceWebSocketManager()
    message = json.dumps(
        {
            "e": "kline",
            "E": 123456789,
            "s": "BNBBTC",
            "k": {
                "t": 1499040000000,
                "T": 1499644799999,
                "s": "BNBBTC",
                "i": "1m",
                "o": "0.01634790",
                "c": "0.01577100",
                "h": "0.80000000",
                "l": "0.01575800",
                "v": "148976.11427815",
                "n": 308,
                "q": "2434.19055334",
                "V": "1756.87402397",
                "Q": "28.46694368",
            },
        }
    )

    with patch("src.api.websocket.websockets.connect", return_value=FakeWebSocket([message])):
        await manager.subscribe_klines("BNBBTC", "1m", callback)
        await asyncio.wait_for(manager.tasks["bnbbtc@kline_1m"], timeout=1)

    event = callback.await_args.args[0]
    assert isinstance(event, Kline)
    assert event.open_time == 1499040000000


@pytest.mark.asyncio
async def test_subscribe_book_ticker_dispatches_typed_ticker():
    callback = AsyncMock()
    manager = BinanceWebSocketManager()
    message = json.dumps(
        {
            "u": 400900217,
            "s": "BNBUSDT",
            "b": "25.35190000",
            "B": "31.21000000",
            "a": "25.36520000",
            "A": "40.66000000",
        }
    )

    with patch("src.api.websocket.websockets.connect", return_value=FakeWebSocket([message])):
        await manager.subscribe_book_ticker("BNBUSDT", callback)
        await asyncio.wait_for(manager.tasks["bnbusdt@bookTicker"], timeout=1)

    event = callback.await_args.args[0]
    assert isinstance(event, BookTicker)
    assert event.symbol == "BNBUSDT"


@pytest.mark.asyncio
async def test_subscribe_depth_updates_dispatches_typed_update():
    callback = AsyncMock()
    manager = BinanceWebSocketManager()
    message = json.dumps(
        {
            "e": "depthUpdate",
            "E": 1672515782136,
            "s": "BNBBTC",
            "U": 157,
            "u": 160,
            "b": [["0.0024", "10"]],
            "a": [["0.0026", "100"]],
        }
    )

    with patch("src.api.websocket.websockets.connect", return_value=FakeWebSocket([message])):
        await manager.subscribe_depth_updates("BNBBTC", callback)
        await asyncio.wait_for(manager.tasks["bnbbtc@depth"], timeout=1)

    event = callback.await_args.args[0]
    assert isinstance(event, DepthUpdate)
    assert event.final_update_id == 160


@pytest.mark.asyncio
async def test_duplicate_subscribe_is_noop():
    callback = AsyncMock()
    manager = BinanceWebSocketManager()

    with patch.object(manager, "_create_listener_task", wraps=manager._create_listener_task) as create_task:
        await manager.subscribe_trades("BNBBTC", callback)
        await manager.subscribe_trades("BNBBTC", callback)
        manager.tasks["bnbbtc@trade"].cancel()
        with pytest.raises(asyncio.CancelledError):
            await manager.tasks["bnbbtc@trade"]

    create_task.assert_called_once()


@pytest.mark.asyncio
async def test_unsubscribe_closes_open_connection():
    callback = AsyncMock()
    manager = BinanceWebSocketManager()
    fake_socket = FakeWebSocket([])
    manager.connections["bnbbtc@trade"] = fake_socket
    manager.tasks["bnbbtc@trade"] = asyncio.create_task(asyncio.sleep(10))

    await manager.unsubscribe("bnbbtc@trade")

    assert fake_socket.closed is True
    assert "bnbbtc@trade" not in manager.connections
    assert "bnbbtc@trade" not in manager.tasks


@pytest.mark.asyncio
async def test_reconnects_after_connection_closed():
    callback = AsyncMock()
    manager = BinanceWebSocketManager(reconnect_delay=0)
    connect_calls = 0

    class TestConnectionClosed(Exception):
        pass

    async def fake_connect(_url):
        nonlocal connect_calls
        connect_calls += 1
        if connect_calls == 1:
            raise TestConnectionClosed()
        return FakeWebSocket(
            [
                json.dumps(
                    {
                        "e": "trade",
                        "E": 123456789,
                        "s": "BNBBTC",
                        "t": 12345,
                        "p": "0.001",
                        "q": "100",
                        "T": 123456785,
                        "m": True,
                        "M": True,
                    }
                )
            ]
        )

    with patch("src.api.websocket.websockets.connect", side_effect=fake_connect), patch(
        "src.api.websocket.websockets.exceptions.ConnectionClosed", TestConnectionClosed
    ):
        await manager.subscribe_trades("BNBBTC", callback)
        await asyncio.wait_for(manager.tasks["bnbbtc@trade"], timeout=1)

    assert connect_calls == 2
    callback.assert_awaited_once()
