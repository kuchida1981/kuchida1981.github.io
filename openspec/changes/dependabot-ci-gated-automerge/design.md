## Context

現状確認済みのリポジトリ設定（2026-08-08 時点、`gh api` で確認）:

```
repos/.../kuchida1981.github.io:
  allow_auto_merge: false
  allow_merge_commit: true
  allow_squash_merge: true

branches/master/protection:
  required_pull_request_reviews.required_approving_review_count: 0
  required_status_checks: (未設定・キー自体が存在しない)
  enforce_admins: true
```

つまり現状は「CIが red でも master へのマージボタンが押せてしまう」状態であり、Dependabot を導入するだけでは「greenならマージ」という要件は満たせない。branch protection の整備が前提として必要。

既存の automerge.yaml は `automerge-24h` ラベル + 24時間経過 + `mergeable != CONFLICTING` のみを見て `gh pr merge` を叩いており、CI のステータスそのものは見ていない（`gh pr merge` は branch protection で required checks が設定されていれば内部的に失敗するが、現状は未設定なので抑止力になっていない）。

`daily-post-script-testability` の完了により `scripts-tests.yaml` が追加され、`hugo.yaml` の build ジョブと合わせて2つの CI ジョブが常時実行される状態になっている前提。

## Goals / Non-Goals

**Goals:**
- Dependabot による依存更新PRの自動生成（github-actions, pip）
- 必須ステータスチェック（hugo build, scripts test）が green の場合のみマージ可能にする branch protection の整備
- patch/minor の更新は人手を介さず自動マージ、major は人間レビューを必須のままにする

**Non-Goals:**
- `Dockerfile` の base image 更新の自動化（検証するCIが存在しないため）
- `themes/papermod`（git submodule）の更新自動化（Dependabot非対応。Renovate等の別ツール導入は別議論）
- 既存の `automerge.yaml`（AI生成記事の24時間後automerge）のロジック変更
- レビュー必須化（`required_approving_review_count` の引き上げ）。今回は required status checks の追加のみを行う

## Decisions

- **自動マージの実装は GitHub 純正の Auto-merge 機能を使う（ラベル+時間経過方式は使わない）**
  理由: 要件は「CIがgreenになった瞬間にマージしたい」であり、時間経過ベースの `automerge.yaml` パターンとは目的が異なる。GitHub純正のAuto-mergeなら、`allow_auto_merge` を有効化した上で対象PRに対して一度 `gh pr merge --auto` を叩くだけで、あとはGitHub側が required status checks の完了を監視して自動でマージしてくれる。

- **patch/minor は自動マージ、major は人間レビュー必須（自動マージを有効化しない）**
  理由: GitHub Actions の pin や pip パッケージの major bump は破壊的変更を含む可能性がある。CI（Hugoビルド・pytest）は現状の挙動を検証できるが、Gemini SDK のような外部APIクライアントの major bump は、モックテストでは検知できない仕様変更を含みうる。`dependabot/fetch-metadata` アクションで `update-type` を判定し、`version-update:semver-major` の場合は自動マージワークフローを早期終了させる。

- **branch protection の required status checks には `hugo.yaml` の `build` ジョブと `scripts-tests.yaml` のテストジョブのみを指定し、`deploy` ジョブは含めない**
  理由: `deploy` ジョブは push/schedule/workflow_dispatch 時のみ実行され、PRイベントでは実行されない（`hugo.yaml` の `if` 条件を参照）。PRに対して報告されないジョブを required にすると、そのチェックが永遠に「保留」となりマージが恒久的にブロックされる（GitHub Actionsの既知の落とし穴）。

- **`allow_auto_merge` の有効化と branch protection の変更は、Claude Code が `gh api` で実行前にユーザーに確認を取ってから行う**
  理由: branch protection の変更はリポジトリ全体のマージ挙動に影響する共有設定であり、CLAUDE.md 上も「ワークフロー変更」や「破壊的変更に関わる判断」に類する。tasks.md 上で明示的な確認ステップとして独立させる。

- **Dockerfile（docker エコシステム）は対象外とする**
  理由: `Dockerfile` はローカル開発用の `docker compose up` にのみ使われ、`hugo.yaml`（本番ビルド）はこれを経由しない。docker エコシステムの更新PRを出しても検証するCIが存在せず、「greenならマージ」の前提が成立しない。将来 Dockerfile のビルド検証をCIに追加すれば再検討する。

## Risks / Trade-offs

- [Dependabot が起点となるワークフロー実行は、GitHubのセキュリティ上の制約で `GITHUB_TOKEN` の権限や secrets へのアクセスが通常より制限される場合がある] → 実装時に `dependabot-automerge.yaml` が実際に PR に対して auto-merge を有効化できるか動作検証する。権限不足で失敗する場合は `pull_request_target` トリガーへの切り替え、または Dependabot 専用の PAT の利用を検討する（Open Questions 参照）
- [branch protection に required status checks を追加すると、既存の `automerge.yaml`（24時間後automerge）も CI green が前提になる] → これは意図した副次効果（安全性向上）だが、現在 CI が red のまま24時間放置されているPRがあれば、この変更後は automerge されなくなる点を運用者は認識しておく必要がある
- [pip の major bump を自動マージから除外しても、minor/patch の更新が Gemini SDK の挙動を微妙に変える可能性はモックテストでは検知できない] → 許容する非ゴール。実運用（実際のdaily-post生成結果）でのモニタリングに委ねる
- [`allow_auto_merge` の有効化・branch protection の変更はGitHub上のリポジトリ設定であり、コードレビューの対象にならない] → tasks.md で実行前にユーザー確認を取るステップを明示する

## Migration Plan

1. `pin-daily-post-dependencies` と `daily-post-script-testability` が完了していることを確認する
2. `.github/dependabot.yml` を追加する（github-actions, pip）
3. branch protection の変更内容（required status checksに追加する具体的なチェック名）をユーザーに確認する
4. ユーザー確認後、`allow_auto_merge` の有効化と branch protection の更新を `gh api` で実行する
5. `dependabot-automerge.yaml` を追加する
6. Dependabot が実際にPRを作成するのを待つか、`gh api` で手動トリガーして動作を確認する（patch/minor が自動マージされること、major が自動マージされずレビュー待ちのままであることの両方を確認する）
7. ロールバック方針: `dependabot.yml` の削除でPR生成自体を止められる。branch protection は `gh api` で `required_status_checks: null` に戻せば即座に元の状態に戻せる

## Open Questions

- Dependabot起点のワークフロー実行における `GITHUB_TOKEN` の実際の権限（auto-merge を有効化する `gh pr merge --auto` の実行に十分な権限があるか）は、実装・動作検証時に確定させる
