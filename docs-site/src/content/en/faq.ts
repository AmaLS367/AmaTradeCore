import type { DocPage } from "../../types";

export const faqEn: DocPage = {
  slug: "faq",
  title: "FAQ",
  description: "Answers to the most common first-run questions.",
  section: "Reference",
  language: "en",
  sections: [
    {
      id: "faq",
      heading: "Common questions",
      blocks: [
        {
          type: "glossary",
          entries: [
            { term: "Why is the API key optional?", description: "Because Phase 1 uses public Binance market-data endpoints." },
            { term: "Why does KLINE repeat with a different close?", description: "Because Binance pushes multiple updates for the same open candle." },
            { term: "What is snapshot vs stream?", description: "Snapshot is a point-in-time REST state, while a stream is a sequence of live WebSocket events." },
          ],
        },
      ],
    },
  ],
};
