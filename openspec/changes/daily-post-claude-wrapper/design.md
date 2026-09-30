## Context

- `daily-post.yaml` は GitHub がホストするランナー上で実行される。tailnet（Tailscale私設ネットワーク）には参加していない。
- `claude-code-openai-wrapper` はこのユーザーのローカルPC上で systemd `--user` サービスとして常駐し、Tailscale IP（`100.120.169.11:18789`）にのみバインドされている。認証は Claude CLI のサブスクリプション（`ANTHROPIC_API_KEY` は未設定）で、リクエストには wrapper 独自の `API_KEY` によるBearer認証が必要。
- 同一 tailnet 上には、この用途と無関係な機微ノードが同居している（`vaultwarden`＝パスワードマネージャー、`synology-nas`＝NAS）。ネットワーク到達範囲の設計はこれらを意識する必要がある。
- n8n（GCP VM）は既に同一 tailnet のメンバーとして wrapper を呼び出しているが、n8n はこの記事生成機能とは無関係な用途で運用されており、踏み台として使うと変更管理がこのリポジトリの外（n8n管理画面）に分散する。そのため本changeでは不採用。
- ローカルPCの電源状態・ネットワーク状態は、GitHub Actions側から見て完全には制御できない外部要因である。

## Goals / Non-Goals

**Goals:**
- daily-post の記事生成において、Claude Code（wrapper経由）を優先プロバイダとして使い、コスト（サブスク活用）と品質を改善する。
- wrapperに到達できない場合は自動的にGeminiにフォールバックし、既存の可用性（=記事が生成されPRが作られること）を落とさない。
- tailnet全体ではなく、CI用の経路を必要最小限（wrapperの該当ポートのみ）に絞る。
- 変更をこのリポジトリ内で完結させる（他プロジェクト・他システムへの新規結合を避ける）。

**Non-Goals:**
- 記事生成プロンプト自体の改善（RSSスニペット→WebFetchによる元記事取得など）は扱わない。将来の別changeとする。
- このPCをGitHub Actionsのセルフホストランナーにすることは扱わない。
- n8nを踏み台にする方式は扱わない。
- wrapper自体の変更（`claude-code-openai-wrapper`リポジトリ側の改修）は扱わない。疎通確認のみ行う。

## Decisions

### 1. 接続方式: Tailscale公式GitHub Actionでランナーを一時参加（案A採用）

`tailscale/github-action` を使い、ジョブ実行中だけランナーをtailnetに一時参加（ephemeral node）させる。認証には長期の pre-generated authkey ではなく **OAuth client**（`TS_OAUTH_CLIENT_ID` / `TS_OAUTH_CLIENT_SECRET`）を使う。OAuth clientはTailscale側で失効・スコープ管理がしやすく、Actionが自動的に短命のephemeral keyを発行するため、漏洩時の被害範囲と持続時間が抑えられる。

比較した案Bは、GitHub ActionsからHTTPS経由でn8nのwebhookを呼び、n8nが自身のtailnet経路でwrapperを中継する方式。tailnetに新規参加者を増やさない利点はあるが、無関係なn8nインスタンスに本機能専用のwebhookワークフローと認証情報管理を追加することになり、変更履歴がこのリポジトリだけで追えなくなる。ブログの記事生成パイプラインという単機能のために別システムへ恒常的な結合を作るコストの方が大きいと判断し、不採用とした。

### 2. ネットワーク到達範囲: Tailscale ACLでCI用タグを新設し、wrapperの該当ポートのみ許可

ephemeral nodeはデフォルトのACLポリシーのままだとtailnet内の他ノード（vaultwarden、synology-nas等）にも到達しうる。これを避けるため、Tailscale管理コンソールのACLポリシーに以下を追加する。

- 新規タグ `tag:ci-blog-daily-post` を定義し、`TS_OAUTH_CLIENT_ID`/`SECRET` にこのタグを持つephemeral nodeとしてのみ発行を許可する（OAuth client自体にタグを紐付ける）。
- wrapperが動くホストに `tag:claude-wrapper-server` を付与する（未付与なら追加）。
- ACLルールで `tag:ci-blog-daily-post` → `tag:claude-wrapper-server:18789` のみを許可し、それ以外のtailnet宛通信を拒否する。

