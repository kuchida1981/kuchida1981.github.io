## 1. Taxonomy 設定

- [x] 1.1 `config.yml` に `taxonomies` セクションを追加する（`tag: tags`, `category: categories`, `author: author` を明示定義。単数形 `author` を使用し既存 front matter との互換性を確保）

## 2. テンプレートオーバーライド

- [x] 2.1 `layouts/partials/post_meta.html` をオーバーライドし、`.GetTerms "author"` で author 名を `/author/<slug>/` へのリンクとして表示する（テーマの `post_meta.html` をオーバーライド）

## 3. 動作確認

- [x] 3.1 Hugo ビルドが成功し、`/author/` ページと `/author/ghost-writer/` ページが生成されることを確認
- [x] 3.2 記事ページの author 名が `/author/ghost-writer/` へのリンクになっていることを確認
- [x] 3.3 既存の `/tags/` と `/categories/` ページが引き続き正常に表示されることを確認
