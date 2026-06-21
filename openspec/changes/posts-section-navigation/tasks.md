## 1. Archives ページの廃止

- [ ] 1.1 `content/archives.md` を削除する
- [ ] 1.2 `config.yml` のメニュー定義から `archives` エントリを削除する

## 2. ナビゲーション partial の作成

- [ ] 2.1 `layouts/partials/posts_nav.html` を作成する。Categories（全件・件数付き）、Tags（上位15件 + 全タグリンク）、Archives（年月リンク）を含むナビゲーションブロックを実装する

## 3. Posts セクションのテンプレートオーバーライド

- [ ] 3.1 `layouts/posts/list.html` を作成する。PaperMod の `themes/papermod/layouts/_default/list.html` をベースにコピーし、ページネーションの下に `{{ partial "posts_nav.html" . }}` を追加する
- [ ] 3.2 `layouts/posts/single.html` を作成する。PaperMod の `themes/papermod/layouts/_default/single.html` をベースにコピーし、post-footer の下・comments の前に `{{ partial "posts_nav.html" . }}` を追加する

## 4. 動作確認

- [ ] 4.1 `hugo` ビルドがエラーなく完了することを確認する
- [ ] 4.2 `/posts/` にナビゲーションブロックが表示され、カテゴリ・タグ・年月リンクが正しいURLに遷移することを確認する
- [ ] 4.3 個別記事ページにナビゲーションブロックが表示されることを確認する
- [ ] 4.4 `/services/` にナビゲーションブロックが表示されないことを確認する
- [ ] 4.5 `/archives/` が存在しないこと（404）を確認する
