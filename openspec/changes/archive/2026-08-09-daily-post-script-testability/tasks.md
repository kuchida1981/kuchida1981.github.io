## 1. スクリプトのリファクタリング

- [x] 1.1 `generate_daily_post.py` のトップレベルにある `GEMINI_API_KEY` チェックを `require_api_key()` 関数に切り出す
- [x] 1.2 `genai.Client` の生成をモジュールトップレベルから `main()` 内に移動する
- [x] 1.3 `generate_blog_post()` のシグネチャを `generate_blog_post(client, feed_items)` に変更し、グローバル `client`参照を廃止する
- [x] 1.4 `main()` を更新し、`require_api_key()` → `genai.Client` 生成 → 各関数への `client` 引数渡しの順に呼び出すよう修正する
- [x] 1.5 リファクタ後もロジック・出力内容（プロンプト文言、フロントマター形式）が変わっていないことをコードレビューで確認する

## 2. テスト基盤の追加

- [x] 2.1 `scripts/requirements-dev.txt` を新設し、`pytest` を最新安定版で `==` 固定して追加する
- [x] 2.2 `scripts/test_generate_daily_post.py` を新設する

## 3. テストケースの実装

- [x] 3.1 `sanitize_slug()` の境界値テスト（空白・非ASCII・7語以上・空文字結果時のフォールバック）を実装する
- [x] 3.2 `extract_title()` のテスト（フロントマターあり/なし、コードブロック付きなど）を実装する
- [x] 3.3 `save_post()` のテスト（`tmp_path` でカレントディレクトリを切り替え、ファイル生成・author補完ロジックを検証）を実装する
- [x] 3.4 `fetch_rss_items()` のテスト（`feedparser.parse` をモックし、上位5件抽出・整形ロジックを検証）を実装する
- [x] 3.5 `generate_blog_post()` のテスト（フェイク Gemini クライアントを渡し、プロンプトにRSS内容が含まれること・レスポンステキストがそのまま返ることを検証）を実装する
- [x] 3.6 `generate_slug()` のテスト（正常系のスラッグ整形、例外発生時に `daily-news` にフォールバックすることを検証）を実装する

## 4. CI 統合

- [x] 4.1 `.github/workflows/scripts-tests.yaml` を新設し、`pull_request`（master向け）と `push`（master）で `scripts/requirements.txt` と `scripts/requirements-dev.txt` をインストールしてから pytest を実行するジョブを定義する
- [x] 4.2 PR を作成し、`scripts-tests` ジョブが実際に実行され green になることを確認する
- [x] 4.3 意図的にテストを失敗させた状態で push し、CI が red になることを確認してから元に戻す

## 5. 動作確認

- [x] 5.1 マージ後、`.github/workflows/daily-post.yaml` を `workflow_dispatch` で手動実行し、リファクタ後も正常に記事が生成されることを確認する
