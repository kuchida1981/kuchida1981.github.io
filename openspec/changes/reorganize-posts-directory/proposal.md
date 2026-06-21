## Why

content/posts/ に139件の記事がフラットに並んでおり、毎日1件ペースで増加するため年末には350件超になる。ファイル管理が困難になる前に年月階層（YYYY/MM/）で整理する。

## What Changes

- 既存の daily-news 記事138件を `content/posts/YYYY/MM/` ディレクトリに移動
- `generate_daily_post.py` の出力パスを `content/posts/YYYY/MM/` 形式に変更
- `layouts/_default/list.html` でサブディレクトリ内の記事も一覧表示されるよう修正
- hello-world.md は `content/posts/` 直下に残す
- URL は変更を許容（permalinks 設定は追加しない）
- 年月インデックスページ（_index.md）は作成しない

## Capabilities

### New Capabilities

なし

### Modified Capabilities

- `blog`: 記事のディレクトリ構造が変わる。自動投稿の出力先が `content/posts/YYYY/MM/` になり、記事一覧がサブディレクトリを再帰的に取得するよう変更。

## Impact

- **layouts/_default/list.html**: `.RegularPages` → `.RegularPagesRecursive` に変更
- **scripts/generate_daily_post.py**: 出力パスとディレクトリ作成ロジックの変更
- **content/posts/**: 138件のファイル移動、6ディレクトリ（年1 × 月6）の新規作成
- **URL**: 既存記事の URL が `/posts/YYYY-MM-DD-daily-news/` → `/posts/YYYY/MM/YYYY-MM-DD-daily-news/` に変更
