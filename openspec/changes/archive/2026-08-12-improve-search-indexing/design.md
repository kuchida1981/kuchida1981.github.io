## Context

Hugo + PaperMod で構築された個人ブログ（`kuchida1981.github.io`、`publishDir: docs`、GitHub Pages配信）。GitHub Actionsが `push`（master）・6時間おきのスケジュール・手動実行でビルド&デプロイを行う。日次で1本、Geminiが RSS を種にした記事を自動生成しPRを作る運用があり、記事数は193本（うち大半が自動生成）。

調査の結果、以下が判明している。

- `themes/papermod/layouts/robots.txt` は存在するが `enableRobotsTXT` が未設定のためビルド出力に含まれない
- `config.yml` の `Params.description` が `Sandbox` のままで、`<meta name="description">` とホームページのJSON-LD (`schema_json.html`) の両方に反映されている
- 193記事中、他の記事へリンクしているものは0件。`generate_daily_post.py` は過去記事を一切参照せずに単発生成している
- プロジェクトは `layouts/` にテーマオーバーライドを既に持っており（`layouts/posts/single.html` など）、テーマ本体を変更せずに機能追加できる
- Google Search Console の登録・ドメイン所有権のTXTレコード検証は運用側で対応済み（本changeのスコープ外）

## Goals / Non-Goals

**Goals:**
- 検索エンジンがサイトを継続的に発見・クロールできる状態を、設定変更と小規模なテンプレート追加で作る
- 内部リンクの欠如を、記事本文や生成プロセスを変更せずに解消する
- 変更を配信パイプライン（`hugo.yaml`）の信頼性を落とさずに組み込む

**Non-Goals:**
- Google Indexing API の導入（短命コンテンツ向けであり、本サイトの用途に合わないため見送り）
- `generate_daily_post.py` のプロンプト改変によるLLM主導のリンク挿入（非決定的で既存記事に遡及しないため見送り）
- 「薄い記事」の大量生成問題そのものの是正（編集方針の話であり、別changeで扱う）
- Search Console でのsitemap.xml登録（GSC UI上の手動作業であり、運用側のタスク）

## Decisions

### 1. `enableRobotsTXT: true` を使い、robots.txtは手書きしない
テーマの `themes/papermod/layouts/robots.txt` は `hugo.IsProduction` を見て本番以外は `Disallow: /` を返し、`Sitemap:` 行も自動で出す。これを使わずに `static/robots.txt` を手書きする案もあったが、環境判定ロジックを二重管理することになり、意図せずプレビュー環境までcrawl許可してしまうリスクがある。config一行の変更で足りるため、既存テンプレートをそのまま有効化する。

### 2. サイト説明文は「雑記ブログとしての実態を正直に反映」する方向で確定
ユーザーと協議の上、`Params.description` を以下に変更する。

```
バックエンド・インフラを中心に活動するフリーランスエンジニアの個人ブログ。技術的な試行錯誤の記録から日々のニュース、ときにフィクションまで。
```

技術キーワード（Go/Python/AWS/GCP）を前面に出す案も検討したが、サイトには日次ニュースやフィクション連載も混在しており、検索結果のスニペットと実際のコンテンツが乖離するとクリック後の離脱要因になりうる。実態に即した記述を優先する。

### 3. 内部リンクは Hugo の Related Content 機能で解決し、記事本文は書き換えない
`site.RegularPages.Related` はfront matterの `tags` / `categories` の重複度からビルド時に関連記事を計算する。これを `layouts/posts/single.html` の記事フッター（タグ一覧の直後、`post_nav_links` の前）に追加する。

比較した代替案:
- **Geminiプロンプト改変**（過去記事一覧をコンテキストに渡し本文中にリンクさせる）: 今後の記事にしか効かず、LLM依存でリンク先の妥当性が保証されない
- **`patch_past_posts.py` 的な一括バックフィルスクリプト**: 193記事全てを機械的に書き換えることになり、差分レビューの負荷とリグレッションリスクが大きい

