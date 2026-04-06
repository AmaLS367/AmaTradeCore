import type { DocPage } from "../../types";

export const collectorModesEn: DocPage = {
  slug: "collector-modes",
  title: "Collector Modes",
  description: "Explain TRADE, KLINE, BOOK_TICKER, and DEPTH_UPDATES.",
  section: "Usage",
  language: "en",
  sections: [
    {
      id: "modes",
      heading: "Mode glossary",
      blocks: [
        { type: "glossary", entries: [
          { term: "TRADE", description: "Individual market trades." },
          { term: "KLINE", description: "Candle updates for a chosen interval." },
          { term: "BOOK_TICKER", description: "Best bid/ask stream." },
          { term: "DEPTH_UPDATES", description: "Order book delta updates." },
        ] },
      ],
    },
    {
      id: "example",
      heading: "Reading a KLINE line",
      blocks: [
        { type: "code", language: "text", code: "KLINE BTCUSDT 5m o=69152.25 h=69159.04 l=69122.24 c=69143.18" },
        { type: "paragraph", text: "This means a BTCUSDT candle update for the 5-minute timeframe where open, high, low, and current close are shown. The line can repeat because Binance updates an unfinished candle multiple times." },
      ],
    },
  ],
};
