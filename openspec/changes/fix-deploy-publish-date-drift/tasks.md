## 1. publish-checker.yaml（新規ワークフロー）

- [x] 1.1 `.github/workflows/publish-checker.yaml` を新規作成する。`on: schedule (*/15 * * * *)` と `on: workflow_dispatch` をトリガーにする
- [x] 1.2 `content/posts/**/*.md` の `date:` フロントマターを軽量にgrep/parseし、直近20分のルックバック窓内で現在時刻(UTC基準で比較)を過ぎたものを検出するステップを実装する（Hugoのインストールは行わない）
- [x] 1.3 該当記事が1件以上あれば `gh workflow run hugo.yaml` で `hugo.yaml` を起爆するステップを実装する。該当なしの場合は何もせず終了する
- [x] 1.4 必要な権限（`actions: write`）をワークフローの `permissions` に付与する

## 2. hugo.yaml の変更（push起点の日時補正 + schedule頻度見直し）

- [x] 2.1 push トリガー実行時のみ動作する日時補正ジョブ（またはbuildジョブ内のステップ）を追加する。既存のIndexNow用 `git diff --name-status "$before" "$after"` の差分ロジックを流用し、`A`（新規追加）ステータスかつ `content/posts/*.md` に一致するファイルを対象にする
- [x] 2.2 対象ファイルごとに `date:` フロントマターをパースし、現在時刻以下なら実行時刻（`+09:00` JST表記）に書き換える。未来日付なら何もしない
- [x] 2.3 書き換えが発生した場合、`git commit` & `git push` でmasterに補正commitを反映する。push失敗時（他のpushとの競合）は1回だけ `git pull --rebase` してリトライし、それでも失敗した場合は警告ログを出してビルドを継続する（デプロイ自体は止めない）
- [x] 2.4 補正後のワーキングツリーを使って、同一ジョブ内でHugoビルド・デプロイを実行する（別ジョブに分離して二重デプロイを起こさない）
- [x] 2.5 `workflow_dispatch` / `schedule` トリガー時はこの日時補正ロジックをスキップするよう条件分岐する（`if: github.event_name == 'push'` 等）
- [x] 2.6 既存の `schedule: cron: '0 */6 * * *'` を1日1回（例: `'0 0 * * *'`）に変更する

## 3. automerge.yaml の変更（マージ前補正 + マージ後の明示デプロイ）

- [x] 3.1 24時間経過判定でマージ対象と確定したPRについて、マージ実行前にPRブランチをcheckoutし、当該PRで新規追加された記事ファイルの `date:` をパースするステップを追加する
- [x] 3.2 `date:` が現在時刻以下ならマージ確定時刻（`+09:00` JST表記）に書き換えてPRブランチへcommit & pushする。未来日付なら何もしない
- [x] 3.3 既存のマージ処理（`gh pr merge`）はそのまま維持する
- [x] 3.4 マージ成功後、`gh workflow run hugo.yaml` を呼び出すステップを追加する

## 4. ドキュメント化

- [ ] 4.1 `docs/deploy-workflow.md` を新規作成し、以下を記載する:
  - 各ワークフロー（`daily-post.yaml` / `automerge.yaml` / `hugo.yaml` / `publish-checker.yaml`）の役割と実行順序の図
  - `GITHUB_TOKEN` によるpush/mergeが他ワークフローの `push` トリガーを起動しないというGitHub Actionsの仕様と、それが今回の設計に与える影響
  - 日時補正ルール（新規追加ファイルのみ対象、未来日付は据え置き、tz表記は `+09:00` に統一）
  - 予約投稿（未来日付）の使い方と、公開までに許容される最大遅延（15〜20分 + cron実行遅延分）
- [ ] 4.2 `CLAUDE.md` に `docs/deploy-workflow.md` へのリンクと1〜2行の概要を追加する

## 5. 動作確認（ユーザーによる手動検証手順）

- [ ] 5.1 **publish-checkerの単体動作確認**: `gh workflow run publish-checker.yaml` で手動起動し、`gh run watch` または `gh run view --log` でログを確認する。該当記事が無い状態で実行し、「該当なし・何もしない」ことを確認する
- [ ] 5.2 **未来日付の予約投稿テスト**: テスト用の記事ファイル（例: `content/posts/2026/08/2026-08-XX-test-scheduled-publish.md`、`draft: false`、`date:` を現在時刻から20〜30分後に設定）を用意し、PRを作成してmasterにマージする。マージ後、`date:` が書き換わらず未来日付のまま維持されることを確認する。指定時刻経過後、`publish-checker.yaml` の次回実行（最大15分後）で `hugo.yaml` が自動起爆されることを `gh run list --workflow=hugo.yaml` で確認し、サイトに実際に記事が公開されることをブラウザで確認する。確認後、テスト記事は削除するPRを作成する
- [ ] 5.3 **手動記事の日時補正テスト**: `date:` を現在時刻より過去（例: 2日前）に設定したテスト記事をPRで作成し、マージする。マージ後の `hugo.yaml` 実行（push起点）で、masterに補正commitが追加され、`date:` が実際のマージ・push時刻（`+09:00`表記）に書き換わっていることを確認する。デプロイされたサイト上の表示日時も確認する
- [ ] 5.4 **既存過去記事への影響がないことの確認**: 5.3実施後、`git log --follow -- <既存の任意の過去記事のパス>` で当該記事に意図しない補正commitが追加されていないことを確認する
- [ ] 5.5 **AI生成記事の自動マージ後即時デプロイの確認**: 通常の `daily-post.yaml` 実行を待つ（または `gh workflow run daily-post.yaml` で手動起動）。生成されたPRが24h後に `automerge.yaml` によってマージされた直後（次の3h毎cronの実行タイミング）、`date:` がマージ確定時刻に書き換わっていること、および `hugo.yaml` が6h cronを待たずに即座にdispatchされ実行されていることを `gh run list --workflow=hugo.yaml` で確認する
- [ ] 5.6 **ドキュメントの整合性確認**: `docs/deploy-workflow.md` の記載内容が、実際に実装したワークフローの挙動（トリガー条件・補正ルール・タイミング）と一致していることを読み合わせて確認する
