## Why

サイトの実装を調査した結果、Googleなどの検索エンジンにインデックスされる上でのギャップが複数見つかった。特に、`robots.txt` が未生成、サイト全体の meta description が仮の値（`Sandbox`）のまま公開されている、193本の記事のうち他記事へリンクしているものが0件という状態は、いずれも設定変更や小規模なテンプレート追加で改善できる。Google Search Console の登録とドメイン所有権のTXTレコード検証は既に対応済みで、残る現実的な施策を今回まとめて適用する。

## What Changes

- Hugo の `enableRobotsTXT: true` を有効化し、`robots.txt` を生成する（テーマ側テンプレートは対応済みで、`Sitemap:` 行も自動出力される）
- サイト全体の `description`（meta description および JSON-LD の description に反映される）を、実態に即した内容に差し替える
- 個別記事ページに、Hugo の Related Content 機能（`.RegularPages.Related`）を用いた「関連記事」セクションを追加する。tags/categories の重み付けは `config.yml` の `related:` ブロックで設定する。既存記事の本文を書き換えることなく、既存記事・新規記事の両方に自動的に内部リンクを提供する
- GitHub Actions のデプロイフロー（`hugo.yaml`）に、公開/更新された記事URLをIndexNowエンドポイントへ通知するステップを追加する。`static/` にIndexNow用のキーファイルを1つ配置する

## Capabilities

### New Capabilities
- `seo-indexing`: 検索エンジンによるクロール・インデックスを促進するためのサイト全体設定（robots.txt生成、サイト説明文、IndexNow通知）を扱う
- `related-posts`: 個別記事ページに tags/categories ベースで算出した関連記事へのリンクを表示する機能を扱う

### Modified Capabilities
(なし。既存の `blog` および `posts-navigation` の要件は変更しない)

## Impact

- `config.yml`: `enableRobotsTXT: true` の追加、`Params.description` の変更、`related:` ブロックの追加
- `layouts/posts/single.html`: 関連記事セクションの追加（テーマ本体は変更しない）
- `.github/workflows/hugo.yaml`: デプロイ後にIndexNow通知ステップを追加
- `static/`: IndexNow検証用キーファイルを新規追加
- 影響範囲はビルド設定とテンプレートのみで、既存記事の内容・URL構造には影響しない
