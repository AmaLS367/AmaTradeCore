import type { DocPage } from "../../types";

export const configurationEn: DocPage = {
  slug: "configuration",
  title: "Configuration",
  description: "Environment variables and how they affect the collector.",
  section: "Usage",
  language: "en",
  sections: [
    {
      id: "vars",
      heading: "Environment variables",
      blocks: [
        {
          type: "glossary",
          entries: [
            { term: "BINANCE_API_KEY", description: "Optional Binance API key." },
            { term: "BINANCE_API_SECRET", description: "Optional Binance API secret." },
            { term: "BINANCE_BASE_URL", description: "REST base URL." },
            { term: "BINANCE_WS_URL", description: "WebSocket base URL." },
            { term: "DEFAULT_SYMBOL", description: "Default symbol shown in the CLI." },
            { term: "DEFAULT_STREAM", description: "Default stream mode." },
            { term: "DEFAULT_INTERVAL", description: "Default kline interval." },
            { term: "DEFAULT_DEPTH_LIMIT", description: "Default depth snapshot size." },
            { term: "LOG_LEVEL", description: "Application log level." },
          ],
        },
      ],
    },
  ],
};
