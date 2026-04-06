import { cliGuideEn } from "./en/cli-guide";
import { collectorModesEn } from "./en/collector-modes";
import { configurationEn } from "./en/configuration";
import { dataModelsEn } from "./en/data-models";
import { faqEn } from "./en/faq";
import { gettingStartedEn } from "./en/getting-started";
import { overviewEn } from "./en/overview";
import { cliGuideRu } from "./ru/cli-guide";
import { collectorModesRu } from "./ru/collector-modes";
import { configurationRu } from "./ru/configuration";
import { dataModelsRu } from "./ru/data-models";
import { faqRu } from "./ru/faq";
import { gettingStartedRu } from "./ru/getting-started";
import { overviewRu } from "./ru/overview";
import type { DocLanguage, DocPage } from "../types";

export const docsOrder = ["overview", "getting-started", "configuration", "collector-modes", "cli-guide", "data-models", "faq"] as const;

export const docsByLanguage: Record<DocLanguage, DocPage[]> = {
  ru: [overviewRu, gettingStartedRu, configurationRu, collectorModesRu, cliGuideRu, dataModelsRu, faqRu],
  en: [overviewEn, gettingStartedEn, configurationEn, collectorModesEn, cliGuideEn, dataModelsEn, faqEn],
};

export function getPage(language: DocLanguage, slug: string): DocPage | undefined {
  return docsByLanguage[language].find((page) => page.slug === slug);
}

export function getOrderedPages(language: DocLanguage): DocPage[] {
  const pages = docsByLanguage[language];
  return docsOrder.map((slug) => pages.find((page) => page.slug === slug)).filter((page): page is DocPage => Boolean(page));
}
