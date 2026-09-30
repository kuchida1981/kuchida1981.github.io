## Why

`daily-post.yaml` は現在 Gemini API（`GEMINI_API_KEY`、従量課金）で日次記事を生成しているが、ローカルPC上で稼働中の `claude-code-openai-wrapper`（Claude CLIサブスク認証、既に n8n から tailnet 経由で利用中）を使えば、追加コストなしでより高品質な記事生成に切り替えられる。GitHub Actions のホスト型ランナーは tailnet 外にあるため、そのままでは wrapper に到達できないが、Tailscale公式GitHub Actionでランナーを一時的にtailnetへ参加させることで解決できる。ローカルPCの起動状態に依存する構成になるため、Gemini への自動フォールバックを維持し、可用性を落とさない。

## What Changes

- `daily-post.yaml` に Tailscale 接続ステップを追加し、GitHub Actions ランナーを一時的に tailnet へ参加させ、`claude-code-openai-wrapper`（`100.120.169.11:18789`）に到達できるようにする。接続ステップは `continue-on-error: true` とし、失敗してもジョブ全体は継続する。
- `scripts/generate_daily_post.py` に記事生成のプロバイダ抽象化を導入する。起動時に wrapper の `/health` へ疎通確認し、成功時は Claude（wrapper の OpenAI 互換エンドポイント）、失敗・タイムアウト時は Gemini にフォールバックする。1回の実行内で本文生成とslug生成は同一プロバイダに統一する（プロバイダの混在はしない）。
- 記事生成プロンプトのロジック自体（RSSスニペットを用いた一発生成）は変更しない。WebFetchによる元記事取得は本changeのスコープ外。
- `scripts/requirements.txt` に `openai` パッケージを追加する（Claude wrapper呼び出し用。OpenAI互換エンドポイントを叩くため）。既存の `google-genai` はフォールバック用に維持する。
- `scripts/test_generate_daily_post.py` を更新し、プロバイダ切り替えロジック（health check成功/失敗の両分岐）のテストを追加する。
- 新規 GitHub Secrets/Variables: `CLAUDE_WRAPPER_BASE_URL`、`CLAUDE_WRAPPER_API_KEY`、`TS_OAUTH_CLIENT_ID`、`TS_OAUTH_CLIENT_SECRET`。既存の `GEMINI_API_KEY` は維持。
- PR本文に、実際に使用されたプロバイダ（Claude / Gemini fallback）を動的に出力する。
- **手動作業（リポジトリ外）**: Tailscale管理コンソールでのACLポリシー変更（CI専用タグの新設、wrapperノードの該当ポートのみへのアクセス許可）、および OAuth client の発行。詳細は `design.md` に明記し、実装・レビューの前提条件とする。

## Capabilities

### New Capabilities
- `daily-post-claude-provider`: daily-post パイプラインが Claude Code（ローカルwrapper、Tailscale経由）を優先プロバイダとして記事を生成し、到達不可時にGeminiへ自動フォールバックする振る舞いを定義する。

### Modified Capabilities
- `daily-post-dependency-pinning`: 固定バージョン管理の対象パッケージに `openai` を追加する（既存の `google-genai` 等の要件は変更しない）。
- `daily-post-script-testability`: 依存性注入の対象が「Geminiクライアント」から「プロバイダ（Claude/Gemini のいずれか）」に一般化される。テストは両プロバイダの分岐・切り替えロジックをモックで検証しなければならない。

## Impact

- **コード**: `.github/workflows/daily-post.yaml`、`scripts/generate_daily_post.py`、`scripts/requirements.txt`、`scripts/test_generate_daily_post.py`
- **外部システム**: このPC上の `claude-code-openai-wrapper`（変更なし、疎通確認のみ）、Tailscale管理コンソール（ACLポリシー・OAuth client、リポジトリ外の手動設定）
- **シークレット/変数**: GitHub Actions Secrets/Variables への4項目追加、既存 `GEMINI_API_KEY` は維持
- **運用**: ローカルPCの起動状態が記事の生成品質（Claude vs Geminiフォールバック）に影響するようになる。可用性そのもの（記事が生成されるか）は既存同様に維持される。
