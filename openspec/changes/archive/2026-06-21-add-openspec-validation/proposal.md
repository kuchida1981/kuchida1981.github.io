## Why

openspec ドキュメントの品質基準違反がコミット時に検出されず、`spec/google-analytics` が現在バリデーションエラー状態になっている。pre-commit hook で `openspec validate --strict --all` を自動実行し、品質基準を満たさないドキュメントのコミットを防止する。

## What Changes

- `.pre-commit-config.yaml` を新規作成し、`openspec validate` フックを定義する
- `openspec/` 配下のファイル変更時のみフックが実行される（`files: ^openspec/`）
- 既存の `google-analytics/spec.md` のバリデーションエラー（Requirement 本文に SHALL/MUST キーワードが欠落）を修正する

## Capabilities

### New Capabilities
- `openspec-doc-validation`: pre-commit hook による openspec ドキュメントの自動バリデーション

### Modified Capabilities
- `google-analytics`: 3つの Requirement 本文に SHALL/MUST キーワードを追加し、strict バリデーションに適合させる

## Impact

- 新規ファイル: `.pre-commit-config.yaml`
- 修正ファイル: `openspec/specs/google-analytics/spec.md`
- 依存: `pre-commit` ツールがローカル環境にインストールされていること、`openspec` CLI がパスに存在すること
