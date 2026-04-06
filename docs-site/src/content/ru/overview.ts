import type { DocPage } from "../../types";

export const overviewRu: DocPage = {
  slug: "overview",
  title: "Обзор",
  description: "Что такое AmaTradeCore сегодня и какие задачи решает текущая Phase 1.",
  section: "Введение",
  language: "ru",
  searchTerms: ["market data collector", "binance", "phase 1"],
  sections: [
    {
      id: "project",
      heading: "Что это за проект",
      blocks: [
        { type: "paragraph", text: "AmaTradeCore сейчас находится на Phase 1 и реализует Binance-first Market Data Collector. Это не торговый движок и не риск-менеджер, а слой получения и нормализации рыночных данных." },
        { type: "list", items: ["Публичные REST-запросы к Binance для market data.", "Публичные WebSocket-стримы Binance.", "CLI collector для живого просмотра событий в терминале.", "Typed-модели данных для trade, kline, book ticker, order book и depth updates."] },
      ],
    },
    {
      id: "boundaries",
      heading: "Что уже есть и чего пока нет",
      blocks: [
        { type: "callout", tone: "info", title: "Текущее состояние", text: "Проект умеет собирать и отображать market data, но не исполняет ордера, не строит локально синхронизированную книгу и не содержит слой риск-менеджмента." },
        { type: "list", items: ["Есть: сбор server time, exchange info, klines, trades, book ticker, order book snapshots и depth updates.", "Есть: интерактивный выбор пары и режима в CLI.", "Нет: private account endpoints и signed trading requests.", "Нет: persistence, strategy engine, paper trading и portfolio accounting."] },
      ],
    },
  ],
};
