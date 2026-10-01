# daily-post-claude-provider Specification

## Purpose

daily-post パイプラインが、ローカルPC上で稼働する `claude-code-openai-wrapper`（Tailscale経由）を優先プロバイダとして記事を生成し、到達不可・設定不備・生成失敗のいずれの場合もGeminiへ自動フォールバックする振る舞いを定義する。

## Requirements

### Requirement: Claudeを優先プロバイダとして使用する
daily-post 生成パイプラインは、記事生成の実行開始時に `claude-code-openai-wrapper`（Tailscale経由、`CLAUDE_WRAPPER_BASE_URL`）の `/health` エンドポイントへ疎通確認を行い、成功した場合はClaude（wrapperのOpenAI互換エンドポイント経由）を本文生成・slug生成の双方に使用しなければならない（MUST）。

#### Scenario: health check成功時にClaudeが両方に使われる
- **WHEN** `/health` エンドポイントへのリクエストがタイムアウト内に200を返す
- **THEN** 本文生成（`generate_blog_post`相当）はClaudeプロバイダ経由で行われる
- **AND** slug生成（`generate_slug`相当）もClaudeプロバイダ経由で行われる

### Requirement: Geminiへの自動フォールバック
daily-post 生成パイプラインは、`/health` への疎通確認が失敗（タイムアウト・接続エラー・非200応答のいずれか）した場合、Gemini（既存の `google-genai` クライアント）にフォールバックし、本文生成・slug生成の双方をGeminiで実行しなければならない（MUST）。

#### Scenario: health check失敗時にGeminiへフォールバックする
- **WHEN** `/health` エンドポイントへの接続がタイムアウトする、または接続エラーになる、または200以外の応答を返す
- **THEN** 本文生成はGeminiプロバイダ経由で行われる
- **AND** slug生成もGeminiプロバイダ経由で行われる

### Requirement: プロバイダの混在禁止
daily-post 生成パイプラインは、1回の実行（1記事の生成）において、本文生成とslug生成に異なるプロバイダ（ClaudeとGemini）を混在させてはならない（MUST NOT）。

#### Scenario: 同一実行内でプロバイダが統一されている
- **WHEN** 1回の記事生成処理が完了する
- **THEN** 本文生成とslug生成の両方が同一プロバイダ（ClaudeまたはGeminiのいずれか一方のみ）で行われている

### Requirement: 使用プロバイダの明示
daily-post 生成パイプラインは、実際に使用したプロバイダ（Claude、またはGeminiフォールバック）を判別できる情報を出力しなければならない（MUST）。この情報はPull Requestの本文に反映される。

#### Scenario: Claude使用時の出力
- **WHEN** Claudeプロバイダで記事が生成される
- **THEN** 生成結果に付随する出力（`GITHUB_OUTPUT`等）に、Claudeが使用されたことを示す情報が含まれる

#### Scenario: Geminiフォールバック使用時の出力
- **WHEN** Geminiプロバイダへのフォールバックで記事が生成される
- **THEN** 生成結果に付随する出力に、Geminiへのフォールバックが発生したことを示す情報が含まれる

### Requirement: Claude設定不備時のフォールバック
daily-post 生成パイプラインは、`/health` の疎通確認には成功していても、Claude利用に必要な設定（`CLAUDE_WRAPPER_BASE_URL` または `CLAUDE_WRAPPER_API_KEY`）が未設定・空である場合、エラー終了せずGeminiにフォールバックしなければならない（MUST）。Geminiへのフォールバックも不可能な場合（`GEMINI_API_KEY` も未設定）にのみ、エラーを出力してプロセスを終了する（MUST）。

#### Scenario: wrapperは到達可能だがAPI keyが未設定の場合にGeminiへフォールバックする
- **WHEN** `/health` への疎通確認は成功するが、`CLAUDE_WRAPPER_API_KEY` が未設定である
- **AND** `GEMINI_API_KEY` は設定されている
- **THEN** プロセスは終了せず、Geminiプロバイダで記事生成が行われる

#### Scenario: Claudeもフォールバック先のGeminiも利用できない場合はエラー終了する
- **WHEN** Claude利用に必要な設定が不足しており、かつ `GEMINI_API_KEY` も未設定である
- **THEN** エラーメッセージを出力してプロセスを終了する

### Requirement: 生成中の失敗時のフォールバック
daily-post 生成パイプラインは、Claudeが選択された状態で実際の本文生成呼び出し（`generate_blog_post`相当）が例外（空応答・接続エラー等を含む）を発生させた場合、`GEMINI_API_KEY` が利用可能であればGeminiで本文生成・slug生成をやり直し、実際に使用したプロバイダとして `gemini-fallback` を報告しなければならない（MUST）。`GEMINI_API_KEY` も利用できない場合は、エラーを出力してプロセスを終了する（MUST）。

#### Scenario: Claude生成失敗時にGeminiで再生成する
- **WHEN** Claudeプロバイダが選択され、本文生成呼び出しが例外を発生させる
- **AND** `GEMINI_API_KEY` が設定されている
- **THEN** Geminiプロバイダで本文生成・slug生成がやり直される
- **AND** 使用プロバイダの出力は `gemini-fallback` になる

#### Scenario: Claude生成失敗時にGeminiも利用できない場合はエラー終了する
- **WHEN** Claudeプロバイダが選択され、本文生成呼び出しが例外を発生させる
- **AND** `GEMINI_API_KEY` が未設定である
- **THEN** エラーメッセージを出力してプロセスを終了する

### Requirement: CIランナーのtailnet参加とフォールバック耐性
`daily-post.yaml` ワークフローは、記事生成ステップの前にTailscale公式GitHub Action経由でランナーを一時的にtailnetへ参加させるステップを実行しなければならない（MUST）。このステップは失敗してもワークフロー全体を失敗させてはならない（MUST NOT）。

#### Scenario: tailscale接続ステップが成功する
- **WHEN** Tailscale接続ステップがOAuth client認証で正常に完了する
- **THEN** 後続の記事生成ステップがwrapperの `/health` に到達可能な状態で実行される

#### Scenario: tailscale接続ステップが失敗してもジョブが継続する
- **WHEN** Tailscale接続ステップが（OAuth client期限切れ・ACL設定不備等により）失敗する
- **THEN** ワークフローは中断されず、後続の記事生成ステップが実行される
- **AND** `/health` への疎通確認が失敗し、Geminiフォールバックが使用される
