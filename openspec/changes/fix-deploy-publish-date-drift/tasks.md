## 1. publish-checker.yaml（新規ワークフロー）

- [x] 1.1 `.github/workflows/publish-checker.yaml` を新規作成する。`on: schedule (*/15 * * * *)` と `on: workflow_dispatch` をトリガーにする
- [x] 1.2 `content/posts/**/*.md` の `date:` フロントマターを軽量にgrep/parseし、直近20分のルックバック窓内で現在時刻(UTC基準で比較)を過ぎたものを検出するステップを実装する（Hugoのインストールは行わない）
- [x] 1.3 該当記事が1件以上あれば `gh workflow run hugo.yaml` で `hugo.yaml` を起爆するステップを実装する。該当なしの場合は何もせず終了する
- [x] 1.4 必要な権限（`actions: write`）をワークフローの `permissions` に付与する

## 2. automerge.yaml の変更（マージ前補正 + マージ後の明示デプロイ）

- [x] 2.1 24時間経過判定でマージ対象と確定したPRについて、マージ実行前にPRブランチをcheckoutし、当該PRで新規追加された記事ファイルの `date:` をパースするステップを追加する
- [x] 2.2 `date:` が現在時刻以下ならマージ確定時刻（`+09:00` JST表記）に書き換えてPRブランチへcommit & pushする。未来日付なら何もしない
- [x] 2.3 既存のマージ処理（`gh pr merge`）はそのまま維持する
- [x] 2.4 マージ成功後、`gh workflow run hugo.yaml` を呼び出すステップを追加する
- [x] 2.5 日時補正・PRブランチへの補正commit pushは `master` ではなくPR自身のブランチに対して行う（branch protectionの影響を受けないことを確認済み）
- [x] 2.6 `gh api .../pulls/$number/files` は `--paginate` を付与し、30ファイル超のPRでも取りこぼさないようにする
- [x] 2.7 補正commitのpushが失敗した場合、`git pull --rebase` で1回リトライし、それでも失敗したら警告ログを出すだけでスクリプト・ループ全体を継続させる（`set -e` で異常終了させない）

## 3. 手動記事向け日時補正ワークフロー（新規）

`master` のbranch protection（`required_pull_request_reviews` 有効・`enforce_admins: true`・bypassアクター無し）により、`GITHUB_TOKEN` からの `master` への直接pushは常に拒否される。そのため、手動記事の日時補正も automerge.yaml と同様に「PRブランチへのマージ前commit」方式で行う。

- [x] 3.1 `.github/workflows/correct-manual-post-dates.yaml`（名称は実装時に適宜調整可）を新規作成する。トリガーは `pull_request: types: [opened, synchronize]`（対象ブランチ: `master` 宛のPR）
- [x] 3.2 `automerge-24h` ラベルが付与されているPRは対象外とする（AI生成記事は automerge.yaml が既に処理するため、重複補正を避ける）
- [x] 3.3 `gh api repos/OWNER/REPO/pulls/$PR_NUMBER/files --paginate` で、当該PRにより新規追加（`status=="added"`）された `content/posts/*.md`（`_index.md`除く）を特定する
- [x] 3.4 該当ファイルがあれば、PRのheadブランチ（`github.head_ref`、同一リポジトリ内のブランチであることが前提。forkからのPRは対象外でよい）をcheckoutし、`scripts/correct_publish_dates.py` を実行する（automerge.yamlと共通のスクリプトを再利用する）
- [x] 3.5 変更があれば、そのPRブランチへcommit & pushする（`master`へは一切pushしない）。push失敗時は1回だけ `git pull --rebase` してリトライし、それでも失敗したら警告ログを出すだけで正常終了する
- [x] 3.6 必要な権限（`contents: write`, `pull-requests: read`）を `permissions` に付与する

## 4. hugo.yaml の変更（schedule頻度の見直しのみ、日時補正ロジックは持たせない）

- [x] 4.1 既存の `schedule: cron: '0 */6 * * *'` を1日1回（例: `'0 0 * * *'`）に変更する
- [x] 4.2 push起点で追加していた日時補正ステップ（`Correct stale publish dates for new posts` / `Commit and push corrected dates`）を削除する。`master` への直接pushはbranch protectionにより常に失敗するため、`hugo.yaml` はビルド・デプロイに専念させる

