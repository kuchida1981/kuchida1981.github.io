## Why

`scripts/requirements.txt`（`google-genai` / `feedparser` / `python-dotenv`）はバージョン指定なしで管理されており、`daily-post.yaml` が実行されるたびに「その時点の最新版」がインストールされる。これにより、upstream が破壊的変更を出した瞬間に何の予兆もなく daily-post パイプラインが壊れるリスクを常に抱えている。また、バージョン範囲が存在しないため、将来 Dependabot の pip エコシステムを導入しても更新対象として認識されず、更新PRが出てこない。依存関係を明示的にピン留めすることで、再現可能なビルドを実現し、以降のテスト整備・Dependabot 導入（別 change で対応予定）の土台を作る。

## What Changes

- `scripts/requirements.txt` の `google-genai` / `feedparser` / `python-dotenv` を、現在動作している具体的なバージョンに `==` で固定する
- スクリプトのロジック自体（`scripts/generate_daily_post.py` の挙動）は変更しない
- `daily-post.yaml` ワークフローの `pip install -r scripts/requirements.txt` の呼び出し方自体は変更しない（インストールされるバージョンが固定される点のみが変わる）

## Capabilities

### New Capabilities
- `daily-post-dependency-pinning`: daily-post 生成パイプラインが使用する Python 依存関係のバージョンを固定し、再現可能なインストールを保証する

### Modified Capabilities
(なし)

## Impact

- 影響ファイル: `scripts/requirements.txt`
- 影響ワークフロー: `.github/workflows/daily-post.yaml`（インストールされる依存バージョンが固定されるのみで、ステップ自体は無変更）
- 後続: この change の完了が、(1) `generate_daily_post.py` のテスト整備、(2) Dependabot 導入、の前提条件となる
