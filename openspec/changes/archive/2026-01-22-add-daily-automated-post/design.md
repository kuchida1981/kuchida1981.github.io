# Design: Daily Automated Post

## Context
We need a system to automatically draft blog posts based on recent news. The project already uses GitHub Actions.

## Goals
- Automate the creation of a Markdown file for a blog post.
- Use Gemini to source content (recent news) and write the post.
- Create a PR for review (no direct commit to master).
- Run daily.

## Decisions

### 1. Scripting Language: Python
- **Decision**: Use Python for the generation script.
- **Why**: Excellent support for `google-generativeai` SDK and string manipulation.
- **Location**: `scripts/generate_daily_post.py`.

### 2. Content Generation: Gemini API
- **Decision**: Use Google's Gemini API via `google-generativeai` library.
- **Topic Selection**: The script will ask the model to "find a recent interesting tech or general news topic from today/yesterday" and write about it. We will rely on the model's training or built-in search grounding capabilities (if configured) to find "current" news, or we might need to feed it a news RSS feed if the model's knowledge cutoff is an issue.
- *Refinement*: To ensure freshness, we will use the `google-generativeai` library. If the specific model version supports search grounding, we will enable it. Otherwise, the prompt will ask for "timeless" or "recently popular" topics that the model is aware of, or we can fetch top headlines from an RSS feed (e.g., Hacker News, BBC) using `feedparser` and pass them to Gemini as context.
- **Selected Approach**: Fetch RSS feeds (e.g., Hacker News, GitHub Trending, major Tech News) -> Summarize/Select one with Gemini -> Generate Post. This ensures the news is actually recent.

### 3. Workflow: GitHub Actions
- **Trigger**: `schedule` (cron: `0 0 * * *` - daily at midnight UTC).
- **Steps**:
    1.  Checkout code.
    2.  Setup Python.
    3.  Install dependencies (`feedparser`, `google-generativeai`).
    4.  Run script (outputs `content/posts/...`).
    5.  Create PR using `peter-evans/create-pull-request`.

## Risks
- **Model Hallucination**: Model might invent news.
    - *Mitigation*: Use RSS feeds as the source of truth/context.
- **API Costs**: Gemini API usage.
    - *Mitigation*: It's low volume (1/day).
- **Git Conflicts**: If file naming isn't unique.
    - *Mitigation*: Use timestamp in filename.

## Open Questions
- Specific RSS feeds to use? (Start with a generic tech mix).
