export type DocLanguage = "ru" | "en";

export type DocBlock =
  | { type: "paragraph"; text: string }
  | { type: "list"; items: string[] }
  | { type: "code"; language: string; code: string; caption?: string }
  | { type: "callout"; tone: "info" | "tip" | "warn"; title: string; text: string }
  | { type: "glossary"; entries: Array<{ term: string; description: string }> };

export interface DocSection {
  id: string;
  heading: string;
  blocks: DocBlock[];
}

export interface DocPage {
  slug: string;
  title: string;
  description: string;
  section: string;
  language: DocLanguage;
  sections: DocSection[];
  searchTerms?: string[];
}