この作業はTailscale管理コンソール（リポジトリ外）での手動作業であり、実装・レビューの前提条件とする。詳細な手順と検証方法は本ドキュメント末尾の「Tailscale側の手動作業と検証」に明記する。

### 3. フォールバック判定: `/health` による事前疎通確認 + プロバイダ統一

`generate_daily_post.py` の `main()` 冒頭で wrapper の `GET {CLAUDE_WRAPPER_BASE_URL}/health` を短いタイムアウト（例: 5秒）で呼び出す。

- 成功（200応答）→ `ClaudeProvider` を選択し、本文生成・slug生成の両方をClaudeで行う。
- 失敗（タイムアウト・接続拒否・非200）→ `GeminiProvider` にフォールバックし、両方をGeminiで行う。

プロバイダを実行途中で切り替えない（本文はClaude、slugはGeminiのような混在をしない）ことで、1記事内の文体・挙動の一貫性を保つ。両プロバイダは `generate(prompt: str) -> str` の共通インターフェースを持つ薄いラッパーとして実装し、既存の `generate_blog_post` / `generate_slug` はこのインターフェース経由で呼び出す形にリファクタする。

Tailscale接続ステップ（ワークフロー側）自体は `continue-on-error: true` にする。これにより、ACL設定ミスやOAuth clientの期限切れでtailscale接続が失敗しても、後続の `/health` 呼び出しが（到達できず）失敗するだけでGeminiフォールバックに自然に落ち、ジョブ全体は継続する。

**（レビューで判明した追加の分岐）** `/health` の疎通確認はあくまで「wrapperプロセスが応答するか」しか見ておらず、以下の2つの失敗モードは別途ハンドリングが必要と判明した:
- wrapperは到達可能だが `CLAUDE_WRAPPER_API_KEY` 等の設定が不足している場合 → 即エラー終了ではなく、Geminiへフォールバックする。
- health check後、実際の生成呼び出し（`chat.completions.create`）がタイムアウト・空応答・例外などで失敗した場合 → その場でジョブを失敗させるのではなく、`GEMINI_API_KEY` があればGeminiで本文・slugを生成し直す。

これらはspecs/daily-post-claude-provider/spec.mdに要件として追記済み。

### 4. Claude呼び出し方式: `openai` パッケージでwrapperのOpenAI互換エンドポイントを利用

wrapperは `/v1/chat/completions`（OpenAI互換）と `/v1/messages`（Anthropic互換）の両方を提供するが、`openai` パッケージの `OpenAI(base_url=..., api_key=...)` クライアントで `/v1/chat/completions` を叩く方式を採用する。理由:
- 追加の依存パッケージが `openai` 1つで済み、リクエスト/レスポンスの型もOpenAI SDKの標準的な形（`response.choices[0].message.content`）で扱える。
- wrapperの `/v1/models` から実際のモデルID（例: `claude-sonnet-4-6`）を取得可能だが、本changeでは既知のデフォルトモデルID（wrapper設定の `DEFAULT_MODEL` 相当）を明示的に指定する。動的な `/v1/models` 問い合わせは行わない（シンプルさ優先、Non-Goal）。

### 5. モデル選定

本文生成・slug生成ともに同一モデル（wrapperのデフォルトSonnet系モデル）を使う。slug生成のみ軽量モデル（Haiku系 `FAST_MODEL`）に分ける最適化も検討したが、要求が小さく呼び出し回数も1回増えるだけなので、実装の単純さを優先し本changeでは見送る（Open Questionsに記載）。

## Risks / Trade-offs

