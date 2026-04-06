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
  ],
};
