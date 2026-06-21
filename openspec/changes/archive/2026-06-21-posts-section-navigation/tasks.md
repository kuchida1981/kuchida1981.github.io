## 1. Archives ページの廃止

- [x] 1.1 `content/archives.md` を削除する
- [x] 1.2 `config.yml` のメニュー定義から `archives` エントリを削除する

## 2. ナビゲーション partial の作成

- [x] 2.1 `layouts/partials/posts_nav.html` を作成する。Categories（全件・件数付き）、Tags（上位15件 + 全タグリンク）、Archives（年月リンク）を含むナビゲーションブロックを実装する

## 3. Posts セクションのテンプレートオーバーライド

- [x] 3.1 `layouts/posts/list.html` を作成する。PaperMod の `themes/papermod/layouts/_default/list.html` をベースにコピーし、ページネーションの下に `{{ partial "posts_nav.html" . }}` を追加する
- [x] 3.2 `layouts/posts/single.html` を作成する。PaperMod の `themes/papermod/layouts/_default/single.html` をベースにコピーし、post-footer の下・comments の前に `{{ partial "posts_nav.html" . }}` を追加する

## 4. セクションページの生成（年月アーカイブリンク先の404対応）

- [x] 4.1 既存の年/月ディレクトリ（`content/posts/2026/01` 〜 `2026/06`）に `_index.md` を追加し、Hugo がセクションページを生成するようにする
- [x] 4.2 `scripts/generate_daily_post.py` の `save_post` 関数で、新しい月のディレクトリ作成時に `_index.md` も自動生成するようにする

## 5. 動作確認

- [x] 5.1 `hugo` ビルドがエラーなく完了することを確認する
- [x] 5.2 `/posts/` にナビゲーションブロックが表示され、カテゴリ・タグ・年月リンクが正しいURLに遷移することを確認する
- [x] 5.3 個別記事ページにナビゲーションブロックが表示されることを確認する
- [x] 5.4 `/services/` にナビゲーションブロックが表示されないことを確認する
- [x] 5.5 `/archives/` が存在しないこと（404）を確認する
