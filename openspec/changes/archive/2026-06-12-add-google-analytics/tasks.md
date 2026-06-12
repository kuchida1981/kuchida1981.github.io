## 1. 設定ファイルの更新

- [x] 1.1 `config.yml` の `Params` セクションに `googleAnalyticsID: "G-QSVPG0XQ59"` を追記する

## 2. テンプレートの作成

- [x] 2.1 `layouts/partials/extend_head.html` を新規作成し、`hugo.IsProduction` ガード付きの gtag.js スクリプトを記述する

## 3. 動作確認

- [x] 3.1 `hugo server` でローカルサーバーを起動し、生成された HTML に gtag.js スクリプトが含まれないことを確認する
- [x] 3.2 `hugo` でプロダクションビルドを実行し、`docs/` 配下の HTML に gtag.js スクリプトが含まれることを確認する

## 4. デプロイ

- [ ] 4.1 変更をコミットして master ブランチにプッシュする
