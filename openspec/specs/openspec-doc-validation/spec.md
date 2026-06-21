# openspec-doc-validation Specification

## Purpose
pre-commit hook で `openspec validate --strict --all` を自動実行し、openspec ドキュメントの品質基準違反をコミット時に検出してブロックする。

## Requirements

### Requirement: pre-commit での openspec バリデーション
`openspec/` 配下のファイルが変更されたコミット時に、システムは `openspec validate --strict --all` を自動実行し、バリデーションエラーがある場合はコミットをブロックしなければならない（MUST）。

#### Scenario: openspec ファイル変更時にバリデーションが実行される
- **WHEN** `openspec/` 配下のファイルを変更してコミットしようとする
- **THEN** pre-commit が `openspec validate --strict --all --no-interactive` を実行する

#### Scenario: バリデーションエラーがある場合コミットがブロックされる
- **WHEN** `openspec validate --strict --all` がエラーを検出する
- **THEN** コミットが中止され、エラー内容が表示される

#### Scenario: openspec 以外の変更ではバリデーションがスキップされる
- **WHEN** `openspec/` 配下のファイルを変更せずにコミットする
- **THEN** openspec validate フックはスキップされる
