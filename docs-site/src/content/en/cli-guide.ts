import type { DocPage } from "../../types";

export const cliGuideEn: DocPage = {
  slug: "cli-guide",
  title: "CLI Guide",
  description: "How to navigate the terminal collector and use custom symbol input.",
  section: "Usage",
  language: "en",
  sections: [
    {
      id: "navigation",
      heading: "Navigation",
      blocks: [
        { type: "list", items: ["Pair lets you cycle through fetched symbols.", "Custom Pair lets you type a symbol directly.", "Start Collector opens the live collector view.", "Quit exits the menu."] },
      ],
    },
  ],
};
