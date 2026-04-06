import type { DocPage } from "../../types";

export const gettingStartedRu: DocPage = {
  slug: "getting-started",
  title: "Быстрый старт",
  description: "Как установить зависимости, настроить .env и запустить collector.",
  section: "Введение",
  language: "ru",
  searchTerms: ["uv", "install", "run", "collector"],
  sections: [
    { id: "install", heading: "Установка", blocks: [{ type: "code", language: "bash", caption: "Установка зависимостей и проверка тестов", code: "uv sync\nuv run pytest" }] },
    {
      id: "run",
      heading: "Запуск collector",
      blocks: [
        { type: "code", language: "bash", caption: "Запуск интерактивного терминального collector", code: "uv run amatradecore" },
        { type: "list", items: ["Up/Down перемещают курсор по настройкам.", "Left/Right меняют значение текущей настройки.", "Enter на Start Collector запускает поток данных.", "q, Esc или Ctrl+C останавливают live collector."] },
      ],
    },
    {
      id: "pairs",
      heading: "Как выбрать торговую пару",
      blocks: [
        { type: "paragraph", text: "Есть два способа. Первый — листать доступные пары стрелками на строке Pair. Второй — открыть строку Custom Pair и ввести тикер вручную, например BTCUSDT, ETHUSDT или ARBUSDT." },
        { type: "callout", tone: "tip", title: "Когда использовать Custom Pair", text: "Если нужная пара далеко в списке или ты уже знаешь точный тикер, custom input быстрее и удобнее." },
      ],
    },
  ],
};