- **[Risk] ローカルPCの電源断・スリープ・ネットワーク断で毎回Geminiフォールバックに落ちる** → 記事の可用性は保たれるが、当初の目的（コスト・品質改善）が達成されない日が発生しうる。PR本文に実使用プロバイダを明記することで、日々の状況を可視化できるようにする。
- **[Risk] ACLポリシー設定を誤ると、CIランナーがtailnet内の機微ノード（vaultwarden、NAS）に到達できてしまう** → 「Tailscale側の手動作業と検証」節の手順に従い、ACLルールを設定後、実際に他ノードへ到達できないことを検証する（後述）。
- **[Risk] OAuth clientの認証情報がGitHub Secretsから漏洩した場合、tailnetへの参加経路として悪用されうる** → タグスコープを `tag:ci-blog-daily-post` に限定し、ACLでwrapperの1ポートのみに制限することで被害範囲を最小化する。定期的なOAuth client secretのローテーションを運用として推奨する。
- **[Trade-off] wrapperの `/health` 疎通確認とtailscale接続がジョブの実行時間を数秒〜数十秒押し上げる** → 日次バッチ処理であり許容範囲と判断。
- **[Risk] ACLポリシーの「意図」と実機での「実際のenforcement」に食い違いが観測されている** → Tailscale管理コンソールの「Tests」機能（`tag:ci-blog-daily-post`はwrapperの18789のみaccept、wrapperの22番・vaultwardenの80番・NASの5000番はdenyと定義）は**ポリシーの評価ロジックとしては正しいことを確認済み**。しかし、実際にOAuth client経由で発行した一時タグ付きノード（Dockerコンテナ）からの到達性テストでは、wrapper:18789には到達できず（同一ホスト上でのDockerブリッジ経由という特殊経路が原因の可能性が高い）、NAS:5000・vaultwarden:80には到達できてしまう（tailscaled再起動後も同様）という、ポリシーの意図と逆の結果が観測された。原因は未特定（enforcement伝搬の遅延、プラットフォーム依存のnetfilter適用の違いなど複数の仮説があるが未検証）。**本changeでは、Tailscale自身によるポリシーロジックの検証（Tests機能）が通っていることを設計上の根拠とし、実際のGitHub Actionsからの本番相当アクセス（tasks.md 8章の`workflow_dispatch`検証）を最終的な受け入れ確認として位置づける。** もし本番テストでも同様にNAS/vaultwardenへの到達が確認された場合は、別途Tailscaleサポートへの問い合わせ、または該当ノードのTailscaleクライアント再インストール等の追加調査が必要。

## Migration Plan

1. Tailscale側の手動作業（ACLポリシー、OAuth client発行）を完了させる（後述の手順）。
2. GitHub Secrets/Variablesに `CLAUDE_WRAPPER_BASE_URL`、`CLAUDE_WRAPPER_API_KEY`、`TS_OAUTH_CLIENT_ID`、`TS_OAUTH_CLIENT_SECRET` を登録する。
3. コード変更（`generate_daily_post.py` のプロバイダ抽象化、`daily-post.yaml` へのtailscaleステップ追加、`requirements.txt`、テスト追加）をPRとして作成する。
4. `workflow_dispatch` で `daily-post.yaml` を手動実行し、Claude経由で記事が生成されることを確認する（後述の検証手順）。
5. 意図的にwrapperを停止する等でフォールバック経路も検証する。
6. 問題なければ通常の日次cronに委ねる。ロールバックは、tailscaleステップとプロバイダ切り替えロジックを含むコミットをrevertするだけで、Gemini単体の元の挙動に戻せる（`GEMINI_API_KEY` は維持し続けるため）。

## Open Questions

- slug生成にHaiku系の軽量モデル（`FAST_MODEL`）を使う最適化を別changeで行うか。
- `/health` のタイムアウト秒数の具体的な値（暫定5秒）は実運用のレイテンシを見て調整が必要か。
- OAuth client secretのローテーション運用（頻度・手順）をどこまでこのchangeのスコープに含めるか、あるいは運用ドキュメント側の別課題とするか。

---

## Tailscale側の手動作業と検証（リポジトリ外、実装前提）

このセクションはTailscale管理コンソール上で行う、コード変更とは独立した作業と、その検証手順を明記する。実装（tasks.md）を進める前、および完了後の受け入れ確認として使う。

### 手動作業

1. **wrapperホストへのタグ付与**
   - Tailscale管理コンソール → Machines → wrapperが動くホスト（`100.120.169.11`）に `tag:claude-wrapper-server` を付与する。
