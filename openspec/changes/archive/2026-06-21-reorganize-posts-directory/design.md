## Context

content/posts/ に139件の記事ファイルがフラットに配置されている。毎日 Gemini が自動生成する daily-news 記事が1件ずつ増え、年末には350件を超える見込み。Hugo v0.145、テーマは PaperMod。

現在の記事一覧は `layouts/_default/list.html` で `union .RegularPages .Sections` を使っており、直下のページとサブセクションを表示している。

## Goals / Non-Goals

**Goals:**
- 記事を `content/posts/YYYY/MM/` の年月階層で管理する
- 既存138件の daily-news 記事を正しいディレクトリに移動する
- 自動投稿スクリプトが新しい階層に記事を出力する
- 記事一覧がサブディレクトリ配下を含めて正しく表示される

**Non-Goals:**
- URL の後方互換性維持（permalinks 設定追加はしない）
- 年月ごとのインデックスページ（_index.md）の作成
- hello-world.md の移動（content/posts/ 直下に残す）
- ファイル名フォーマットの変更（YYYY-MM-DD-daily-news.md のまま）

## Decisions

### 1. 一覧表示に `.RegularPagesRecursive` を使用

`union .RegularPages .Sections` を `.RegularPagesRecursive` に置き換える。

- **理由**: サブディレクトリに移動した記事を `/posts/` 一覧で全件表示するため
- **代替案**: `.Pages` で再帰的に取得する方法もあるが、Hugo v0.121+ では `.RegularPagesRecursive` が明示的で推奨
- **影響**: `.Sections`（サブセクション自体へのリンク）は表示されなくなるが、年月インデックスは不要なので問題ない

### 2. ディレクトリ作成に `os.makedirs(exist_ok=True)` を使用

`save_post` 関数で出力先ディレクトリを自動作成する。

- **理由**: GitHub Actions 環境では `content/posts/YYYY/MM/` が存在しない場合がある（新しい月の初日）
- **代替案**: ワークフロー側で `mkdir -p` する方法もあるが、スクリプト内で完結させた方がシンプル

### 3. 既存記事の移動はファイル名の日付部分から年月を抽出

ファイル名 `YYYY-MM-DD-daily-news.md` の先頭8文字から年（1-4）と月（6-7）を抽出し、対応するディレクトリに移動する。

- **理由**: front matter の解析より確実かつ高速
- **対象外**: `hello-world.md` のように日付プレフィックスを持たないファイルはスキップ

## Risks / Trade-offs

- **URL変更による外部リンク切れ** → 検索エンジンからのリンクが404になる可能性があるが、URL維持不要の判断済み
- **Hugo のセクション挙動** → サブディレクトリが Hugo セクションとして扱われ、意図しないインデックスページが生成される可能性 → `_index.md` がなければデフォルトのリストテンプレートが適用されるが、記事一覧は `.RegularPagesRecursive` で正しく表示されるため実害なし
