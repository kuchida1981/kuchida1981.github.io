## 1. サイト全体設定（robots.txt / description）

- [x] 1.1 `config.yml` に `enableRobotsTXT: true` を追加する
- [x] 1.2 `config.yml` の `Params.description` を `Sandbox` から確定した説明文（「バックエンド・インフラを中心に活動するフリーランスエンジニアの個人ブログ。技術的な試行錯誤の記録から日々のニュース、ときにフィクションまで。」）に変更する
- [x] 1.3 ローカルで `hugo` ビルドし、`docs/robots.txt` が生成され `Sitemap:` 行を含むこと、`docs/index.html` の `<meta name="description">` とJSON-LDの `description` が新しい説明文になっていることを確認する

## 2. 関連記事機能

- [x] 2.1 `config.yml` に `related` ブロックを追加し、`tags` の重みを `categories` より高く設定する
- [x] 2.2 `layouts/posts/single.html` の記事フッター（タグ一覧の直後、`post_nav_links` の前）に、`.Site.RegularPages.Related` を用いた「関連記事」セクション（上位5件、0件時はセクション自体を非表示）を追加する
- [x] 2.3 ローカルで `hugo` ビルドし、タグを共有する記事同士で関連記事が表示されること、関連記事が見つからない記事ではセクションが表示されないことを確認する

## 3. IndexNow通知

- [x] 3.1 IndexNow用のキー文字列を生成し、`static/<key>.txt`（中身はキー文字列のみ）として追加する
- [x] 3.2 `.github/workflows/hugo.yaml` に、`push` イベントかつ `content/posts/` 配下の変更を含む場合にのみ実行されるIndexNow通知ステップを追加する。`github.event.before`/`github.event.after` 間の diff から追加・変更されたポストファイルを特定し、Hugoのパーマリンク規則でURLへ変換してIndexNowエンドポイントへ送信する。`continue-on-error: true` を設定する
- [x] 3.3 `schedule` / `workflow_dispatch` / `pull_request` トリガー時や `content/posts/` に変更が無い場合には通知ステップが実行されない(または即終了する)ことをワークフロー定義上で確認する

## 4. 最終確認

- [ ] 4.1 `hugo --gc --minify` でのフルビルドが成功することを確認する
- [ ] 4.2 変更差分一式をレビューし、コミットする
