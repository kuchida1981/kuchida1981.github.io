# Capability: daily-post-dependency-pinning

## Purpose

daily-post 生成パイプラインが使用する Python 依存関係のバージョンを固定し、再現可能なインストールを保証する。

## Requirements

### Requirement: トップレベル依存のバージョン固定
`scripts/requirements.txt` に列挙されるトップレベルの Python 依存パッケージ（`google-genai`, `feedparser`, `python-dotenv`）は、すべて `==` による厳密なバージョン指定を伴わなければならない（MUST）。バージョン範囲指定なしのエントリを含んではならない。

#### Scenario: すべての依存に厳密なバージョン指定がある
- **WHEN** `scripts/requirements.txt` の内容を確認する
- **THEN** 各行が `<package>==<version>` の形式になっている
- **AND** バージョン指定のない行（パッケージ名のみの行）が存在しない

#### Scenario: daily-post ワークフローが固定バージョンをインストールする
- **WHEN** `.github/workflows/daily-post.yaml` が `pip install -r scripts/requirements.txt` を実行する
- **THEN** `scripts/requirements.txt` に記載された通りの厳密なバージョンがインストールされる
- **AND** 実行のたびにインストールされるトップレベルパッケージのバージョンが変化しない
