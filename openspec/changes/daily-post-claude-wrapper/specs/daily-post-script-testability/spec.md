## MODIFIED Requirements

### Requirement: Import 時の副作用排除
`scripts/generate_daily_post.py` は、モジュールを `import` した時点で環境変数の検証・プロセス終了・外部APIクライアント（Claude用・Gemini用いずれも）の生成・wrapperへのヘルスチェック通信を行ってはならない（MUST NOT）。これらの処理は `main()` の呼び出し時にのみ実行されなければならない（MUST）。

#### Scenario: 環境変数未設定でも import が成功する
- **WHEN** `GEMINI_API_KEY` および `CLAUDE_WRAPPER_API_KEY` 環境変数が設定されていない状態で `scripts/generate_daily_post.py` を `import` する
- **THEN** `import` はエラーや `SystemExit` を発生させずに成功する

#### Scenario: main() 実行時にプロバイダ選択に必要な設定不足を検出する
- **WHEN** 選択されたプロバイダ（health check結果に基づく）に必要な環境変数（Claude利用時は `CLAUDE_WRAPPER_BASE_URL`/`CLAUDE_WRAPPER_API_KEY`、Geminiフォールバック時は `GEMINI_API_KEY`）が未設定のまま `main()` を実行する
- **THEN** エラーメッセージが出力され、プロセスが終了する

### Requirement: プロバイダの依存性注入
記事生成を行う関数（本文生成・slug生成に相当する関数）は、いずれも使用するプロバイダ（ClaudeまたはGeminiのクライアントをラップしたオブジェクト）を引数として受け取らなければならない（MUST）。関数内でモジュールレベルのグローバル変数や、特定プロバイダへの決め打ちを暗黙に参照してはならない（MUST NOT）。

#### Scenario: 本文生成関数がプロバイダを引数で受け取る
- **WHEN** 本文生成関数をプロバイダオブジェクトとRSSアイテムを渡して呼び出す
- **THEN** 渡されたプロバイダオブジェクトの生成メソッドが呼び出される
- **AND** 関数はグローバル変数のクライアントを参照しない

#### Scenario: slug生成関数がプロバイダを引数で受け取る
- **WHEN** slug生成関数をプロバイダオブジェクトとタイトルを渡して呼び出す
- **THEN** 渡されたプロバイダオブジェクトの生成メソッドが呼び出される
- **AND** 関数はグローバル変数のクライアントを参照しない

### Requirement: 外部通信なしのテストカバレッジ
`scripts/generate_daily_post.py` の主要ロジック（`sanitize_slug`, `extract_title`, `save_post`, `fetch_rss_items`, 本文生成関数, slug生成関数, プロバイダ選択ロジック）には、Gemini API・Claude wrapper・RSS フィードへの実際のネットワークアクセスを行わない自動テストが存在しなければならない（MUST）。

#### Scenario: テストが外部ネットワークにアクセスしない
- **WHEN** `scripts/test_generate_daily_post.py` のテストスイートを実行する
- **THEN** すべてのテストはモック化された `feedparser.parse`、モック化されたClaude/Geminiクライアント、モック化されたヘルスチェック応答のみを使用する
- **AND** 実際の外部ネットワーク呼び出しは発生しない

#### Scenario: スラッグ生成の境界値が検証される
- **WHEN** `sanitize_slug()` に空白・非ASCII文字・7語以上の入力を与える
- **THEN** 生成されるスラッグは kebab-case・小文字ASCII・6語以内のルールに従う

#### Scenario: プロバイダ選択ロジックが両分岐でテストされる
- **WHEN** ヘルスチェックが成功する場合と失敗する場合のそれぞれをモックで再現してプロバイダ選択ロジックを実行する
- **THEN** 成功時はClaudeプロバイダが選択され、失敗時はGeminiプロバイダが選択されることがテストで検証される

### Requirement: CI でのテスト実行
`scripts/generate_daily_post.py` に対するテストスイートは、CI 上で `pull_request` および `push`(master) イベントの両方で実行され、テストが失敗した場合はチェックが失敗しなければならない（MUST）。

#### Scenario: PR 上でテストが実行される
- **WHEN** master ブランチへの pull request が作成・更新される
- **THEN** `scripts/test_generate_daily_post.py` のテストスイートが CI 上で実行される
- **AND** テストが1件でも失敗した場合、当該 CI ジョブは失敗ステータスになる
