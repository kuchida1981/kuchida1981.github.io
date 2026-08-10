# daily-post-script-testability Specification

## Purpose

`scripts/generate_daily_post.py` は daily-post パイプラインの中核として稼働し続けているが、自動テストが一切なく、モジュールの import 時に環境変数チェックや外部APIクライアント生成などの副作用が発生するため、Gemini API を実際に呼ばない範囲でテストを書くことができない。このケーパビリティは、同スクリプトが import 時に副作用を起こさず、外部API・ネットワークに依存しない自動テストで主要ロジックの正しさを検証できる状態、およびその検証が CI 上で継続的に実行される状態を定義する。

## Requirements

### Requirement: Import 時の副作用排除
`scripts/generate_daily_post.py` は、モジュールを `import` した時点で環境変数の検証・プロセス終了・外部APIクライアントの生成を行ってはならない（MUST NOT）。これらの処理は `main()` の呼び出し時にのみ実行されなければならない（MUST）。

#### Scenario: 環境変数未設定でも import が成功する
- **WHEN** `GEMINI_API_KEY` 環境変数が設定されていない状態で `scripts/generate_daily_post.py` を `import` する
- **THEN** `import` はエラーや `SystemExit` を発生させずに成功する

#### Scenario: main() 実行時に API キー未設定を検出する
- **WHEN** `GEMINI_API_KEY` 環境変数が未設定のまま `main()` を実行する
- **THEN** エラーメッセージが出力され、プロセスが終了する

### Requirement: Gemini クライアントの依存性注入
Gemini API を呼び出す関数（`generate_blog_post`, `generate_slug`）は、いずれもクライアントインスタンスを引数として受け取らなければならない（MUST）。関数内でモジュールレベルのグローバル変数を暗黙に参照してはならない（MUST NOT）。

#### Scenario: generate_blog_post がクライアントを引数で受け取る
- **WHEN** `generate_blog_post(client, feed_items)` を呼び出す
- **THEN** 渡された `client` インスタンスの `models.generate_content` が呼び出される
- **AND** 関数はグローバル変数の `client` を参照しない

### Requirement: 外部通信なしのテストカバレッジ
`scripts/generate_daily_post.py` の主要ロジック（`sanitize_slug`, `extract_title`, `save_post`, `fetch_rss_items`, `generate_blog_post`, `generate_slug`）には、Gemini API・RSS フィードへの実際のネットワークアクセスを行わない自動テストが存在しなければならない（MUST）。

#### Scenario: テストが外部ネットワークにアクセスしない
- **WHEN** `scripts/test_generate_daily_post.py` のテストスイートを実行する
- **THEN** すべてのテストはモック化された `feedparser.parse` およびモック化された Gemini クライアントのみを使用する
- **AND** 実際の外部ネットワーク呼び出しは発生しない

#### Scenario: スラッグ生成の境界値が検証される
- **WHEN** `sanitize_slug()` に空白・非ASCII文字・7語以上の入力を与える
- **THEN** 生成されるスラッグは kebab-case・小文字ASCII・6語以内のルールに従う

### Requirement: CI でのテスト実行
`scripts/generate_daily_post.py` に対するテストスイートは、CI 上で `pull_request` および `push`(master) イベントの両方で実行され、テストが失敗した場合はチェックが失敗しなければならない（MUST）。

#### Scenario: PR 上でテストが実行される
- **WHEN** master ブランチへの pull request が作成・更新される
- **THEN** `scripts/test_generate_daily_post.py` のテストスイートが CI 上で実行される
- **AND** テストが1件でも失敗した場合、当該 CI ジョブは失敗ステータスになる
