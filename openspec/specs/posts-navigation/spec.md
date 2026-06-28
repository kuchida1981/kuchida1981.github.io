# posts-navigation Specification

## Purpose
Posts セクション内のページにカテゴリ・タグ・年月アーカイブへのナビゲーションブロックを提供する。

## Requirements
### Requirement: Posts Section Navigation Block
Posts セクション内の全ページ（記事一覧ページおよび個別記事ページ）の下部に、カテゴリ・タグ・年月アーカイブへのナビゲーションブロックを表示する SHALL。ナビゲーションは `layouts/partials/posts_nav.html` として実装し、Posts セクション専用のテンプレートオーバーライドから呼び出す。

#### Scenario: Navigation appears on post list page
- **WHEN** ユーザーが記事一覧ページ (`/posts/`) にアクセスする
- **THEN** ページネーションの下にナビゲーションブロックが表示される

#### Scenario: Navigation appears on individual post page
- **WHEN** ユーザーが個別記事ページ (`/posts/YYYY/MM/slug/`) にアクセスする
- **THEN** 記事フッター（タグ・前後リンク）の下にナビゲーションブロックが表示される

#### Scenario: Navigation does not appear on non-Posts pages
- **WHEN** ユーザーが Posts セクション以外のページ (`/services/` など) にアクセスする
- **THEN** ナビゲーションブロックは表示されない

### Requirement: Category Links in Navigation
ナビゲーションブロックに、全カテゴリを件数付きリンクとして表示する SHALL。リンク先は Hugo が自動生成するタクソノミーページ (`/categories/<name>/`) とする。

#### Scenario: Displaying categories
- **WHEN** ナビゲーションブロックが表示される
- **THEN** サイトに存在する全カテゴリが件数付きリンクとして表示される
- **AND** 各リンクは `/categories/<name>/` に遷移する

### Requirement: Tag Links in Navigation
ナビゲーションブロックに、記事件数の多い上位15件のタグをリンクとして表示する SHALL。全タグ一覧ページ (`/tags/`) へのリンクも併せて表示する。

#### Scenario: Displaying top tags
- **WHEN** ナビゲーションブロックが表示される
- **THEN** 記事件数の多い上位15件のタグがリンクとして表示される
- **AND** 各リンクは `/tags/<name>/` に遷移する

#### Scenario: Link to all tags
- **WHEN** ナビゲーションブロックが表示される
- **THEN** 全タグ一覧ページ (`/tags/`) へのリンクが表示される

### Requirement: Archive Links in Navigation
ナビゲーションブロックに、年月別のアーカイブリンクを表示する SHALL。リンク先は Posts セクションのセクションページ (`/posts/YYYY/MM/`) とする。

#### Scenario: Displaying year-month archive links
- **WHEN** ナビゲーションブロックが表示される
- **THEN** 記事が存在する年月の組み合わせがリンクとして表示される
- **AND** 各リンクは `/posts/YYYY/MM/` に遷移する
