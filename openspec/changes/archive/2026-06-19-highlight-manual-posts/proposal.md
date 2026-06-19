## Why

現在、ブログ記事は手動で作成されたものと、GitHub Actionsで毎日Geminiにより自動生成されたものが混在しています。読者および管理者にとって、どの記事が手作業によるもの（本人の意見）で、どれがAIアシスタントによって自動生成されたもの（ニュースの要約等）かを視覚的に区別しやすくする必要があります。

## What Changes

- **AI記事の著者設定**: Daily Automated Postによって自動生成される記事のフロントマターに `author: "Ghost Writer"` を追加します。
- **手動記事のハイライト**: 記事一覧ページにおいて、手動で書かれた記事（`author` が指定されていない、または `author` が自分自身の名前であるもの）に特別なクラスを付与し、背景色をハイライト表示します。
- **ダークモード対応**: ハイライトの背景色は、ブログの既存テーマ（PaperMod）のダークモード・ライトモードそれぞれに調和するものを採用します。

## Capabilities

### New Capabilities

<!-- なし -->

### Modified Capabilities

- `blog`: 記事の著者を区別し、手動記事を一覧ページでハイライト表示する要件を追加します。

## Impact

- `scripts/generate_daily_post.py` (AI記事のフロントマターテンプレートを変更)
- `layouts/_default/list.html` (各記事カード Durations/クラス設定を変更)
- `layouts/partials/extend_head.html` または `assets/css/extended/` 配下 (ハイライト用のカスタムCSSを追加)
