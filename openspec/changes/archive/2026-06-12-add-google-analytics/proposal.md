## Why

サイトへのアクセス状況（ページビュー数、流入経路、滞在時間など）を把握する手段がなく、コンテンツの改善判断が感覚頼りになっている。Google Analytics 4 を導入してデータドリブンなサイト運営を可能にする。

## What Changes

- `config.yml` に GA4 測定 ID（`G-QSVPG0XQ59`）を追記
- `layouts/partials/extend_head.html` を新規作成し、gtag.js スクリプトを挿入
- 本番環境のみ計測（`hugo.IsProduction` によるガード）、開発サーバーでは計測しない

## Capabilities

### New Capabilities

- `google-analytics`: Hugo + PaperMod サイトへの GA4 トラッキングスクリプトの組み込み。本番ビルド時のみ `<head>` にスクリプトが出力される。

### Modified Capabilities

（なし）

## Impact

- 変更ファイル: `config.yml`（数行追記）、`layouts/partials/extend_head.html`（新規作成）
- `themes/` 配下は一切変更しないため、テーマ更新の影響を受けない
- 生成される HTML の `<head>` に gtag.js スクリプトが追加される（本番のみ）
- 外部依存: `https://www.googletagmanager.com` への非同期リクエストが発生
