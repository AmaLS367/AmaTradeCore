import asyncio
import os
import sys
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable, Deque, Optional

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .api.client import BinanceAsyncClient
from .api.websocket import BinanceWebSocketManager
from .models.market import BookTicker, DepthUpdate, ExchangeInfo, Kline, OrderBook, Trade

COMMON_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KLINE_INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]
DEPTH_LIMITS = [5, 10, 20, 50, 100]
MAX_EVENTS = 12


class StreamType(str, Enum):
    TRADES = "trades"
    KLINES = "klines"
    BOOK_TICKER = "book_ticker"
    DEPTH_UPDATES = "depth_updates"

    @property
    def label(self) -> str:
        return {
            StreamType.TRADES: "Trades",
            StreamType.KLINES: "Klines",
            StreamType.BOOK_TICKER: "Best Bid/Ask",
            StreamType.DEPTH_UPDATES: "Depth Updates",
        }[self]


class MenuAction(Enum):
    NONE = "none"
    START = "start"
    QUIT = "quit"


@dataclass
class CollectorConfig:
    symbol: str
    stream: StreamType = StreamType.TRADES
    interval: str = "1m"
    depth_limit: int = 20


@dataclass
class MenuState:
    config: CollectorConfig
    selected_index: int
    symbols: list[str]
    intervals: list[str] = field(default_factory=lambda: list(KLINE_INTERVALS))
    depth_limits: list[int] = field(default_factory=lambda: list(DEPTH_LIMITS))


def extract_symbol_pairs(exchange_info: ExchangeInfo) -> list[str]:
    trading_symbols = [
        symbol.symbol
        for symbol in exchange_info.symbols
        if symbol.status == "TRADING"
    ]
    return sorted(trading_symbols, key=lambda value: (not value.endswith("USDT"), value))


class MenuController:
    def __init__(self, state: MenuState):
        self.state = state

    def handle_key(self, key: str, extended_key: Optional[str] = None) -> MenuAction:
        if key in ("\x00", "\xe0"):
            return self._handle_arrow(extended_key)
        if key == "\r":
            return self._activate_selected()
        if key.lower() == "q":
            return MenuAction.QUIT
        return MenuAction.NONE

    def _handle_arrow(self, extended_key: Optional[str]) -> MenuAction:
        if extended_key == "H":
            self.state.selected_index = (self.state.selected_index - 1) % 6
        elif extended_key == "P":
            self.state.selected_index = (self.state.selected_index + 1) % 6
        elif extended_key == "K":
            self._cycle_current(-1)
        elif extended_key == "M":
            self._cycle_current(1)
        return MenuAction.NONE

    def _activate_selected(self) -> MenuAction:
        if self.state.selected_index == 4:
            return MenuAction.START
        if self.state.selected_index == 5:
            return MenuAction.QUIT
        return MenuAction.NONE

    def _cycle_current(self, direction: int) -> None:
        index = self.state.selected_index
        if index == 0:
            self.state.config.symbol = _cycle_value(
                self.state.symbols,
                self.state.config.symbol,
                direction,
            )
        elif index == 1:
            self.state.config.stream = _cycle_value(
                list(StreamType),
                self.state.config.stream,
                direction,
            )
        elif index == 2:
            self.state.config.interval = _cycle_value(
                self.state.intervals,
                self.state.config.interval,
                direction,
            )
        elif index == 3:
            self.state.config.depth_limit = _cycle_value(
                self.state.depth_limits,
                self.state.config.depth_limit,
                direction,
            )


def _cycle_value(options: list[Any], current: Any, direction: int) -> Any:
    current_index = options.index(current)
    next_index = (current_index + direction) % len(options)
    return options[next_index]


def render_menu(state: MenuState) -> Panel:
    table = Table.grid(expand=True)
    table.add_column(ratio=1)
    table.add_column(ratio=1)

    rows = [
        ("Pair", state.config.symbol),
        ("Stream", state.config.stream.label),
        ("Interval", state.config.interval),
        ("Depth Limit", str(state.config.depth_limit)),
        ("Start Collector", "Press Enter"),
        ("Quit", "Press Enter or q"),
    ]

    for index, (label, value) in enumerate(rows):
        style = "bold black on cyan" if index == state.selected_index else ""
        table.add_row(Text(label, style=style), Text(value, style=style))

    instructions = Text(
        "Arrows: Up/Down move, Left/Right change value, Enter select, q quit",
        style="dim",
    )
    return Panel(
        Group(table, instructions),
        title="AmaTradeCore Collector Setup",
        border_style="cyan",
    )


