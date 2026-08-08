import datetime
import importlib
from types import SimpleNamespace
from unittest.mock import MagicMock

import generate_daily_post as gdp


def test_import_does_not_require_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    importlib.reload(gdp)


# ---- sanitize_slug ----

def test_sanitize_slug_converts_spaces_and_lowercases():
    assert gdp.sanitize_slug("Hello World") == "THIS SHOULD FAIL"


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
    client = MagicMock()
    client.models.generate_content.return_value = SimpleNamespace(text="Generated post body")

    result = gdp.generate_blog_post(client, ["- Title: Example News\n"])

    assert result == "Generated post body"
    _, kwargs = client.models.generate_content.call_args
    assert kwargs["model"] == "gemini-2.5-flash"
    assert "Example News" in kwargs["contents"]


# ---- generate_slug ----

def test_generate_slug_sanitizes_successful_response():
    client = MagicMock()
    client.models.generate_content.return_value = SimpleNamespace(text="Adobe AI Agents")

    assert gdp.generate_slug(client, "Some Title") == "adobe-ai-agents"


def test_generate_slug_falls_back_on_empty_response():
    client = MagicMock()
    client.models.generate_content.return_value = SimpleNamespace(text="")

    assert gdp.generate_slug(client, "Some Title") == "daily-news"


def test_generate_slug_falls_back_on_exception():
    client = MagicMock()
    client.models.generate_content.side_effect = RuntimeError("api error")

    assert gdp.generate_slug(client, "Some Title") == "daily-news"
