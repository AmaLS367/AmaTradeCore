# AmaTradeCore

Это Phase 1 ядра для торгового бота или аналитической платформы на Python.

## Начало работы

1. Склонируйте репозиторий.
2. Скопируйте `.env.example` в `.env` и настройте переменные окружения.
3. Установите зависимости через `uv sync`.

## Проверка

```bash
uv run pytest
```

## CLI

Запуск интерактивного data collector:

```bash
uv run amatradecore
```

Или напрямую как модуль:

```bash
uv run python -m src
```

Управление:

- `Up/Down` перемещают курсор по настройкам
- `Left/Right` меняют значение текущей настройки
- `Enter` запускает collector или выходит
- `q` закрывает меню или останавливает live collector

## REST пример

```python
from src.api.client import BinanceAsyncClient


async def main():
    async with BinanceAsyncClient() as client:
        server_time = await client.get_server_time()
        order_book = await client.get_order_book("BTCUSDT", limit=5)
        print(server_time.serverTime, order_book.bids[0])
```

## WebSocket пример

```python
from src.api.websocket import BinanceWebSocketManager


async def on_trade(trade):
    print(trade.symbol, trade.price, trade.qty)


async def main():
    manager = BinanceWebSocketManager()
    await manager.subscribe_trades("BTCUSDT", on_trade)
```
