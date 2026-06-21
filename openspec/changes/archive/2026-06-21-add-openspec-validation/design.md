## Context

本プロジェクトでは openspec を使って仕様管理を行っているが、ドキュメントの品質チェックは手動実行に依存しており、実際に `spec/google-analytics` が strict バリデーションに違反した状態でコミットされている。video-ratings プロジェクトでは pre-commit hook + GitHub Actions CI の2層で検証しているが、本プロジェクトは Hugo ブログであり CI 層は不要と判断された。

現状、`.pre-commit-config.yaml` は存在しない。

## Goals / Non-Goals

**Goals:**
- openspec ドキュメント変更時に pre-commit hook でバリデーションを自動実行する
- 既存の google-analytics spec のバリデーションエラーを解消する
- `openspec validate --strict --all` が全件パスする状態を維持する

**Non-Goals:**
- GitHub Actions CI でのバリデーション（本プロジェクトでは不要）
- openspec 以外の pre-commit フック追加（Hugo テンプレートの lint 等）

## Decisions

### pre-commit hook の構成

video-ratings と同じ local hook 方式を採用する。

```yaml
repos:
  - repo: local
    hooks:
      - id: openspec-validate
        name: openspec validate (strict)
        entry: openspec validate --strict --all --no-interactive
        language: system
        files: ^openspec/
        pass_filenames: false
```

**理由:** openspec CLI はローカルにインストール済みのため `language: system` で十分。外部リポジトリのフックを使う必要がない。`files: ^openspec/` でスコープを限定し、ブログ記事のコミット時には実行されないようにする。

### google-analytics spec の修正方針

既存の Requirement 本文に「SHALL」を追加する最小限の修正とする。Requirement の意味や Scenario は変更しない。

## Risks / Trade-offs

- [Risk] `pre-commit` ツールや `openspec` CLI が未インストールの環境ではフックが動作しない → ドキュメントに前提条件を明記する（CLAUDE.md は対象外）
- [Risk] `--strict --all` は全 spec を検証するため、spec 数が増えると実行時間が伸びる → 現状 3 spec で問題なし、将来的にも Hugo ブログの spec 数は限定的