def render_collector(
    config: CollectorConfig,
    events: Deque[str],
    status: str,
    snapshot: Optional[OrderBook | BookTicker],
) -> Panel:
    table = Table(expand=True)
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    table.add_row("Pair", config.symbol)
    table.add_row("Stream", config.stream.label)
    if config.stream is StreamType.KLINES:
        table.add_row("Interval", config.interval)
    if config.stream is StreamType.DEPTH_UPDATES:
        table.add_row("Depth Limit", str(config.depth_limit))
    table.add_row("Status", status)

    if snapshot is not None:
        if isinstance(snapshot, OrderBook) and snapshot.bids and snapshot.asks:
            table.add_row("Snapshot", f"bid {snapshot.bids[0]} | ask {snapshot.asks[0]}")
        elif isinstance(snapshot, BookTicker):
            table.add_row(
                "Snapshot",
                f"bid {snapshot.bid_price}/{snapshot.bid_qty} | ask {snapshot.ask_price}/{snapshot.ask_qty}",
            )

    event_table = Table(expand=True)
    event_table.add_column("Latest Events", style="green")
    if events:
        for event in events:
            event_table.add_row(event)
    else:
        event_table.add_row("Waiting for data...")

    return Panel(
        Group(table, event_table, Text("Press q to stop collector", style="dim")),
        title="Live Collector",
        border_style="green",
    )


def format_event(event: Trade | Kline | BookTicker | DepthUpdate) -> str:
    if isinstance(event, Trade):
        return f"TRADE {event.symbol} price={event.price} qty={event.qty}"
    if isinstance(event, Kline):
        return (
            f"KLINE {event.symbol} {event.interval} "
            f"o={event.open} h={event.high} l={event.low} c={event.close}"
        )
    if isinstance(event, BookTicker):
        return (
            f"TICKER {event.symbol} "
            f"bid={event.bid_price}/{event.bid_qty} ask={event.ask_price}/{event.ask_qty}"
        )
    return (
        f"DEPTH {event.symbol} "
        f"u={event.first_update_id}-{event.final_update_id} "
        f"bids={len(event.bids)} asks={len(event.asks)}"
    )


async def subscribe_for_config(
    manager: BinanceWebSocketManager,
    config: CollectorConfig,
    callback: Callable[[Any], Awaitable[None]],
) -> None:
    if config.stream is StreamType.TRADES:
        await manager.subscribe_trades(config.symbol, callback)
    elif config.stream is StreamType.KLINES:
        await manager.subscribe_klines(config.symbol, config.interval, callback)
    elif config.stream is StreamType.BOOK_TICKER:
        await manager.subscribe_book_ticker(config.symbol, callback)
    else:
        await manager.subscribe_depth_updates(config.symbol, callback)


async def fetch_symbols() -> list[str]:
    try:
        async with BinanceAsyncClient() as client:
            exchange_info = await client.get_exchange_info()
    except Exception:
        return list(COMMON_SYMBOLS)

    symbols = extract_symbol_pairs(exchange_info)
    return symbols or list(COMMON_SYMBOLS)


async def fetch_snapshot(config: CollectorConfig) -> Optional[OrderBook | BookTicker]:
    async with BinanceAsyncClient() as client:
        if config.stream is StreamType.DEPTH_UPDATES:
            return await client.get_order_book(config.symbol, limit=config.depth_limit)
        if config.stream is StreamType.BOOK_TICKER:
            return await client.get_book_ticker(config.symbol)
    return None


async def run_collector(config: CollectorConfig, console: Console) -> None:
    events: Deque[str] = deque(maxlen=MAX_EVENTS)
    status = "Connecting"
    try:
        snapshot = await fetch_snapshot(config)
    except Exception as exc:
        snapshot = None
        status = f"Snapshot failed: {exc}"

    async def on_event(event: Any) -> None:
        nonlocal status
        status = "Streaming"
        events.appendleft(format_event(event))

    manager = BinanceWebSocketManager()
    try:
        await subscribe_for_config(manager, config, on_event)
        with Live(
            render_collector(config, events, status, snapshot),
            console=console,
            refresh_per_second=10,
        ) as live:
            while True:
                live.update(render_collector(config, events, status, snapshot))
                key, _ = await asyncio.to_thread(read_key)
                if key.lower() == "q" or key == "\x1b":
                    break
    finally:
        await manager.unsubscribe_all()


async def cli() -> int:
    console = Console()
    symbols = await fetch_symbols()
    state = MenuState(
        config=CollectorConfig(symbol=symbols[0]),
        selected_index=0,
        symbols=symbols,
    )
    controller = MenuController(state)

    with Live(render_menu(state), console=console, refresh_per_second=12) as live:
        while True:
            live.update(render_menu(state))
            key, extended_key = await asyncio.to_thread(read_key)
            action = controller.handle_key(key, extended_key)
            if action is MenuAction.START:
                live.stop()
                console.clear()
                await run_collector(state.config, console)
                console.clear()
                live.start()
            elif action is MenuAction.QUIT:
                return 0


def read_key() -> tuple[str, Optional[str]]:
    if os.name == "nt":
        import msvcrt

        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            return key, msvcrt.getwch()
        return key, None

    import termios
    import tty

    fd = sys.stdin.fileno()
    original = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == "\x1b":
            next_char = sys.stdin.read(1)
            if next_char == "[":
                final_char = sys.stdin.read(1)
                mapping = {"A": "H", "B": "P", "C": "M", "D": "K"}
                return "\xe0", mapping.get(final_char)
        return key, None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original)


def main() -> None:
    raise SystemExit(asyncio.run(cli()))
