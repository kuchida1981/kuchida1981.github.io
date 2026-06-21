## 1. Hugo テンプレート修正

- [x] 1.1 `layouts/_default/list.html` の41行目 `$pages := union .RegularPages .Sections` を `$pages := .RegularPagesRecursive` に変更

## 2. 自動投稿スクリプト修正

- [x] 2.1 `scripts/generate_daily_post.py` の `save_post` 関数で出力パスを `content/posts/YYYY/MM/YYYY-MM-DD-daily-news.md` に変更し、`os.makedirs(exist_ok=True)` でディレクトリを自動作成

## 3. 既存記事の移動

- [x] 3.1 `content/posts/` 直下の `YYYY-MM-DD-*.md` ファイルを `content/posts/YYYY/MM/` に一括移動（hello-world.md はスキップ）

## 4. 動作確認

- [x] 4.1 `hugo` ビルドが成功することを確認
- [x] 4.2 記事一覧ページに全記事が表示されることを確認
