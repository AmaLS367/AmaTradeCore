import type { DocPage } from "../../types";

export const dataModelsRu: DocPage = {
  slug: "data-models",
  title: "Модели данных",
  description: "Какие typed-модели используются в AmaTradeCore и что они обозначают.",
  section: "Reference",
  language: "ru",
  searchTerms: ["Trade", "Kline", "BookTicker", "DepthUpdate", "OrderBook"],
  sections: [
    {
      id: "models",
      heading: "Основные модели",
      blocks: [
        {
          type: "glossary",
          entries: [
            { term: "Trade", description: "Сделка: id, price, qty, quoteQty, time, buyer-maker flags и symbol." },
            { term: "Kline", description: "Свеча: open/high/low/close, volume, interval, symbol и тайминги свечи." },
            { term: "BookTicker", description: "Лучший bid/ask плюс количества и update id." },
            { term: "DepthUpdate", description: "Апдейт стакана с диапазоном update ids и наборами bids/asks." },
            { term: "OrderBook", description: "REST snapshot стакана с lastUpdateId и текущими уровнями bids/asks." },
            { term: "ExchangeInfo", description: "Метаданные биржи, включая список символов и их статусы." },
          ],
        },
      ],
    },
    { id: "typing", heading: "Зачем это важно", blocks: [{ type: "paragraph", text: "CLI получает уже typed payloads, а не сырые dict-объекты. Это упрощает дальнейшее расширение на стратегии, валидацию правил биржи и документирование формата данных." }] },
  ],
};
