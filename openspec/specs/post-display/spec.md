# post-display Specification

## Purpose
TBD - created by archiving change enable-posts. Update Purpose after archive.
## Requirements
### Requirement: 記事一覧へのアクセス
ユーザーはサイトのメニューから記事一覧ページへアクセスできる必要があります (MUST)。

#### Scenario: メニュークリック
Given ユーザーがトップページを表示している
When "Posts" (または "Blog") メニューをクリックする
Then 記事一覧ページが表示される

### Requirement: 記事の表示
`content/posts` ディレクトリに配置された Markdown ファイルは、サイト上で記事としてレンダリングされなければなりません (MUST)。

#### Scenario: 記事詳細表示
Given `content/posts/hello-world.md` が存在する
When 記事一覧から "Hello World" 記事をクリックする
Then 記事の詳細ページが表示される

