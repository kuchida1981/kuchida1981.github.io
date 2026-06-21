# Capability: Google Analytics (GA4) Integration

## Purpose
サイトへのアクセス状況（ページビュー数、流入経路、滞在時間など）を把握し、コンテンツの改善判断やデータドリブンなサイト運営を可能にする。

## Requirements

### Requirement: 本番環境での GA4 トラッキングスクリプト挿入
全ページの `<head>` に GA4 の gtag.js スクリプトが挿入されなければならない（SHALL）。スクリプトの挿入は本番ビルド（`hugo.IsProduction = true`）のときのみ行われる。

#### Scenario: 本番ビルドで全ページに gtag.js が出力される
- **WHEN** `hugo build`（本番環境）を実行する
- **THEN** 生成されたすべての HTML ファイルの `<head>` に gtag.js の `<script>` タグが含まれる

#### Scenario: 開発サーバーでは gtag.js が出力されない
- **WHEN** `hugo server` でローカルサーバーを起動する
- **THEN** 生成された HTML の `<head>` に gtag.js の `<script>` タグが含まれない

### Requirement: GA4 測定 ID の一元管理
GA4 の測定 ID は `config.yml` の `Params.googleAnalyticsID` で管理されなければならず（SHALL）、テンプレートはこの値を参照する。

#### Scenario: 測定 ID が config.yml に定義されている
- **WHEN** `config.yml` の `Params.googleAnalyticsID` に測定 ID が設定されている
- **THEN** 生成される gtag.js スクリプト内の測定 ID がその値と一致する

### Requirement: テーマファイルへの非干渉
GA4 の統合は `themes/` 配下のファイルを変更せず、`layouts/partials/extend_head.html` のオーバーライドのみで実装されなければならない（SHALL）。

#### Scenario: テーマ更新後も GA トラッキングが維持される
- **WHEN** `themes/papermod/` を更新する
- **THEN** `layouts/partials/extend_head.html` は変更されず、GA トラッキングは引き続き機能する

