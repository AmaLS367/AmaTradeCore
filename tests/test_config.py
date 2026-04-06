from src.config import AppConfig, create_collector_config, load_config
from src.main import StreamType


def test_load_config_reads_binance_env(monkeypatch):
    monkeypatch.setenv("BINANCE_API_KEY", "key-123")
    monkeypatch.setenv("BINANCE_API_SECRET", "secret-456")
    monkeypatch.setenv("BINANCE_BASE_URL", "https://testnet.binance.vision")
    monkeypatch.setenv("BINANCE_WS_URL", "wss://stream.testnet.binance.vision/ws")
    monkeypatch.setenv("DEFAULT_SYMBOL", "ETHUSDT")
    monkeypatch.setenv("DEFAULT_STREAM", "klines")
    monkeypatch.setenv("DEFAULT_INTERVAL", "15m")
    monkeypatch.setenv("DEFAULT_DEPTH_LIMIT", "50")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    config = load_config()

    assert config.binance_api_key == "key-123"
    assert config.binance_api_secret == "secret-456"
    assert config.binance_base_url == "https://testnet.binance.vision"
    assert config.binance_ws_url == "wss://stream.testnet.binance.vision/ws"
    assert config.default_symbol == "ETHUSDT"
    assert config.default_stream == "klines"
    assert config.default_interval == "15m"
    assert config.default_depth_limit == 50
    assert config.log_level == "DEBUG"


def test_create_collector_config_uses_env_defaults():
    config = AppConfig.model_construct(
        binance_api_key="",
        binance_api_secret="",
        binance_base_url="https://api.binance.com",
        binance_ws_url="wss://stream.binance.com:9443/ws",
        default_symbol="SOLUSDT",
        default_stream="book_ticker",
        default_interval="5m",
        default_depth_limit=100,
        log_level="INFO",
    )

    collector_config = create_collector_config(config)

    assert collector_config.symbol == "SOLUSDT"
    assert collector_config.stream is StreamType.BOOK_TICKER
    assert collector_config.interval == "5m"
    assert collector_config.depth_limit == 100
