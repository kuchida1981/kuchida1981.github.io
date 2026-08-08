## Why

`scripts/generate_daily_post.py` は「書き捨て」に近い想定で書かれたが、半年以上 daily-post パイプラインの中核として稼働し続けている。自動テストが一切なく、モジュールのトップレベルで `GEMINI_API_KEY` の存在チェックと `exit(1)`、Gemini クライアントの生成という副作用が実行されるため、`import` するだけでテストが書けない構造になっている。Dependabot（別 change で導入予定）が依存パッケージの更新PRを出しても、それが安全かどうかを CI 上で検証する手段が今は存在しない。Gemini API を実際に呼ばない範囲でロジックの正しさを保証できるようにし、依存更新の安全網を用意する。

## What Changes

- `scripts/generate_daily_post.py` を以下の方針で軽量にリファクタリングする（単一ファイルのまま、パッケージ分割はしない）:
  - モジュールのトップレベルにある `GEMINI_API_KEY` チェックと `genai.Client` の生成を `main()` 内に移動し、import 時の副作用を排除する
  - `generate_blog_post()` を `generate_slug()` と同様に `client` を引数として受け取る形に統一する（現状はグローバル変数の `client` を直接参照している）
  - 上記以外のロジック（プロンプト内容、RSS取得、スラッグ生成、フロントマター処理、ファイル保存）は変更しない
- `scripts/` 配下に pytest ベースのテストスイートを新設し、Gemini API・RSS フィードへの実際のネットワークアクセスなしに以下を検証する:
  - `sanitize_slug()` / `extract_title()`（純粋関数の境界値）
  - `save_post()`（ファイル保存・フロントマターへの author 補完、`tmp_path` で検証）
  - `fetch_rss_items()`（`feedparser.parse` をモックして解析ロジックを検証）
  - `generate_blog_post()` / `generate_slug()`（Gemini クライアントをフェイクに差し替えてプロンプト構築・レスポンス処理・フォールバック挙動を検証）
- CI に `scripts/` 配下のテストを実行するジョブを追加する（既存の `hugo.yaml` への追加、または新規ワークフローファイルのどちらにするかは design.md で決定）
- `scripts/patch_past_posts.py` は対象外（今回のリファクタ・テスト整備には含めない）

## Capabilities

### New Capabilities
- `daily-post-script-testability`: `generate_daily_post.py` が import 時に副作用を起こさず、外部API・ネットワークに依存しない自動テストで主要ロジックの正しさを検証できる状態であることを定義する

### Modified Capabilities
(なし。`filename-slug-generation` のスラッグ生成ロジック自体の挙動は変更しない)

## Impact

- 影響ファイル: `scripts/generate_daily_post.py`（リファクタ）、`scripts/test_generate_daily_post.py` 等の新規テストファイル、CI ワークフロー（テストジョブの追加）
- 依存関係: テスト実行のため `pytest`（および必要であれば `pytest-mock` 等のモック用ライブラリ）を開発時依存として追加する。`scripts/requirements.txt` への追加方法（本番用と分けるか等）は design.md で決定する
- 前提: 本 change は `pin-daily-post-dependencies`（依存バージョン固定）の完了を前提とする
- 後続: 本 change の完了が Dependabot 導入（pip エコシステムを含む CI 安全網）の前提条件となる
