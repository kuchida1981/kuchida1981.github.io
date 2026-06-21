## 1. 既存ドキュメントの修正

- [ ] 1.1 `openspec/specs/google-analytics/spec.md` の3つの Requirement 本文に SHALL キーワードを追加し、strict バリデーションに適合させる

## 2. pre-commit フック導入

- [ ] 2.1 `.pre-commit-config.yaml` を新規作成し、openspec-validate フック（`entry: openspec validate --strict --all --no-interactive`, `language: system`, `files: ^openspec/`, `pass_filenames: false`）を定義する
- [ ] 2.2 `pre-commit install` を実行して git hooks を有効化する

## 3. 検証

- [ ] 3.1 `openspec validate --strict --all` を実行し、全 spec がパスすることを確認する
- [ ] 3.2 openspec ファイルを含むコミットで pre-commit フックが実行されることを確認する
