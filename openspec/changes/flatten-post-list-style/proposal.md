## Why

記事一覧（Posts）のカード型レイアウトが視覚的に重く、よりシンプルでフラットな見た目にしたい。現在はカード背景色（ライト: 白、ダーク: グレー）とページ背景色の差でカードを浮かせているが、この装飾を廃止してフラットなリストにする。併せて、ユーザー作成記事の強調方法も背景色ベースから左ボーダーアクセントに変更する。

## What Changes

- 記事一覧ページ `.list` の背景色指定（`--code-bg` / `--theme`）を削除
- `.post-entry` のカード背景色（`var(--entry)`）、枠線（`var(--border)`）、角丸（`var(--radius)`）を削除
- ユーザー作成記事の強調表現を背景色ハイライトから左ボーダー（`border-left`）に変更
- 記事間の区切りをカード枠から余白（margin/padding）に変更

## Capabilities

### New Capabilities

（なし）

### Modified Capabilities

- `blog`: 「Highlight Manual Posts」の要件を変更 — 背景色ハイライトから左ボーダーアクセントによる視覚的区別に変更

## Impact

- `themes/papermod/assets/css/core/theme-vars.css` — `.list` / `.dark.list` 背景色削除
- `themes/papermod/assets/css/common/post-entry.css` — `.post-entry` のカードスタイル削除
- `assets/css/extended/custom.css` — `.post-self` スタイルを左ボーダーに置換
- `layouts/_default/list.html` — 変更なし（`post-self` クラスの付与ロジックはそのまま利用）
