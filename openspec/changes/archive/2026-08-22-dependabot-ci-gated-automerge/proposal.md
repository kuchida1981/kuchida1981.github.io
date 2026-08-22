## Why

現在このリポジトリには依存関係の更新を検知・提案する仕組みが存在せず、GitHub Actions・pip 依存の更新はすべて手動で気づいて対応する必要がある。`pin-daily-post-dependencies` で pip 依存をピン留めし、`daily-post-script-testability` で CI 上のテスト安全網（`scripts-tests.yaml`）を整備したことで、ようやく「更新PRが出たら、テストが通った場合にのみ安全にマージする」という体制を組める土台が揃った。Dependabot を導入し、CI が green の場合に自動マージされる体制を作ることで、依存更新の追従コストをゼロに近づける。

## What Changes

- `.github/dependabot.yml` を新設し、以下のエコシステムを対象に更新PRを自動生成する:
  - `github-actions`: `.github/workflows/*.yaml` 内の action pin（例: `actions/checkout@v3`）
  - `pip`: `scripts/requirements.txt` / `scripts/requirements-dev.txt`（`pin-daily-post-dependencies` と `daily-post-script-testability` の完了が前提）
  - `git submodule`（`themes/papermod`）は Dependabot が対応していないため**対象外**
  - `Dockerfile`（`docker` エコシステム）はこの change では**対象外**とする。理由は Impact 節を参照
- master ブランチの branch protection に `required_status_checks` を追加し、`hugo.yaml` の build ジョブと `scripts-tests.yaml` の test ジョブを必須チェックにする
- リポジトリ設定 `allow_auto_merge` を有効化する（GitHub リポジトリ設定の変更）
- Dependabot が作成した PR に対して GitHub 純正の Auto-merge を有効化するワークフロー（`.github/workflows/dependabot-automerge.yaml`）を新設する
  - `dependabot/fetch-metadata` アクションで更新種別（patch / minor / major）を判定する
  - patch・minor の更新は自動マージを有効化する
  - major の更新は自動マージを有効化せず、人間のレビューを必須のままにする（**BREAKING** の可能性がある変更を無条件マージしないための安全策）

## Capabilities

### New Capabilities
- `dependabot-automerge`: Dependabot が生成した依存更新PRを対象に、CI（必須ステータスチェック）が green の場合にのみ自動的にマージする仕組みを定義する

### Modified Capabilities
(なし。既存の automerge.yaml（AI生成記事向けの24時間後automerge）の挙動自体は変更しないが、branch protection に required status checks を追加することで、副次的に「CIがgreenでなければマージできない」制約が automerge.yaml にも及ぶことになる。これは automerge.yaml のリクワイアメントを変更するものではなく、リポジトリ全体のマージ条件の変更であるため、既存specの変更としては扱わない)

## Impact

- 影響ファイル: `.github/dependabot.yml`（新規）、`.github/workflows/dependabot-automerge.yaml`（新規）
- 影響設定: GitHub リポジトリ設定（`allow_auto_merge`）、master の branch protection（`required_status_checks`）
- 副次的な影響: 既存の `automerge.yaml`（ラベルベース・24時間後マージ）も、branch protection に required status checks が追加されることで、CIがgreenでない限りマージできなくなる（意図した副次効果であり、安全性の向上）
- スコープ外: `Dockerfile` の base image 更新（`docker` エコシステム）は、それを検証する CI が存在しないため対象外とする。将来 Docker イメージのビルド検証を CI に追加した際に別 change で対応する
- 前提: `pin-daily-post-dependencies` と `daily-post-script-testability` の両方が完了していること