Related Content案は記事ファイルを一切変更せず、既存193記事・今後の記事の両方に自動的に適用される点で明確に優位。

**重み付け**: `config.yml` に `related` ブロックを追加し、`tags` の重みを `categories` より高くする。カテゴリは `Tech` / `Service` / `Fiction` 程度の粗い分類で、カテゴリだけを重視すると無関係な記事同士まで「関連」になってしまうため。

**表示件数**: 上位5件。関連記事が1件も見つからない場合はセクション自体を非表示にする（空のボックスを出さない）。

**著者フィルタなし**: 自動生成記事（`author: "Ghost Writer"`）と人間が書いた記事を区別せず、トピックの近さのみで関連付ける。著者で足切りすると内部リンクの母数が大きく減り、目的（発見経路を増やす）に反するため。

### 4. IndexNowは push イベント時の記事差分のみを対象に通知する
`hugo.yaml` の `deploy` ジョブ完了後（または `build` ジョブ内のデプロイ直前）に、IndexNow通知ステップを追加する。

- キーはランダムな16進文字列を1つ生成し、`static/<key>.txt`（中身はキー文字列そのもの）としてリポジトリにコミットする。IndexNowの仕様上キー自体は秘匿情報ではなく、サイト上で公開する前提の値なのでGitHub Secretsは不要
- 通知対象URLは、`push` イベントの `github.event.before`/`github.event.after` 間で `content/posts/**/*.md` の変更ファイルを diff し、Hugoのパーマリンク規則（`content/posts/YYYY/MM/slug.md` → `/posts/YYYY/MM/slug/`）でURLへ変換したものに限定する
- `schedule`（6時間おき）や `workflow_dispatch`、`pull_request` トリガーでは通知をスキップする。記事変更を伴わない再ビルドで既知URLを繰り返し送るのは無駄であり、IndexNow側からの評価を下げる可能性もあるため
- 通知ステップは `continue-on-error: true` とし、IndexNow側の障害がGitHub Pagesへのデプロイ自体をブロックしないようにする

全記事URL（sitemap.xml全体）を毎回送る案も検討したが、変更のないURLを送り続けることになり不要なリクエストが積み重なるため、差分ベースを採用する。

## Risks / Trade-offs

- [Risk] Related Content が、タグの薄い記事（連載フィクションなど）に無関係な記事を関連付けてしまう → [Mitigation] tags重視の重み付けと、関連0件時は非表示にするフォールバックで、明らかに無関係なものが目立つ状況を避ける
- [Risk] `git diff` ベースのURL抽出が、リネームやディレクトリ移動を伴う変更で正しく検出できない可能性 → [Mitigation] 実装時に `git diff --name-status` で追加(A)・変更(M)のみを対象にし、削除(D)されたファイルは通知対象から除外する
- [Risk] IndexNow通知ステップの追加により `hugo.yaml` の実行時間・複雑性が増す → [Mitigation] `continue-on-error: true` かつ独立したステップとして追加し、既存のビルド/デプロイフローには影響しない構成にする
- [Risk] サイト説明文の変更により、既存の検索結果スニペットやSNSシェア時の見え方が一時的に変わる → [Mitigation] 影響は軽微で、config一行のロールバックで即座に戻せる

## Migration Plan

1. `config.yml` の変更（`enableRobotsTXT`、`Params.description`、`related` ブロック）— 低リスク、即座に反映
2. `layouts/posts/single.html` への関連記事セクション追加 — ローカルで `hugo` ビルドし、実際に関連記事が表示されることを目視確認
3. IndexNowキー生成・`static/<key>.txt` 追加・`hugo.yaml` へのステップ追加 — 追加後、次回の記事公開pushで実際に通知が送信されることを確認

ロールバックは各ステップとも該当ファイルの変更を打ち消すだけで完結する（データ移行やスキーマ変更を伴わない）。

## Open Questions

- 関連記事の表示件数（5件）は運用しながら調整が必要か
- IndexNowの通知対象を `content/posts/` の変更に限定しているが、`content/about.md` や `content/services.md` の更新も対象に含めるべきか
