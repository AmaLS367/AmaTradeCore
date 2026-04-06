import type { DocPage } from "../../types";

export const dataModelsEn: DocPage = {
  slug: "data-models",
  title: "Data Models",
  description: "Typed objects used by the Binance collector.",
  section: "Reference",
  language: "en",
  sections: [
    {
      id: "models",
      heading: "Core models",
      blocks: [
        { type: "glossary", entries: [
          { term: "Trade", description: "A normalized trade event." },
          { term: "Kline", description: "A normalized candle event." },
          { term: "BookTicker", description: "Best bid/ask state." },
          { term: "DepthUpdate", description: "Order book delta event." },
          { term: "OrderBook", description: "REST depth snapshot." },
          { term: "ExchangeInfo", description: "Exchange metadata and tradable symbols." },
        ] },
      ],
    },
  ],
};
