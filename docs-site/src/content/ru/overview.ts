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
    {
      id: "for-beginners",
      heading: "Трейдинг для всех: Основы данных",
      blocks: [
        { type: "paragraph", text: "Если вы только начинаете путь в трейдинге, вот краткий путеводитель по данным, которые собирает AmaTradeCore:" },
        {
          type: "glossary",
          entries: [
            { term: "Тикер (Ticker/Symbol)", description: "Условное обозначение пары, например BTCUSDT. Это цена Биткоина, выраженная в долларах (USDT)." },
            { term: "Сделка (Trade)", description: "Событие, когда покупатель и продавец нашли друг друга. Каждая сделка имеет цену и объем (количество купленных монет)." },
            { term: "Стакан (Order Book)", description: "Очередь из заявок всех участников рынка. Показывает, сколько людей хотят купить или продать монету по конкретным ценам." },
            { term: "Свеча (Kline/Candle)", description: "Способ визуализации цены за период времени. Включает цену открытия, закрытия, максимум и минимум." },
          ],
        },
      ],
    },
    {
      id: "logging-guide",
      heading: "Читаем логи как профи",
      blocks: [
        { type: "paragraph", text: "При запуске коллектора в терминале появляется поток данных. Мы сделали его максимально понятным даже для человека без опыта." },
        {
          type: "code",
          language: "text",
          caption: "Пример лога сделки",
          code: "[12:45:01] TRADE | BTCUSDT | Price: 68,420.50 | Qty: 0.021 | Side: SELL (Maker: BUY)",
        },
        {
          type: "list",
          items: [
            "Время [12:45:01] — когда именно произошло событие на бирже.",
            "Тип данных (TRADE) — указывает, что это информация о реальной покупке/продаже.",
            "Price и Qty — за сколько и сколько купили. Это база для любого анализа.",
            "Side — показывает агрессивную сторону. Если SELL, значит кто-то продал по рынку в лимитный ордер покупателя.",
          ],
        },
        { type: "callout", tone: "tip", title: "Зачем это нужно?", text: "Наблюдение за 'живыми' логами помогает почувствовать ритм рынка — как часто проходят крупные сделки и как быстро меняется цена в стакане." },
      ],
    },

  ],
};
