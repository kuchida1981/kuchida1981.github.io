## Why

記事本文で `#`（h1）を使うと記事タイトルと同じフォントサイズ（40px）になり、視覚的な区別がつかない。見た目のために `##` から書き始めることを強いられるが、これは Markdown のセマンティクスに反する。h1〜h3 のサイズを段階的に下げ、記事タイトルとの差を作ることで自然な執筆体験を回復する。

## What Changes

- `assets/css/extended/custom.css` に `.post-content h1 / h2 / h3` のフォントサイズ上書きを追記する
  - h1: 40px → 32px
  - h2: 32px → 24px
  - h3: 24px → 20px
- 記事タイトル（`.post-title`、40px）は変更しない
- h4〜h6 は使用しない運用のため変更しない

## Capabilities

### New Capabilities

なし

### Modified Capabilities

- `blog`: 記事本文の見出しサイズが変更される（ビジュアル要件の変更）

## Impact

- 影響ファイル: `assets/css/extended/custom.css`（1ファイルのみ）
- 既存記事の見た目が変わる（`#` を使っている記事では h1 が小さくなる）
- テーマファイル（`themes/papermod/`）は触らないため、テーマ更新の影響を受けない
