## Why

記事の `date:` フロントマターと実際のサイト公開時刻が常時24〜33時間ズレている。原因は2つ確認済み: (1) `automerge.yaml` が `GITHUB_TOKEN` でPRをマージするため、GitHub Actionsの仕様上 `hugo.yaml` の `push` トリガーが発火せず、デプロイが6時間毎cronだけに依存している、(2) AI生成記事の `date:` は生成（PR作成）時刻のままで、24hの自動マージ猶予後に公開されても書き換わらない。加えて、未来日付を指定した「予約投稿」は現状Hugoの仕様上ビルドから除外されるだけで、指定時刻に近いタイミングで公開する仕組みが存在しない。

## What Changes

- `automerge.yaml`: PRマージ判断前に、対象記事の `date:` が現在時刻以下ならマージ確定時刻（`+09:00` JST表記）に書き換えてPRブランチにcommit。未来日付は変更せず予約投稿として尊重する。マージ後に `gh workflow run hugo.yaml` を明示dispatchし、6h cron待ちを解消する
- `hugo.yaml`: `push` トリガー時のみ、当該pushで新規追加された `content/posts/*.md` を対象に同様の日時補正（現在時刻以下なら書き換えてmasterへcommit、未来日付は据え置き）を行う。`workflow_dispatch`/`schedule` 起点では補正ロジックを実行しない（二重補正・無限書き換え防止）。既存の6時間毎 `schedule` は取りこぼし保険として頻度を見直す
- 新規ワークフロー `publish-checker.yaml`: 15分毎に `content/posts/**` の `date:` を軽量スキャンし、直近のルックバック窓内で現在時刻を過ぎた未来日付記事があれば `gh workflow run hugo.yaml` を起爆する（stateless、Hugoインストール不要）
- デプロイフロー全体（各ワークフローの役割分担、日時補正ルール、`GITHUB_TOKEN` のpushトリガー制限という根本原因）をドキュメント化する
- ユーザーが実装後に手動で動作確認する具体的な手順を `tasks.md` に明記する

## Capabilities

### New Capabilities
- `publish-timing`: 記事の公開日時（`date:` フロントマター）と実際のデプロイ・公開タイミングを一致させるための、マージ時日時補正・即時デプロイdispatch・未来日付予約投稿のポーリング公開の仕組み

### Modified Capabilities
(なし。`blog` の「Automated Daily Content」要件はAI記事の生成・PR作成フローを規定しており、日時補正はマージ・デプロイ側の新規capabilityとして分離する)

## Impact

- `.github/workflows/automerge.yaml`: マージ前の日時補正ステップ、マージ後の明示dispatchステップを追加
- `.github/workflows/hugo.yaml`: push起点のみの日時補正ジョブを追加、schedule頻度を見直し
- `.github/workflows/publish-checker.yaml`: 新規ファイル
- ドキュメント: デプロイフローの説明を追加（配置場所は design.md で決定）
- 既存の `content/posts/**` の過去記事には影響なし（補正対象は「新規追加ファイル」に限定するガードにより担保）
