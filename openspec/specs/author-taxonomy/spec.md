## ADDED Requirements

### Requirement: Author taxonomy が有効であること
Hugo の taxonomy として `authors` が定義されており、`/author/` および `/author/<name>/` ページが自動生成される。

#### Scenario: Author 一覧ページが存在する
- **WHEN** `/author/` にアクセスする
- **THEN** すべての author の一覧が表示される

#### Scenario: 特定 author の記事一覧ページが存在する
- **WHEN** `/author/ghost-writer/` にアクセスする
- **THEN** `author: "Ghost Writer"` を持つ記事の一覧が表示される

#### Scenario: 既存の tags/categories taxonomy が維持される
- **WHEN** `taxonomies` を明示定義した後
- **THEN** `/tags/` および `/categories/` ページが引き続き正常に表示される

### Requirement: 記事ページの author 名が taxonomy ページへリンクすること
記事ページに表示される author 名は、対応する `/author/<slug>/` ページへのリンクとして表示される。

#### Scenario: 単一 author の記事でリンクが表示される
- **WHEN** `author: "Ghost Writer"` を持つ記事ページを表示する
- **THEN** author 名 "Ghost Writer" が `/author/ghost-writer/` へのリンクとして表示される

#### Scenario: author が未指定の場合はサイトデフォルトが使われる
- **WHEN** 記事の front matter に `author` が未指定で、`config.yml` に `Params.author` が設定されている
- **THEN** サイトデフォルトの author 名がリンクなしで表示される（taxonomy に登録されていないため）
