from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_SITE = ROOT / "docs-site"


def test_docs_site_scaffold_exists():
    assert (DOCS_SITE / "package.json").exists()
    assert (DOCS_SITE / "vite.config.ts").exists()
    assert (DOCS_SITE / "src" / "main.tsx").exists()


def test_vite_base_is_configured_for_github_pages():
    vite_config = (DOCS_SITE / "vite.config.ts").read_text(encoding="utf-8")

    assert "base: '/AmaTradeCore/'" in vite_config or 'base: "/AmaTradeCore/"' in vite_config


def test_docs_content_tree_exists_for_both_languages():
    ru_pages = [
        "overview",
        "getting-started",
        "configuration",
        "collector-modes",
        "cli-guide",
        "data-models",
        "faq",
    ]
    en_pages = list(ru_pages)

    for slug in ru_pages:
        assert (DOCS_SITE / "src" / "content" / "ru" / f"{slug}.ts").exists()

    for slug in en_pages:
        assert (DOCS_SITE / "src" / "content" / "en" / f"{slug}.ts").exists()


def test_collector_modes_page_mentions_all_supported_modes():
    collector_modes = (DOCS_SITE / "src" / "content" / "ru" / "collector-modes.ts").read_text(
        encoding="utf-8"
    )

    assert "TRADE" in collector_modes
    assert "KLINE" in collector_modes
    assert "BOOK_TICKER" in collector_modes
    assert "DEPTH_UPDATES" in collector_modes


def test_configuration_page_mentions_all_current_env_vars():
    configuration_page = (DOCS_SITE / "src" / "content" / "ru" / "configuration.ts").read_text(
        encoding="utf-8"
    )

    for env_var in [
        "BINANCE_API_KEY",
        "BINANCE_API_SECRET",
        "BINANCE_BASE_URL",
        "BINANCE_WS_URL",
        "DEFAULT_SYMBOL",
        "DEFAULT_STREAM",
        "DEFAULT_INTERVAL",
        "DEFAULT_DEPTH_LIMIT",
        "LOG_LEVEL",
    ]:
        assert env_var in configuration_page


def test_github_pages_workflow_exists():
    workflow = ROOT / ".github" / "workflows" / "docs-pages.yml"

    assert workflow.exists()


def test_docs_site_build_has_spa_fallback_for_github_pages():
    package_json = (DOCS_SITE / "package.json").read_text(encoding="utf-8")
    fallback_script = DOCS_SITE / "scripts" / "copy-spa-fallback.mjs"

    assert "copy-spa-fallback" in package_json
    assert fallback_script.exists()
