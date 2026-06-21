## Why

Archives が独立したページ・グローバルメニュー項目として存在しているが、その存在感に見合うほどの役割を果たしていない。カテゴリ・タグ・年月といったブラウジング導線を Posts セクション内に統合し、記事閲覧の流れの中で自然にアクセスできるようにしたい。

## What Changes

- `content/archives.md` を削除し、`config.yml` のグローバルメニューから `archives` エントリを削除
- Posts セクション内の全ページ（記事一覧・個別記事）の下部に、カテゴリ・タグ・年月アーカイブへのナビゲーションブロックを追加
- タグは件数上位N件のみ表示し、全タグ一覧（`/tags/`）へのリンクを添える
- PaperMod テーマファイルは直接編集せず、プロジェクト側の `layouts/` でオーバーライドする

## Capabilities

### New Capabilities
- `posts-navigation`: Posts セクション内ページ下部に表示するカテゴリ・タグ・年月ナビゲーションブロック

### Modified Capabilities
- `blog`: Archives ページの廃止に伴い、ブログナビゲーションの要件が変更される（グローバルメニューから Archives を削除）

## Impact

- `content/archives.md`: 削除
- `config.yml`: メニュー定義から archives エントリを削除
- `layouts/partials/posts_nav.html`: 新規作成（ナビゲーション partial）
- `layouts/posts/list.html`: 新規作成（PaperMod の `_default/list.html` をオーバーライド）
- `layouts/posts/single.html`: 新規作成（PaperMod の `_default/single.html` をオーバーライド）
- Hugo の既存タクソノミーページ（`/categories/`, `/tags/`）とセクションページ（`/posts/YYYY/MM/`）をリンク先として活用（これらのページ自体は変更なし）
