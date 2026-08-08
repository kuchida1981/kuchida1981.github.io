## Context

`scripts/generate_daily_post.py`（201行）は以下の4つの責務を単一ファイル内に持つ:

1. RSS取得 (`fetch_rss_items`)
2. Gemini呼び出し (`generate_blog_post`, `generate_slug`)
3. テキスト加工（`sanitize_slug`, `extract_title` はすでに純粋関数）
4. ファイル保存 (`save_post`)

モジュールのトップレベルで以下が実行されており、これが `import` を伴う自動テストを妨げている:

```python
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit(1)

client = genai.Client(api_key=API_KEY)
```

また `generate_blog_post(feed_items)` はこのグローバル `client` を直接参照しており、`generate_slug(client, title)` が `client` を引数で受け取っているのと非対称になっている。

CI（`.github/workflows/hugo.yaml`）は Hugo のビルドのみを検証しており、Python コードは一切実行されない。プロジェクトには pytest 等のテスト基盤が存在しない（`pyproject.toml` / `pytest.ini` / `conftest.py` なし）。

前提: `pin-daily-post-dependencies` change が完了し、`scripts/requirements.txt` の本番依存が `==` で固定済みであること。

## Goals / Non-Goals

**Goals:**
- `generate_daily_post.py` の `import` 時に副作用（`exit(1)` や Gemini クライアント生成）が発生しない構造にする
- `client` をすべての Gemini 呼び出し関数で一貫して引数として受け取れるようにする
- Gemini API・RSS フィードへの実ネットワークアクセスなしに主要ロジックを検証する pytest スイートを追加する
- CI 上でこのテストスイートが実行され、失敗時に PR がブロックされる状態にする

**Non-Goals:**
- 単一ファイルからの分割（パッケージ化）は行わない
- `main()` 全体を実際に Gemini API を叩いて検証する統合テストは作らない
- `scripts/patch_past_posts.py` へのテスト追加やリファクタ
- lock ファイル化やパッケージ管理ツール（Poetry 等）の導入

## Decisions

- **リファクタは最小限（client 注入 + トップレベル副作用の除去）に留め、単一ファイルのまま進める**
  理由: スクリプトの規模（201行、4責務）に対してパッケージ分割は過剰。既存ロジック（プロンプト内容、フロントマター処理）は半年の実運用で検証済みであり、挙動を変えるリスクを避けたい。
  代替案として検討した「パッケージ分割 + 依存性注入の徹底」は、今回のスコープ（テスト可能にする）に対してオーバーエンジニアリングと判断し却下。

- **モックには標準ライブラリの `unittest.mock` / pytest 標準の `monkeypatch` フィクスチャのみを使い、`pytest-mock` 等の追加プラグインは導入しない**
  理由: このスクリプトの規模でモックすべき対象は少数（`feedparser.parse`、Gemini クライアントの `models.generate_content`）であり、標準機能で十分に書ける。新規依存を最小限にする。

- **テスト用依存（`pytest`）は本番用 `scripts/requirements.txt` とは別に `scripts/requirements-dev.txt` を新設して管理する**
  理由: `scripts/requirements.txt` は `daily-post.yaml` の本番実行でもインストールされる。`pytest` を本番依存に混ぜると、本番実行のインストール時間が伸びる上に、依存関係の性質（本番実行に必須 vs テスト実行にのみ必要）が曖昧になる。分離することで `pin-daily-post-dependencies` で固定した本番依存の一覧をテスト都合で汚さない。

- **CI ジョブは新規ワークフローファイル `.github/workflows/scripts-tests.yaml` として独立させ、`push`(master) / `pull_request` の両方で常に実行する（`paths` によるフィルタは使わない）**
  理由: `hugo.yaml` は Hugo ビルド専用で 6時間おきのスケジュール実行も含み、責務が異なる。分離することで、後続の Dependabot 導入時にこのジョブを "required status check" として指定しやすくなる。
  `paths: ['scripts/**']` のようなフィルタは意図的に使わない。理由: GitHub の required status check は、ワークフローがトリガーされず該当ジョブが一度も報告されない PR に対しては永遠に「保留」のままとなり、マージがブロックされ続けるという既知の問題がある。テストスイート自体が小規模で実行コストが低いため、フィルタで最適化するメリットよりこの落とし穴を避けるメリットを優先する。

- **固定するバージョンの選定方針は `pin-daily-post-dependencies` と同様、テスト用途のため最新の安定版を採用する**
  `pytest` は本番のGemini/RSS連携とは独立したツールであり、直近の成功実行のような参照点がないため、導入時点の最新版を `==` で固定する。

## Risks / Trade-offs

- [リファクタで `client` の受け渡し方を変えることで、`main()` の呼び出し順序を書き換える必要があり、わずかでも既存の動作を壊すリスクがある] → 変更はシグネチャと初期化タイミングの移動のみに限定し、プロンプト内容やロジック分岐は一切変更しない。リファクタ後に手動で `workflow_dispatch` を実行し、実際に記事が生成されることを確認する
- [モックしたテストは実際の Gemini API のレスポンス形式変化を検知できない] → これは意図的な非ゴール。実APIとの整合性は引き続き手動確認・実運用でのモニタリングに委ねる
- [新規ワークフローファイルを追加することで CI 実行時間・Actions minutes が増える] → pytest スイート自体は軽量（外部通信なし）なので影響は小さいと判断

## Migration Plan

1. `generate_daily_post.py` をリファクタ（client 注入・トップレベル副作用の除去）。ロジック変更なしであることをコードレビューで確認
2. `scripts/requirements-dev.txt` を新設し `pytest` を追加
3. `scripts/test_generate_daily_post.py` を新設し、各関数のテストを実装
4. `.github/workflows/scripts-tests.yaml` を新設し、PR上でテストが実行されることを確認
5. マージ後、`daily-post.yaml` を `workflow_dispatch` で手動実行し、リファクタ後も正常に記事が生成されることを確認
6. ロールバック方針: 問題が起きた場合は当該コミットを revert する（本番依存やワークフローの構造自体は変えていないため、切り戻しは容易）

## Open Questions

- なし（本 change のスコープは明確。`scripts/patch_past_posts.py` は対象外と確定済み）
