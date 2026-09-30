import datetime
import importlib
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import generate_daily_post as gdp


def test_import_does_not_require_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_WRAPPER_BASE_URL", raising=False)
    monkeypatch.delenv("CLAUDE_WRAPPER_API_KEY", raising=False)
    importlib.reload(gdp)


# ---- sanitize_slug ----

def test_sanitize_slug_converts_spaces_and_lowercases():
    assert gdp.sanitize_slug("Hello World") == "hello-world"


def test_sanitize_slug_strips_non_ascii_characters():
    assert gdp.sanitize_slug("こんにちは World") == "world"


def test_sanitize_slug_truncates_to_six_words():
    raw = "one two three four five six seven eight"
    assert gdp.sanitize_slug(raw) == "one-two-three-four-five-six"


def test_sanitize_slug_falls_back_when_result_is_empty():
    assert gdp.sanitize_slug("こんにちは") == "daily-news"


# ---- extract_title ----

def test_extract_title_reads_title_from_front_matter():
    content = '---\ntitle: "Test Title"\ndate: 2026-01-01\n---\nBody text'
    assert gdp.extract_title(content) == "Test Title"


def test_extract_title_defaults_when_no_front_matter():
    assert gdp.extract_title("No front matter here") == "Daily News"


def test_extract_title_strips_markdown_code_block():
    content = '```markdown\n---\ntitle: "Wrapped"\n---\nBody\n```'
    assert gdp.extract_title(content) == "Wrapped"


# ---- save_post ----

def test_save_post_creates_post_and_index_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    today = datetime.date.today()
    content = '---\ntitle: "My Post"\ndate: 2026-01-01\n---\nBody'

    title = gdp.save_post(content, slug="my-post")

    assert title == "My Post"
    out_dir = tmp_path / "content" / "posts" / today.strftime("%Y") / today.strftime("%m")
    post_file = out_dir / f"{today.strftime('%Y-%m-%d')}-my-post.md"
    assert post_file.exists()
    assert 'author: "Ghost Writer"' in post_file.read_text(encoding="utf-8")
    assert (tmp_path / "content" / "posts" / today.strftime("%Y") / "_index.md").exists()
    assert (out_dir / "_index.md").exists()