## 5. ドキュメント化

- [x] 5.1 `.github/workflows/README.md` を新規作成し、以下を記載する:
  - 各ワークフロー（`daily-post.yaml` / `automerge.yaml` / `correct-manual-post-dates.yaml` / `hugo.yaml` / `publish-checker.yaml`）の役割と実行順序の図
  - `GITHUB_TOKEN` によるpush/mergeが他ワークフローの `push` トリガーを起動しないというGitHub Actionsの仕様と、それが今回の設計に与える影響
  - `master` のbranch protectionにより直接pushができないため、日時補正は常にPRブランチへのマージ前commitで行うという設計上の制約
  - 日時補正ルール（新規追加ファイルのみ対象、未来日付は据え置き、tz表記は `+09:00` に統一）
  - 予約投稿（未来日付）の使い方と、公開までに許容される最大遅延（15〜20分 + cron実行遅延分）
- [x] 5.2 `CLAUDE.md` に `.github/workflows/README.md` へのリンクと1〜2行の概要を追加する
- [x] 5.3 上記のbranch protection制約とworkflow構成の変更（`correct-manual-post-dates.yaml`追加、`hugo.yaml`の日時補正削除）を反映するようドキュメントを更新する

## 6. 動作確認（ユーザーによる手動検証手順）

- [ ] 6.1 **publish-checkerの単体動作確認**: `gh workflow run publish-checker.yaml` で手動起動し、`gh run watch` または `gh run view --log` でログを確認する。該当記事が無い状態で実行し、「該当なし・何もしない」ことを確認する
- [ ] 6.2 **未来日付の予約投稿テスト**: テスト用の記事ファイル（例: `content/posts/2026/08/2026-08-XX-test-scheduled-publish.md`、`draft: false`、`date:` を現在時刻から20〜30分後に設定）を用意し、PRを作成する。PR作成時点で日時補正ワークフローが未来日付を書き換えないことを確認し、マージする。指定時刻経過後、`publish-checker.yaml` の次回実行（最大15分後）で `hugo.yaml` が自動起爆されることを `gh run list --workflow=hugo.yaml` で確認し、サイトに実際に記事が公開されることをブラウザで確認する。確認後、テスト記事は削除するPRを作成する
- [ ] 6.3 **手動記事の日時補正テスト**: `date:` を現在時刻より過去（例: 2日前）に設定したテスト記事でPRを作成する。`correct-manual-post-dates.yaml` が実行され、PRブランチへ補正commitがpushされ、`date:` がPR作成・更新時刻（`+09:00`表記）に書き換わっていることを確認する。その後PRをマージし、サイト上の表示日時も確認する
- [ ] 6.4 **既存過去記事への影響がないことの確認**: 6.3実施後、`git log --follow -- <既存の任意の過去記事のパス>` で当該記事に意図しない補正commitが追加されていないことを確認する
- [ ] 6.5 **AI生成記事の自動マージ後即時デプロイの確認**: 通常の `daily-post.yaml` 実行を待つ（または `gh workflow run daily-post.yaml` で手動起動）。生成されたPRが24h後に `automerge.yaml` によってマージされた直後、`date:` がマージ確定時刻に書き換わっていること、および `hugo.yaml` が6h cronを待たずに即座にdispatchされ実行されていることを `gh run list --workflow=hugo.yaml` で確認する
- [ ] 6.6 **automerge-24hラベル付きPRが `correct-manual-post-dates.yaml` の対象外であることの確認**: `daily-post.yaml` が作成したPR（`automerge-24h` ラベル付き）のActions実行履歴で、`correct-manual-post-dates.yaml` がスキップまたは未実行であることを確認する
- [ ] 6.7 **ドキュメントの整合性確認**: `.github/workflows/README.md` の記載内容が、実際に実装したワークフローの挙動（トリガー条件・補正ルール・タイミング・branch protectionの制約）と一致していることを読み合わせて確認する
