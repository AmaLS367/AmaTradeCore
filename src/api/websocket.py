import asyncio
import inspect
import json
import logging
from contextlib import suppress
from typing import Any, Awaitable, Callable, Dict

import websockets

from ..models.market import BookTicker, DepthUpdate, Kline, Trade

logger = logging.getLogger(__name__)


class BinanceWebSocketManager:
    BASE_URL = "wss://stream.binance.com:9443/ws"

    def __init__(self, reconnect_delay: float = 5.0):
        self.connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.tasks: Dict[str, asyncio.Task] = {}
        self.reconnect_delay = reconnect_delay

    async def subscribe(
        self,
        stream_name: str,
        callback: Callable[[Any], Awaitable[None]],
        parser: Callable[[dict], Any],
    ):
        if stream_name in self.tasks:
            logger.warning(f"Already subscribed to {stream_name}")
            return

        self.tasks[stream_name] = self._create_listener_task(stream_name, callback, parser)
        logger.info(f"Subscribed to {stream_name}")

    async def subscribe_trades(
        self,
        symbol: str,
        callback: Callable[[Trade], Awaitable[None]],
    ):
        await self.subscribe(f"{symbol.lower()}@trade", callback, Trade.from_stream_payload)

    async def subscribe_klines(
        self,
        symbol: str,
        interval: str,
        callback: Callable[[Kline], Awaitable[None]],
    ):
        await self.subscribe(
            f"{symbol.lower()}@kline_{interval}",
            callback,
            Kline.from_stream_payload,
        )

    async def subscribe_book_ticker(
        self,
        symbol: str,
        callback: Callable[[BookTicker], Awaitable[None]],
    ):
        await self.subscribe(
            f"{symbol.lower()}@bookTicker",
            callback,
            BookTicker.from_stream_payload,
        )

    async def subscribe_depth_updates(
        self,
        symbol: str,
        callback: Callable[[DepthUpdate], Awaitable[None]],
    ):
        await self.subscribe(
            f"{symbol.lower()}@depth",
            callback,
            DepthUpdate.from_stream_payload,
        )

    async def unsubscribe(self, stream_name: str):
        if stream_name in self.tasks:
            task = self.tasks.pop(stream_name)
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

        if stream_name in self.connections:
            await self.connections[stream_name].close()
            del self.connections[stream_name]

        logger.info(f"Unsubscribed from {stream_name}")

    async def unsubscribe_all(self):
        streams = list(self.tasks.keys())
        for stream in streams:
            await self.unsubscribe(stream)

    def _create_listener_task(
        self,
        stream_name: str,
        callback: Callable[[Any], Awaitable[None]],
        parser: Callable[[dict], Any],
    ) -> asyncio.Task:
        url = f"{self.BASE_URL}/{stream_name}"
        return asyncio.create_task(self._listen(url, stream_name, callback, parser))

    async def _listen(
        self,
        url: str,
        stream_name: str,
        callback: Callable[[Any], Awaitable[None]],
        parser: Callable[[dict], Any],
    ):
        while True:
            try:
                connection = websockets.connect(url)
                if inspect.isawaitable(connection):
                    connection = await connection

                async with connection as ws:
                    self.connections[stream_name] = ws
                    logger.info(f"Connected to {url}")
                    async for message in ws:
                        try:
                            await callback(parser(json.loads(message)))
                        except Exception as e:
                            logger.error(f"Error processing message from {stream_name}: {e}")
                    break
            except websockets.exceptions.ConnectionClosed:
                logger.warning(
                    f"Connection closed for {stream_name}, reconnecting in {self.reconnect_delay}s..."
                )
                await asyncio.sleep(self.reconnect_delay)
            except asyncio.CancelledError:
                logger.info(f"Listener task cancelled for {stream_name}")
                break
            except Exception as e:
                logger.error(
                    f"WebSocket error on {stream_name}: {e}. Reconnecting in {self.reconnect_delay}s..."
                )
                await asyncio.sleep(self.reconnect_delay)
            finally:
                self.connections.pop(stream_name, None)
