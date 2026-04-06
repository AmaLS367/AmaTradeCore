import { useState } from "react";
import { Navigate, Route, Routes, useLocation, useNavigate, useParams } from "react-router-dom";
import { getOrderedPages, getPage } from "./content";
import type { DocBlock, DocLanguage, DocPage } from "./types";

const languages: DocLanguage[] = ["ru", "en"];

function renderBlock(block: DocBlock) {
  switch (block.type) {
    case "paragraph":
      return <p>{block.text}</p>;
    case "list":
      return <ul>{block.items.map((item) => <li key={item}>{item}</li>)}</ul>;
    case "code":
      return (
        <div className="code-block">
          {block.caption ? <div className="code-caption">{block.caption}</div> : null}
          <pre><code>{block.code}</code></pre>
        </div>
      );
    case "callout":
      return <div className={`callout callout-${block.tone}`}><strong>{block.title}</strong><p>{block.text}</p></div>;
    case "glossary":
      return (
        <div className="glossary-grid">
          {block.entries.map((entry) => (
            <article key={entry.term} className="glossary-card">
              <h4>{entry.term}</h4>
              <p>{entry.description}</p>
            </article>
          ))}
        </div>
      );
  }
}

function DocLayout({ language, page }: { language: DocLanguage; page: DocPage }) {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const pages = getOrderedPages(language);
  const value = query.trim().toLowerCase();
  const filtered = !value
    ? pages
    : pages.filter((candidate) => {
        const haystack = [
          candidate.title,
          candidate.description,
          candidate.section,
          ...(candidate.searchTerms ?? []),
          ...candidate.sections.map((section) => section.heading),
        ].join(" ").toLowerCase();
        return haystack.includes(value);
      });

  const currentIndex = pages.findIndex((item) => item.slug === page.slug);
  const previousPage = currentIndex > 0 ? pages[currentIndex - 1] : undefined;
  const nextPage = currentIndex < pages.length - 1 ? pages[currentIndex + 1] : undefined;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="eyebrow">AmaTradeCore</div>
          <h1 className="brand-title">Docs</h1>
          <p className="sidebar-text">Binance-first collector docs for CLI, config, modes, and data models.</p>
        </div>
        <label className="search">
          <span>Search</span>
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={language === "ru" ? "Найти страницу или режим" : "Find a page or mode"} />
        </label>
        <nav className="nav-groups" aria-label="Documentation navigation">
          {Array.from(new Set(filtered.map((entry) => entry.section))).map((section) => (
            <div key={section} className="nav-group">
              <div className="nav-group-title">{section}</div>
              {filtered.filter((entry) => entry.section === section).map((entry) => {
                const href = `/${language}/${entry.slug}`;
                const active = location.pathname === href;
                return <button key={entry.slug} type="button" className={`nav-link ${active ? "active" : ""}`} onClick={() => navigate(href)}>{entry.title}</button>;
              })}
            </div>
          ))}
        </nav>
      </aside>
      <main className="content">
        <header className="topbar">
          <div>
            <div className="eyebrow">{language === "ru" ? "Документация" : "Documentation"}</div>
            <h2>{page.title}</h2>
            <p className="page-description">{page.description}</p>
          </div>
          <div className="language-switcher" role="group" aria-label="Language switcher">
            {languages.map((candidate) => (
              <button key={candidate} type="button" className={candidate === language ? "active" : ""} onClick={() => navigate(`/${candidate}/${page.slug}`)}>{candidate.toUpperCase()}</button>
            ))}
          </div>
        </header>
        <article className="doc-page">
          {page.sections.map((section) => (
            <section key={section.id} id={section.id} className="doc-section">
              <h3>{section.heading}</h3>
              {section.blocks.map((block, index) => <div key={`${section.id}-${index}`} className="doc-block">{renderBlock(block)}</div>)}
            </section>
          ))}
        </article>
        <footer className="pager">
          {previousPage ? <button type="button" onClick={() => navigate(`/${language}/${previousPage.slug}`)}>← {previousPage.title}</button> : <span />}
          {nextPage ? <button type="button" onClick={() => navigate(`/${language}/${nextPage.slug}`)}>{nextPage.title} →</button> : null}
        </footer>
      </main>
    </div>
  );
}

function DocRoute() {
  const params = useParams();
  const language = languages.includes(params.language as DocLanguage) ? (params.language as DocLanguage) : "ru";
  const slug = params.slug ?? "overview";
  const page = getPage(language, slug);
  if (!page) return <Navigate to={`/${language}/overview`} replace />;
  return <DocLayout language={language} page={page} />;
}

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/ru/overview" replace />} />
      <Route path="/:language/:slug" element={<DocRoute />} />
      <Route path="*" element={<Navigate to="/ru/overview" replace />} />
    </Routes>
  );
}
