import { useState, useEffect } from "react";
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
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "light");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme((prev) => (prev === "light" ? "dark" : "light"));

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
          <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
            <button 
              type="button" 
              className="theme-toggle" 
              onClick={toggleTheme}
              aria-label="Toggle theme"
              style={{
                background: "var(--switcher-bg)",
                border: "none",
                borderRadius: "50%",
                width: "40px",
                height: "40px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
                color: "var(--text-main)"
              }}
            >
              {theme === "light" ? (
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
              )}
            </button>
            <div className="language-switcher" role="group" aria-label="Language switcher">
              {languages.map((candidate) => (
                <button key={candidate} type="button" className={candidate === language ? "active" : ""} onClick={() => navigate(`/${candidate}/${page.slug}`)}>{candidate.toUpperCase()}</button>
              ))}
            </div>
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

function Landing({ language }: { language: DocLanguage }) {
  const navigate = useNavigate();
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "light");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme((prev) => (prev === "light" ? "dark" : "light"));
  const content = {
    ru: {
      title: "Сбор данных Binance — без лишних сложностей",
      subtitle: "AmaTradeCore: Профессиональный инструмент для тех, кто ценит чистоту данных и простоту запуска.",
      cta: "Перейти к документации",
      features: [
        { title: "Для новичков", desc: "Не нужно быть программистом. Запуск одной командой через терминал." },
        { title: "Чистые данные", desc: "Мы уже настроили фильтрацию и форматирование. Вы получаете готовые CSV/JSON." },
        { title: "Надежность", desc: "Авто-реконнект к Binance. Никаких пропущенных тиков и свечей." }
      ],
      forWhom: [
        { t: "Трейдерам", d: "Собирайте историю для анализа своих стратегий без участия в API-сложностях." },
        { t: "Аналитикам", d: "Получайте данные в идеальном виде для Excel, Python или SQL." },
        { t: "Разработчикам", d: "Используйте как надежное ядро для своих торговых ботов." }
      ]
    },
    en: {
      title: "Binance Data Collection — Simplified",
      subtitle: "AmaTradeCore: A professional tool for those who value data purity and ease of use.",
      cta: "Go to Documentation",
      features: [
        { title: "Beginner Friendly", desc: "No coding required. Launch with a single command in your terminal." },
        { title: "Clean Data", desc: "Filtered and formatted. You get ready-to-use CSV/JSON files." },
        { title: "Reliable", desc: "Auto-reconnect to Binance. No missed ticks or candles." }
      ],
      forWhom: [
        { t: "Traders", d: "Collect history for backtesting without dealing with API complexity." },
        { t: "Analysts", d: "Get data in perfect shape for Excel, Python, or SQL." },
        { t: "Developers", d: "Use it as a robust core for your trading bots." }
      ]
    }
  }[language];

  return (
    <div className="landing">
      <section className="hero">
        <div className="eyebrow">AmaTradeCore</div>
        <h1>{content.title}</h1>
        <p className="hero-text">{content.subtitle}</p>
        <button className="cta-button" onClick={() => navigate(`/${language}/overview`)}>{content.cta}</button>
      </section>

      <div className="landing-grid">
        {content.features.map(f => (
          <div key={f.title} className="feature-card">
            <h3>{f.title}</h3>
            <p>{f.desc}</p>
          </div>
        ))}
      </div>

      <section className="use-cases">
        <h2 style={{ textAlign: "center", marginBottom: "40px" }}>{language === "ru" ? "Для кого это?" : "Who is it for?"}</h2>
        <div className="cases-grid">
          {content.forWhom.map(c => (
            <div key={c.t} className="case-item">
              <strong>{c.t}</strong>
              <p>{c.d}</p>
            </div>
          ))}
        </div>
      </section>
      
      <footer className="landing-footer">
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <button 
            type="button" 
            className="theme-toggle" 
            onClick={toggleTheme}
            aria-label="Toggle theme"
            style={{
              background: "var(--section-bg)",
              border: "1px solid var(--sidebar-border)",
              borderRadius: "50%",
              width: "40px",
              height: "40px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              color: "var(--text-main)"
            }}
          >
            {theme === "light" ? (
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
            )}
          </button>
          <div className="language-switcher" style={{ background: "var(--section-bg)", border: "1px solid var(--sidebar-border)" }}>
            {languages.map((candidate) => (
              <button key={candidate} type="button" className={candidate === language ? "active" : ""} onClick={() => navigate(`/${candidate}`)}>{candidate.toUpperCase()}</button>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/ru" replace />} />
      <Route path="/ru" element={<Landing language="ru" />} />
      <Route path="/en" element={<Landing language="en" />} />
      <Route path="/:language/:slug" element={<DocRoute />} />
      <Route path="*" element={<Navigate to="/ru" replace />} />
    </Routes>
  );
}
