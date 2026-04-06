import type { DocPage } from "../../types";

export const cliGuideRu: DocPage = {
  slug: "cli-guide",
  title: "CLI Guide",
  description: "Навигация по терминальному интерфейсу collector и разбор поведения live-экрана.",
  section: "Использование",
  language: "ru",
  searchTerms: ["CLI", "custom pair", "arrow keys", "exit"],
  sections: [
    {
      id: "menu",
      heading: "Навигация по меню",
      blocks: [
        { type: "list", items: ["Pair — переключение по доступным символам стрелками Left/Right.", "Stream — выбор режима: Trades, Klines, Best Bid/Ask, Depth Updates.", "Interval — таймфрейм для KLINE.", "Depth Limit — глубина snapshot для сценариев со стаканом.", "Custom Pair — ручной ввод тикера.", "Start Collector — запуск live collector.", "Quit — выход из меню."] },
      ],
    },
    {
      id: "custom",
      heading: "Custom Pair input",
      blocks: [
        { type: "paragraph", text: "На строке Custom Pair нажми Enter и введи тикер. Символ нормализуется в uppercase и добавляется в список доступных пар для дальнейшего быстрого выбора." },
        { type: "list", items: ["Enter подтверждает ввод.", "Backspace удаляет символ.", "Esc отменяет редактирование пары."] },
      ],
    },
    { id: "live", heading: "Выход из live collector", blocks: [{ type: "paragraph", text: "Во время работы collector выход обрабатывается без постоянного redraw-спама. Для остановки можно использовать q, Esc или Ctrl+C." }] },
  ],
};
