## 1. スクリプト修正

- [x] 1.1 `scripts/generate_daily_post.py` の `save_post()` に author フィールド補完ロジックを追加する。frontmatter 内に `author:` 行が存在しない場合、閉じ `---` の直前に `author: "Ghost Writer"` を挿入する。既存の title 抽出（93-94行目）の近くに追加する。

## 2. 既存記事の修正

- [x] 2.1 `content/posts/2026-06-19-daily-news.md` の frontmatter に `author: "Ghost Writer"` を追加する。
