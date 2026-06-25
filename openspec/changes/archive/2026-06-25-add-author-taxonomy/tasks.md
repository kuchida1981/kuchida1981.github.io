## 1. Taxonomy 設定

- [x] 1.1 `config.yml` に `taxonomies` セクションを追加する（`tag: tags`, `category: categories`, `author: author` を明示定義。単数形 `author` を使用し既存 front matter との互換性を確保）

## 2. テンプレートオーバーライド

- [x] 2.1 `layouts/partials/author.html` を作成し、author 名を `/author/<slug>/` へのリンクとして表示する（テーマの `author.html` をオーバーライド。単数文字列・リスト両方に対応）

## 3. 動作確認

- [x] 3.1 Hugo ビルドが成功し、`/author/` ページと `/author/ghost-writer/` ページが生成されることを確認
- [x] 3.2 記事ページの author 名が `/author/ghost-writer/` へのリンクになっていることを確認
- [x] 3.3 既存の `/tags/` と `/categories/` ページが引き続き正常に表示されることを確認
