## 1. Taxonomy 設定

- [ ] 1.1 `config.yml` に `taxonomies` セクションを追加する（`tag: tags`, `category: categories`, `author: authors` の3つを明示定義）

## 2. テンプレートオーバーライド

- [ ] 2.1 `layouts/partials/author.html` を作成し、author 名を `/authors/<slug>/` へのリンクとして表示する（テーマの `author.html` をオーバーライド。単数文字列・リスト両方に対応）

## 3. 動作確認

- [ ] 3.1 `hugo server` でビルドが成功し、`/authors/` ページと `/authors/ghost-writer/` ページが表示されることを確認する
- [ ] 3.2 記事ページの author 名が `/authors/ghost-writer/` へのリンクになっていることを確認する
- [ ] 3.3 既存の `/tags/` と `/categories/` ページが引き続き正常に表示されることを確認する
