import json
import asyncio
import logging
import websockets
from typing import Callable, Awaitable, Dict, Any, Optional

logger = logging.getLogger(__name__)

class BinanceWebSocketManager:
    BASE_URL = "wss://stream.binance.com:9443/ws"

    def __init__(self):
        self.connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.tasks: Dict[str, asyncio.Task] = {}

    async def subscribe(self, stream_name: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]):
        """
        Subscribe to a specific stream. 
        Example stream_names: 'btcusdt@kline_1m', 'btcusdt@trade', 'btcusdt@depth'
        """
        if stream_name in self.tasks:
            logger.warning(f"Already subscribed to {stream_name}")
            return

        url = f"{self.BASE_URL}/{stream_name}"
        task = asyncio.create_task(self._listen(url, stream_name, callback))
        self.tasks[stream_name] = task
        logger.info(f"Subscribed to {stream_name}")

    async def unsubscribe(self, stream_name: str):
        """Unsubscribe from a specific stream and close connection."""
        if stream_name in self.tasks:
            self.tasks[stream_name].cancel()
            del self.tasks[stream_name]
            
        if stream_name in self.connections:
            await self.connections[stream_name].close()
            del self.connections[stream_name]
            
        logger.info(f"Unsubscribed from {stream_name}")

    async def unsubscribe_all(self):
        """Unsubscribe from all active streams."""
        streams = list(self.tasks.keys())
        for stream in streams:
            await self.unsubscribe(stream)

    async def _listen(self, url: str, stream_name: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]):
        while True:
            try:
                async with websockets.connect(url) as ws:
                    self.connections[stream_name] = ws
                    logger.info(f"Connected to {url}")
                    async for message in ws:
                        try:
                            data = json.loads(message)
                            await callback(data)
                        except Exception as e:
                            logger.error(f"Error processing message from {stream_name}: {e}")
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Connection closed for {stream_name}, reconnecting in 5s...")
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                logger.info(f"Listener task cancelled for {stream_name}")
                break
            except Exception as e:
                logger.error(f"WebSocket error on {stream_name}: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)
