## 1. 前提確認

- [ ] 1.1 `pin-daily-post-dependencies` と `daily-post-script-testability` が両方アーカイブ済みであることを確認する
- [ ] 1.2 `hugo.yaml` の build ジョブと `scripts-tests.yaml` のテストジョブが、直近の master 上で成功していることを確認する（required status check として指定するために、対象ジョブが少なくとも一度は実行済みである必要がある）

## 2. Dependabot 設定

- [ ] 2.1 `.github/dependabot.yml` を新設し、`github-actions` エコシステム（directory: `/`）を設定する
- [ ] 2.2 `.github/dependabot.yml` に `pip` エコシステム（directory: `/scripts`）を追加し、`requirements.txt` と `requirements-dev.txt` の両方が対象になることを確認する
- [ ] 2.3 更新頻度（weekly 等）と `open-pull-requests-limit` を設定する

## 3. Branch protection の整備（要ユーザー確認）

- [ ] 3.1 変更予定の branch protection 設定内容（required status checks に追加する具体的なチェック名: `build` および scripts-tests.yaml のジョブ名）をユーザーに提示し、実行の承認を得る
- [ ] 3.2 承認後、`gh api` で master の branch protection に `required_status_checks`（`hugo.yaml` の build ジョブ、`scripts-tests.yaml` のテストジョブ）を追加する
- [ ] 3.3 承認後、リポジトリ設定で `allow_auto_merge` を `true` に変更する

## 4. 自動マージワークフローの追加

- [ ] 4.1 `.github/workflows/dependabot-automerge.yaml` を新設し、`pull_request` イベント（`github.actor == 'dependabot[bot]'` 条件付き）をトリガーにする
- [ ] 4.2 `dependabot/fetch-metadata` アクションで `update-type` を取得する
- [ ] 4.3 `update-type` が `version-update:semver-patch` または `version-update:semver-minor` の場合のみ `gh pr merge --auto --squash` を実行するロジックを実装する
- [ ] 4.4 `update-type` が `version-update:semver-major` の場合は何もせず終了する（PRはオープンのまま、自動マージは有効化しない）
- [ ] 4.5 ワークフローに必要な permissions（`pull-requests: write`, `contents: write` 等）を設定する

## 5. 動作検証

- [ ] 5.1 `.github/dependabot.yml` の設定を `workflow_dispatch` 相当（Dependabot の "Check for updates" 手動トリガー、または GitHub UI）で確認し、実際に更新PRが生成されることを確認する
- [ ] 5.2 patch/minor の更新PRに対して `dependabot-automerge.yaml` が実行され、`GITHUB_TOKEN` の権限で auto-merge を有効化できることを確認する。権限不足で失敗する場合は `pull_request_target` トリガーへの切り替えを検討し、design.md の Open Questions を更新する
- [ ] 5.3 CIが green になった時点でPRが実際に自動マージされることを確認する
- [ ] 5.4 major 更新PR（またはそれに相当する状況）に対しては自動マージが有効化されないことを確認する
- [ ] 5.5 意図的にテストを失敗させた更新PRが自動マージされないことを確認する
- [ ] 5.6 既存の `automerge.yaml`（AI生成記事の24時間後automerge）が、branch protection 変更後も CI green のPRに対して正常に動作することを確認する