def test_save_post_preserves_existing_author(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    content = '---\ntitle: "My Post"\nauthor: "Someone Else"\n---\nBody'

    gdp.save_post(content, slug="my-post")

    today = datetime.date.today()
    out_dir = tmp_path / "content" / "posts" / today.strftime("%Y") / today.strftime("%m")
    post_file = out_dir / f"{today.strftime('%Y-%m-%d')}-my-post.md"
    saved = post_file.read_text(encoding="utf-8")
    assert saved.count("author:") == 1
    assert 'author: "Someone Else"' in saved


# ---- fetch_rss_items ----

class FakeEntry(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def _fake_feed(entries):
    return SimpleNamespace(entries=entries)


def test_fetch_rss_items_takes_top_five_per_feed(monkeypatch):
    entries = [
        FakeEntry(title=f"Title {i}", link=f"https://example.com/{i}", summary=f"Summary {i}")
        for i in range(7)
    ]
    monkeypatch.setattr(gdp.feedparser, "parse", lambda url: _fake_feed(entries))

    items = gdp.fetch_rss_items()

    assert len(items) == 5 * len(gdp.RSS_FEEDS)
    assert "Title: Title 0" in items[0]
    assert "Summary: Summary 0" in items[0]


def test_fetch_rss_items_defaults_missing_summary(monkeypatch):
    entries = [FakeEntry(title="No Summary", link="https://example.com/x")]
    monkeypatch.setattr(gdp.feedparser, "parse", lambda url: _fake_feed(entries))

    items = gdp.fetch_rss_items()

    assert "Summary: No summary" in items[0]


def test_fetch_rss_items_skips_feed_on_error(monkeypatch):
    def flaky_parse(url):
        if url == gdp.RSS_FEEDS[0]:
            raise RuntimeError("network error")
        return _fake_feed([FakeEntry(title="OK", link="https://example.com/ok", summary="fine")])

    monkeypatch.setattr(gdp.feedparser, "parse", flaky_parse)

    items = gdp.fetch_rss_items()

    assert len(items) == len(gdp.RSS_FEEDS) - 1


# ---- generate_blog_post ----

def test_generate_blog_post_includes_feed_items_in_prompt():
    provider = MagicMock(spec=["generate"])
    provider.generate.return_value = "Generated post body"

    result = gdp.generate_blog_post(provider, ["- Title: Example News\n"])

    assert result == "Generated post body"
    provider.generate.assert_called_once()
    prompt = provider.generate.call_args[0][0]
    assert "Example News" in prompt


# ---- generate_slug ----

def test_generate_slug_sanitizes_successful_response():
    provider = MagicMock(spec=["generate"])
    provider.generate.return_value = "Adobe AI Agents"

    assert gdp.generate_slug(provider, "Some Title") == "adobe-ai-agents"
    provider.generate.assert_called_once()
    prompt = provider.generate.call_args[0][0]
    assert "Some Title" in prompt


def test_generate_slug_falls_back_on_empty_response():
    provider = MagicMock(spec=["generate"])
    provider.generate.return_value = ""

    assert gdp.generate_slug(provider, "Some Title") == "daily-news"


def test_generate_slug_falls_back_on_exception():
    provider = MagicMock(spec=["generate"])
    provider.generate.side_effect = RuntimeError("api error")

    assert gdp.generate_slug(provider, "Some Title") == "daily-news"


# ---- check_claude_wrapper_health ----

def test_check_claude_wrapper_health_success(monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = None
    monkeypatch.setattr(gdp.urllib.request, "urlopen", MagicMock(return_value=mock_resp))

    assert gdp.check_claude_wrapper_health("http://localhost:18789/v1") is True


def test_check_claude_wrapper_health_reads_env_var(monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = None
    monkeypatch.setenv("CLAUDE_WRAPPER_BASE_URL", "http://100.120.169.11:18789/v1")
    monkeypatch.setattr(gdp.urllib.request, "urlopen", MagicMock(return_value=mock_resp))

    assert gdp.check_claude_wrapper_health() is True


def test_check_claude_wrapper_health_failure_on_exception(monkeypatch):
    monkeypatch.setattr(
        gdp.urllib.request, "urlopen", MagicMock(side_effect=Exception("connection refused"))
    )

    assert gdp.check_claude_wrapper_health("http://localhost:18789/v1") is False


def test_check_claude_wrapper_health_failure_on_non_200(monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status = 500
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = None
    monkeypatch.setattr(gdp.urllib.request, "urlopen", MagicMock(return_value=mock_resp))

    assert gdp.check_claude_wrapper_health("http://localhost:18789/v1") is False


def test_check_claude_wrapper_health_missing_base_url(monkeypatch):
    monkeypatch.delenv("CLAUDE_WRAPPER_BASE_URL", raising=False)
    assert gdp.check_claude_wrapper_health(None) is False


def test_check_claude_wrapper_health_invalid_url():
    assert gdp.check_claude_wrapper_health("invalid-url") is False


# ---- select_provider ----

def test_select_provider_chooses_claude_when_healthy(monkeypatch):
    monkeypatch.setattr(gdp, "check_claude_wrapper_health", lambda: True)
    monkeypatch.setenv("CLAUDE_WRAPPER_BASE_URL", "http://localhost:18789/v1")
    monkeypatch.setenv("CLAUDE_WRAPPER_API_KEY", "test-claude-key")
    monkeypatch.setattr(gdp, "OpenAI", MagicMock())

    provider, name = gdp.select_provider()

    assert isinstance(provider, gdp.ClaudeProvider)
    assert name == "claude"


def test_select_provider_chooses_gemini_fallback_when_unhealthy(monkeypatch):
    monkeypatch.setattr(gdp, "check_claude_wrapper_health", lambda: False)
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    monkeypatch.setattr(gdp.genai, "Client", MagicMock())

    provider, name = gdp.select_provider()

    assert isinstance(provider, gdp.GeminiProvider)
    assert name == "gemini-fallback"


def test_select_provider_exits_when_claude_missing_api_key(monkeypatch):
    monkeypatch.setattr(gdp, "check_claude_wrapper_health", lambda: True)
    monkeypatch.setenv("CLAUDE_WRAPPER_BASE_URL", "http://localhost:18789/v1")
    monkeypatch.delenv("CLAUDE_WRAPPER_API_KEY", raising=False)

    with pytest.raises(SystemExit):
        gdp.select_provider()


def test_select_provider_exits_when_claude_missing_base_url(monkeypatch):
    monkeypatch.setattr(gdp, "check_claude_wrapper_health", lambda: True)
    monkeypatch.delenv("CLAUDE_WRAPPER_BASE_URL", raising=False)
    monkeypatch.setenv("CLAUDE_WRAPPER_API_KEY", "test-claude-key")

    with pytest.raises(SystemExit):
        gdp.select_provider()


def test_select_provider_exits_when_gemini_missing_api_key(monkeypatch):
    monkeypatch.setattr(gdp, "check_claude_wrapper_health", lambda: False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(SystemExit):
        gdp.select_provider()


# ---- main / provider consistency ----

def test_main_uses_same_provider_for_post_and_slug(monkeypatch, tmp_path):
    mock_provider = MagicMock(spec=["generate"])
    monkeypatch.setattr(gdp, "select_provider", lambda: (mock_provider, "claude"))
    monkeypatch.setattr(gdp, "fetch_rss_items", lambda: ["- Title: A\n"])

    mock_generate_blog_post = MagicMock(return_value='---\ntitle: "Sample Title"\n---\nBody')
    mock_generate_slug = MagicMock(return_value="sample-title")
    mock_save_post = MagicMock(return_value="Sample Title")

    monkeypatch.setattr(gdp, "generate_blog_post", mock_generate_blog_post)
    monkeypatch.setattr(gdp, "generate_slug", mock_generate_slug)
    monkeypatch.setattr(gdp, "save_post", mock_save_post)

    out_file = tmp_path / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))

    gdp.main()

    mock_generate_blog_post.assert_called_once_with(mock_provider, ["- Title: A\n"])
    mock_generate_slug.assert_called_once_with(mock_provider, "Sample Title")
    mock_save_post.assert_called_once_with('---\ntitle: "Sample Title"\n---\nBody', "sample-title")

    output_content = out_file.read_text()
    assert "post_title=Sample Title\n" in output_content
    assert "used_provider=claude\n" in output_content
