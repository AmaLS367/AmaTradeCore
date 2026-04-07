import type { DocPage } from "../../types";

export const overviewEn: DocPage = {
  slug: "overview",
  title: "Overview",
  description: "What AmaTradeCore is today and what Phase 1 currently covers.",
  section: "Introduction",
  language: "en",
  searchTerms: ["market data collector", "binance", "phase 1"],
  sections: [
    {
      id: "project",
      heading: "What the project is",
      blocks: [
        { type: "paragraph", text: "AmaTradeCore is currently on Phase 1 and implements a Binance-first Market Data Collector. It is not yet a trading engine or a risk manager." },
        { type: "list", items: ["Public Binance REST market-data requests.", "Public Binance WebSocket streams.", "A terminal CLI collector for live event viewing.", "Typed models for trades, klines, book ticker, order books, and depth updates."] },
      ],
    },
    {
      id: "for-beginners",
      heading: "Trading for All: Data Basics",
      blocks: [
        { type: "paragraph", text: "If you're just starting your journey in trading, here's a brief guide to the data collected by AmaTradeCore:" },
        {
          type: "glossary",
          entries: [
            { term: "Ticker (Symbol)", description: "A unique code for a pair, like BTCUSDT. This is the price of Bitcoin expressed in dollars (USDT)." },
            { term: "Trade", description: "An event when a buyer and a seller find each other. Each trade has a price and a quantity (the amount of coins exchanged)." },
            { term: "Order Book", description: "A list of buy and sell orders from all market participants. It shows how many people want to trade at specific prices." },
            { term: "Kline (Candle)", description: "A way to visualize price over a period. It includes the opening, closing, high, and low prices." },
          ],
        },
      ],
    },
    {
      id: "logging-guide",
      heading: "Read Logs Like a Pro",
      blocks: [
        { type: "paragraph", text: "When you launch the collector, a data stream appears in the terminal. We've designed it to be as clear as possible, even for those without prior experience." },
        {
          type: "code",
          caption: "Example of a trade log",
          code: "[12:45:01] TRADE | BTCUSDT | Price: 68,420.50 | Qty: 0.021 | Side: SELL (Maker: BUY)",
        },
        {
          type: "list",
          items: [
            "Time [12:45:01] — exactly when the event occurred on the exchange.",
            "Data Type (TRADE) — indicates that this information is about a real purchase or sale.",
            "Price and Qty — the price and quantity of the trade. This is the core for any analysis.",
            "Side — shows the aggressive side. If SELL, it means someone sold at the market price into a buyer's limit order.",
          ],
        },
        { type: "callout", tone: "tip", title: "Why is this useful?", text: "Watching 'live' logs helps you feel the pulse of the market—how often large trades occur and how quickly the order book shifts." },
      ],
    },
  ],
};
