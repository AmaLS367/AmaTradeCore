import type { DocPage } from "../../types";

export const configurationRu: DocPage = {
  slug: "configuration",
  title: "Конфигурация",
  description: "Все env-переменные проекта и как они влияют на collector.",
  section: "Использование",
  language: "ru",
  searchTerms: ["env", "BINANCE_API_KEY", "DEFAULT_SYMBOL"],
  sections: [
    {
      id: "env-file",
      heading: "Файл .env",
      blocks: [
        { type: "paragraph", text: "Конфигурация читается через pydantic-settings из файла .env. Это значит, что значения подхватываются без ручного парсинга dotenv в приложении." },
        { type: "code", language: "dotenv", caption: "Текущий формат .env.example", code: "BINANCE_API_KEY=\nBINANCE_API_SECRET=\nBINANCE_BASE_URL=https://api.binance.com\nBINANCE_WS_URL=wss://stream.binance.com:9443/ws\nDEFAULT_SYMBOL=BTCUSDT\nDEFAULT_STREAM=trades\nDEFAULT_INTERVAL=1m\nDEFAULT_DEPTH_LIMIT=20\nLOG_LEVEL=INFO" },
      ],
    },
    {
      id: "vars",
      heading: "Что делает каждая переменная",
      blocks: [
        {
          type: "glossary",
          entries: [
            { term: "BINANCE_API_KEY", description: "API key Binance. Для текущих публичных market-data endpoints не обязателен." },
            { term: "BINANCE_API_SECRET", description: "API secret. Сейчас хранится в конфиге, но Phase 1 collector не использует signed requests." },
            { term: "BINANCE_BASE_URL", description: "REST endpoint Binance. Можно переключить на testnet или кастомный endpoint." },
            { term: "BINANCE_WS_URL", description: "WebSocket base URL для live стримов." },
            { term: "DEFAULT_SYMBOL", description: "Стартовая пара в меню collector." },
            { term: "DEFAULT_STREAM", description: "Стартовый режим collector: trades, klines, book_ticker или depth_updates." },
            { term: "DEFAULT_INTERVAL", description: "Дефолтный таймфрейм для режима KLINE." },
            { term: "DEFAULT_DEPTH_LIMIT", description: "Глубина order book snapshot для depth-related сценариев." },
            { term: "LOG_LEVEL", description: "Уровень логирования приложения." },
          ],
        },
      ],
    },
    { id: "auth", heading: "Public vs authenticated mode", blocks: [{ type: "paragraph", text: "CLI collector показывает режим подключения как public или authenticated. Для market data Phase 1 наличие API key не требуется. Если ключ передан, статус интерфейса меняется, но публичные market endpoints всё равно остаются основным источником данных." }] },
  ],
};
