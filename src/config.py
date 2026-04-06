from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import (
    DotEnvSettingsSource,
    EnvSettingsSource,
    InitSettingsSource,
    PydanticBaseSettingsSource,
)


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    binance_api_key: str = Field(default="", validation_alias="BINANCE_API_KEY")
    binance_api_secret: str = Field(default="", validation_alias="BINANCE_API_SECRET")
    binance_base_url: str = Field(
        default="https://api.binance.com",
        validation_alias="BINANCE_BASE_URL",
    )
    binance_ws_url: str = Field(
        default="wss://stream.binance.com:9443/ws",
        validation_alias="BINANCE_WS_URL",
    )
    default_symbol: str = Field(default="BTCUSDT", validation_alias="DEFAULT_SYMBOL")
    default_stream: str = Field(default="trades", validation_alias="DEFAULT_STREAM")
    default_interval: str = Field(default="1m", validation_alias="DEFAULT_INTERVAL")
    default_depth_limit: int = Field(default=20, validation_alias="DEFAULT_DEPTH_LIMIT")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: InitSettingsSource,
        env_settings: EnvSettingsSource,
        dotenv_settings: DotEnvSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


def load_config() -> AppConfig:
    return AppConfig()


def create_collector_config(config: AppConfig):
    from .main import CollectorConfig, StreamType

    try:
        stream = StreamType(config.default_stream.lower())
    except ValueError:
        stream = StreamType.TRADES

    return CollectorConfig(
        symbol=config.default_symbol.upper(),
        stream=stream,
        interval=config.default_interval,
        depth_limit=config.default_depth_limit,
    )
