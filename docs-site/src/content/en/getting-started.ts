import type { DocPage } from "../../types";

export const gettingStartedEn: DocPage = {
  slug: "getting-started",
  title: "Getting Started",
  description: "Install dependencies, configure .env, and start the collector.",
  section: "Introduction",
  language: "en",
  sections: [
    { id: "install", heading: "Install and test", blocks: [{ type: "code", language: "bash", code: "uv sync\nuv run pytest" }] },
    {
      id: "run",
      heading: "Run the collector",
      blocks: [
        { type: "code", language: "bash", code: "uv run amatradecore" },
        { type: "list", items: ["Use Up/Down to move across settings.", "Use Left/Right to change a selected value.", "Press Enter on Start Collector to launch the live screen.", "Use q, Esc, or Ctrl+C to stop the collector."] },
      ],
    },
  ],
};
