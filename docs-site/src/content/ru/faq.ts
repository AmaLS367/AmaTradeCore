import type { DocPage } from "../../types";

export const faqRu: DocPage = {
  slug: "faq",
  title: "FAQ",
  description: "Короткие ответы на вопросы, которые возникают при первом запуске collector.",
  section: "Reference",
  language: "ru",
  searchTerms: ["faq", "api key", "snapshot", "stream"],
  sections: [
    {
      id: "questions",
      heading: "Частые вопросы",
      blocks: [
        {
          type: "glossary",
          entries: [
            { term: "Почему API key необязателен?", description: "Потому что текущая Phase 1 использует публичные market data endpoints Binance." },
            { term: "Почему KLINE повторяется с разным close?", description: "Потому что до закрытия свечи Binance шлёт несколько обновлений одной и той же свечи." },
            { term: "Что такое snapshot vs stream?", description: "Snapshot — снимок состояния на момент запроса через REST. Stream — последовательность live-событий через WebSocket." },
            { term: "Что такое BOOK_TICKER и чем он отличается от DEPTH_UPDATES?", description: "BOOK_TICKER даёт только лучший bid/ask, а DEPTH_UPDATES — изменения по нескольким уровням стакана." },
          ],
        },
      ],
    },
  ],
};
