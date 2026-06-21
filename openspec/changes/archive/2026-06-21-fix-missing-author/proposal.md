## Why

Gemini による自動生成記事の frontmatter に `author: "Ghost Writer"` が含まれないケースがある。プロンプトで指定しているが LLM の出力は非決定的であり、省略される場合がある。137件中1件（2026-06-19）で実際に欠落が発生し、手動修正（PR #196）が必要になった。author フィールドは「手動記事と自動記事の視覚的区別」機能の基盤であり、欠落すると手動記事として誤表示される。

## What Changes

- `scripts/generate_daily_post.py` の `save_post()` に frontmatter の post-process 処理を追加し、`author` フィールドがなければ `"Ghost Writer"` を補完する
- 既にマージ済みの `content/posts/2026-06-19-daily-news.md` に `author: "Ghost Writer"` を追加する

## Capabilities

### New Capabilities

（なし）

### Modified Capabilities

- `blog`: 自動生成記事の author フィールドを LLM 出力に依存せず、post-process で確実に設定する保証を追加

## Impact

- `scripts/generate_daily_post.py`: `save_post()` 関数に frontmatter パース・補完ロジックを追加
- `content/posts/2026-06-19-daily-news.md`: author フィールドの追加
