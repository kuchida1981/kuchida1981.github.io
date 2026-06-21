## Context

`scripts/generate_daily_post.py` は Gemini API でブログ記事を生成し、`save_post()` で frontmatter ごとファイルに保存する。プロンプトに `author: "Ghost Writer"` を含めているが、LLM の出力は非決定的であり、frontmatter から author が省略されるケースがある。現在の `save_post()` は title の抽出以外に frontmatter の検証を行っていない。

## Goals / Non-Goals

**Goals:**
- `save_post()` で frontmatter の `author` フィールドの存在を検証し、欠落時に `"Ghost Writer"` を補完する
- 既存の欠落記事（2026-06-19）を修正する

**Non-Goals:**
- author 以外の frontmatter フィールド（tags, categories, date）の検証は今回スコープ外
- プロンプトの改善（LLM 側の出力精度向上）は行わない
- frontmatter パーサーライブラリの導入は行わない（既存の正規表現ベースで十分）

## Decisions

### D1: frontmatter の author 補完を正規表現で行う

`save_post()` は既に正規表現で `title` を抽出している（93-94行目）。同じアプローチで `author` の有無をチェックし、なければ frontmatter ブロック内に挿入する。

**代替案:** PyYAML や python-frontmatter ライブラリで構造的にパース → 依存追加が不要な正規表現の方がシンプル。frontmatter の構造は単純（フラットな key-value）なので正規表現で十分。

### D2: 挿入位置は frontmatter 末尾（`---` の直前）

author 行が存在しない場合、閉じ `---` の直前に `author: "Ghost Writer"` を挿入する。既存の frontmatter のキー順序を壊さない。

## Risks / Trade-offs

- [Risk] 正規表現が frontmatter 外の `---` にマッチする可能性 → Mitigation: `save_post()` は先頭の `---` 以降を取得済み。2つ目の `---` を frontmatter 終端として扱えば安全。
- [Trade-off] author 以外のフィールド欠落は検知しない → 今回は author のみにスコープを限定し、他フィールドの問題が発生した時点で拡張する。
