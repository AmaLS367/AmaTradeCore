from unittest.mock import AsyncMock

import pytest

from src.main import (
    CollectorConfig,
    MenuAction,
    MenuController,
    MenuState,
    StreamType,
    create_live_display,
    extract_symbol_pairs,
    should_exit_collector,
    subscribe_for_config,
)
from src.models.market import ExchangeInfo


def test_extract_symbol_pairs_filters_trading_symbols():
    exchange_info = ExchangeInfo(
        timezone="UTC",
        serverTime=1,
        rateLimits=[],
        symbols=[
            {
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "quoteAsset": "BTC",
                "filters": [],
            },
            {
                "symbol": "BTCUSDT",
                "status": "TRADING",
                "baseAsset": "BTC",
                "quoteAsset": "USDT",
                "filters": [],
            },
            {
                "symbol": "FOOBAR",
                "status": "BREAK",
                "baseAsset": "FOO",
                "quoteAsset": "BAR",
                "filters": [],
            },
        ],
    )

    assert extract_symbol_pairs(exchange_info) == ["BTCUSDT", "ETHBTC"]


def test_menu_controller_moves_selection_with_arrows():
    controller = MenuController(
        MenuState(
            config=CollectorConfig(symbol="BTCUSDT"),
            selected_index=0,
            symbols=["BTCUSDT", "ETHUSDT"],
        )
    )

    controller.handle_key("\xe0", "P")
    controller.handle_key("\xe0", "P")
    controller.handle_key("\xe0", "H")

    assert controller.state.selected_index == 1


def test_menu_controller_cycles_current_setting_values():
    controller = MenuController(
        MenuState(
            config=CollectorConfig(symbol="BTCUSDT"),
            selected_index=0,
            symbols=["BTCUSDT", "ETHUSDT"],
        )
    )

    controller.handle_key("\xe0", "M")
    assert controller.state.config.symbol == "ETHUSDT"

    controller.state.selected_index = 1
    controller.handle_key("\xe0", "M")
    assert controller.state.config.stream == StreamType.KLINES

    controller.state.selected_index = 2
    controller.handle_key("\xe0", "M")
    assert controller.state.config.interval == "5m"


def test_enter_returns_start_action_on_start_row():
    controller = MenuController(
        MenuState(
            config=CollectorConfig(symbol="BTCUSDT"),
            selected_index=5,
            symbols=["BTCUSDT", "ETHUSDT"],
        )
    )

    action = controller.handle_key("\r", None)

    assert action is MenuAction.START


def test_menu_state_can_start_from_env_default_config():
    state = MenuState(
        config=CollectorConfig(
            symbol="SOLUSDT",
            stream=StreamType.BOOK_TICKER,
            interval="5m",
            depth_limit=50,
        ),
        selected_index=0,
        symbols=["BTCUSDT", "SOLUSDT"],
    )

    assert state.config.symbol == "SOLUSDT"
    assert state.config.stream is StreamType.BOOK_TICKER


def test_create_live_display_disables_auto_refresh():
    display = create_live_display("content")

    assert display.auto_refresh is False


def test_enter_on_custom_pair_row_starts_edit_mode():
    controller = MenuController(
        MenuState(
            config=CollectorConfig(symbol="BTCUSDT"),
            selected_index=4,
            symbols=["BTCUSDT", "ETHUSDT"],
        )
    )

    action = controller.handle_key("\r", None)

    assert action is MenuAction.NONE
    assert controller.state.editing_pair is True
    assert controller.state.pair_input == ""


def test_pair_edit_mode_accepts_custom_symbol_and_appends_to_list():
    controller = MenuController(
        MenuState(
            config=CollectorConfig(symbol="BTCUSDT"),
            selected_index=4,
            symbols=["BTCUSDT", "ETHUSDT"],
        )
    )

    controller.handle_key("\r", None)
    for char in "solusdt":
        controller.handle_key(char, None)
    controller.handle_key("\r", None)

    assert controller.state.editing_pair is False
    assert controller.state.config.symbol == "SOLUSDT"
    assert "SOLUSDT" in controller.state.symbols


def test_pair_edit_mode_supports_backspace_and_escape_cancel():
    controller = MenuController(
        MenuState(
            config=CollectorConfig(symbol="BTCUSDT"),
            selected_index=4,
            symbols=["BTCUSDT", "ETHUSDT"],
        )
    )

    controller.handle_key("\r", None)
    controller.handle_key("\x08", None)
    controller.handle_key("\x1b", None)

    assert controller.state.editing_pair is False
    assert controller.state.config.symbol == "BTCUSDT"


def test_should_exit_collector_supports_q_escape_and_ctrl_c():
    assert should_exit_collector("q") is True
    assert should_exit_collector("Q") is True
    assert should_exit_collector("\x1b") is True
    assert should_exit_collector("\x03") is True
    assert should_exit_collector("a") is False


@pytest.mark.asyncio
async def test_subscribe_for_trade_config_uses_trade_subscription():
    manager = AsyncMock()
    callback = AsyncMock()
    config = CollectorConfig(symbol="BTCUSDT", stream=StreamType.TRADES)

    await subscribe_for_config(manager, config, callback)

    manager.subscribe_trades.assert_awaited_once_with("BTCUSDT", callback)


@pytest.mark.asyncio
async def test_subscribe_for_kline_config_uses_interval():
    manager = AsyncMock()
    callback = AsyncMock()
    config = CollectorConfig(symbol="BTCUSDT", stream=StreamType.KLINES, interval="15m")

    await subscribe_for_config(manager, config, callback)

    manager.subscribe_klines.assert_awaited_once_with("BTCUSDT", "15m", callback)
