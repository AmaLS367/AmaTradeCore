import type { DocPage } from "../../types";

export const collectorModesRu: DocPage = {
  slug: "collector-modes",
  title: "Режимы collector",
  description: "Что означают TRADE, KLINE, BOOK_TICKER и DEPTH_UPDATES, и какой поток данных ты видишь в CLI.",
  section: "Использование",
  language: "ru",
  searchTerms: ["TRADE", "KLINE", "BOOK_TICKER", "DEPTH_UPDATES"],
  sections: [
    {
      id: "glossary",
      heading: "Глоссарий режимов",
      blocks: [
        { type: "glossary", entries: [
          { term: "TRADE", description: "Отдельные рыночные сделки. Каждое событие — это конкретный trade с ценой, количеством и временем." },
          { term: "KLINE", description: "Обновления свечи выбранного интервала. Пока свеча не закрыта, close может меняться много раз." },
          { term: "BOOK_TICKER", description: "Поток лучшего bid/ask. Это компактное состояние верхушки стакана." },
          { term: "DEPTH_UPDATES", description: "Дельты order book. Это не полный стакан, а изменения по ценовым уровням." },
        ] },
      ],
    },
    {
      id: "kline-example",
      heading: "Как читать строку KLINE",
      blocks: [
        { type: "code", language: "text", caption: "Пример вывода CLI", code: "KLINE BTCUSDT 5m o=69152.25 h=69159.04 l=69122.24 c=69143.18" },
        { type: "list", items: ["KLINE — тип события, то есть обновление свечи.", "BTCUSDT — символ торговой пары.", "5m — таймфрейм свечи.", "o — open, цена открытия свечи.", "h — high, максимум внутри свечи.", "l — low, минимум внутри свечи.", "c — close, текущее значение close; до закрытия свечи оно меняется."] },
        { type: "callout", tone: "info", title: "Почему KLINE повторяется", text: "WebSocket Binance шлёт апдейты одной и той же свечи до её закрытия. Поэтому open/high/low часто остаются прежними, а close двигается вместе с рынком." },
      ],
    },
    { id: "which-mode", heading: "Когда какой режим использовать", blocks: [{ type: "list", items: ["TRADE — когда нужен поток фактических сделок и microstructure.", "KLINE — когда нужен свечной поток по таймфрейму и более удобный обзор.", "BOOK_TICKER — когда интересуют только лучшие bid/ask.", "DEPTH_UPDATES — когда нужен поток изменений стакана, а не только top-of-book."] }] },
  ],
};