2. **CI用OAuth clientの発行**
   - 管理コンソール → Settings → OAuth clients で新規OAuth clientを発行する。
   - スコープ: `Devices: Write`（ephemeral nodeの参加に必要な最小権限）。
   - 発行時に付与タグとして `tag:ci-blog-daily-post` を設定する（OAuth client自体にタグを紐付けることで、このclientから参加するノードは常にこのタグを持つ）。
   - 発行された Client ID / Client Secret を控える（この後GitHub Secretsに登録する）。
3. **ACLポリシーの追加**
   - 管理コンソール → Access Controls（ACL）のポリシーファイルに、以下相当のルールを追加する（既存のACL構造に合わせて統合すること。既存タグ定義がある場合はマージする）:
     ```jsonc
     {
       "tagOwners": {
         "tag:ci-blog-daily-post": ["autogroup:admin"],
         "tag:claude-wrapper-server": ["autogroup:admin"]
       },
       "acls": [
         {
           "action": "accept",
           "src": ["tag:ci-blog-daily-post"],
           "dst": ["tag:claude-wrapper-server:18789"]
         }
       ]
     }
     ```
   - 既存のvaultwarden・NAS等へのACLルールに `tag:ci-blog-daily-post` が含まれていないことを確認する（デフォルトdeny前提であれば、明示的な許可ルールを足さない限り到達できないはずだが、既存ポリシーが緩い場合は明示的な拒否も検討する）。
4. **GitHub Secretsへの登録**
   - `TS_OAUTH_CLIENT_ID`、`TS_OAUTH_CLIENT_SECRET`（手順2で発行したもの）
   - `CLAUDE_WRAPPER_BASE_URL`（例: `http://100.120.169.11:18789/v1`）
   - `CLAUDE_WRAPPER_API_KEY`（wrapperの `.env` の `API_KEY` と同じ値）

### 検証手順

1. **ACL到達範囲の検証（コード変更前でも実施可能）**
   - 上記OAuth clientを使い、手元またはテスト用ワークフローで一時的にtailnetへ参加するノードを作る。
   - そのノードから `curl http://100.120.169.11:18789/health` が成功することを確認する。
   - 同じノードから `synology-nas`（`100.65.90.127`）や `vaultwarden`（`100.123.122.116`）宛の疎通（ping/curl等）が**失敗する**ことを確認する。これがACL絞り込みの成否確認になる。
   - **実施結果（2026-10-01時点）**: Tailscale管理コンソールの「Access controls > Tests」機能でポリシーロジックの正しさは確認済み（保存時のテスト通過）。一方、同一ホスト上のDockerコンテナを使った実地到達性テストでは、wrapper:18789への到達失敗（同一ホストのDocker bridge経由という経路上の制約が原因の可能性）、NAS:5000・vaultwarden:80への到達成功（tailscaled再起動後も変わらず、原因未特定）という、意図と逆の結果になった。この食い違いは既知のリスクとして扱い、本番相当の検証（下記3.の`workflow_dispatch`テスト）を最終確認とする。
2. **正常系（Claude経由）の検証（コード変更後）**
   - `daily-post.yaml` を `workflow_dispatch` で手動実行する。
   - ワークフローのログでTailscale接続ステップが成功していることを確認する。
   - 生成された記事のPRに「Generated by Claude」等、Claude経由であることを示す表記が出ていることを確認する。
3. **フォールバック系の検証**
   - ローカルPC側で `systemctl --user stop claude-wrapper` 等により意図的にwrapperを停止した状態で `workflow_dispatch` を実行する。
   - `/health` 呼び出しが失敗し、Geminiにフォールバックして記事が生成されること、PRの表記が「Generated by Gemini (fallback)」等になることを確認する。
   - 検証後、`systemctl --user start claude-wrapper` で元に戻す。
4. **Tailscale接続失敗時のフォールバック検証（任意）**
   - OAuth clientを一時的に無効化する、または誤ったSecretを使うなどしてtailscale接続ステップ自体を失敗させ、`continue-on-error: true` によりジョブが継続し、Geminiフォールバックに落ちることを確認する。
