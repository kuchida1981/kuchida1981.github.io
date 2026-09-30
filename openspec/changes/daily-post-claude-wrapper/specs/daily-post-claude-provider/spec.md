## ADDED Requirements

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

### Requirement: CIランナーのtailnet参加とフォールバック耐性
`daily-post.yaml` ワークフローは、記事生成ステップの前にTailscale公式GitHub Action経由でランナーを一時的にtailnetへ参加させるステップを実行しなければならない（MUST）。このステップは失敗してもワークフロー全体を失敗させてはならない（MUST NOT）。

#### Scenario: tailscale接続ステップが成功する
- **WHEN** Tailscale接続ステップがOAuth client認証で正常に完了する
- **THEN** 後続の記事生成ステップがwrapperの `/health` に到達可能な状態で実行される

#### Scenario: tailscale接続ステップが失敗してもジョブが継続する
- **WHEN** Tailscale接続ステップが（OAuth client期限切れ・ACL設定不備等により）失敗する
- **THEN** ワークフローは中断されず、後続の記事生成ステップが実行される
- **AND** `/health` への疎通確認が失敗し、Geminiフォールバックが使用される
