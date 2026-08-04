## Context

このサイトは Hugo (テーマ: PaperMod) で構築され、`publishDir: docs` の静的出力を GitHub Actions 経由で GitHub Pages にデプロイする完全な静的サイトである。サーバーサイドの実行環境は存在しない。一方で著者は n8n (`n8n.u-rei.com`) を自己ホスティングしており、Webhook トリガーからワークフローを起動できる。この既存インフラを問い合わせフォームの受け皿として使う。

`config.yml` では `markup.goldmark.renderer.unsafe` が未設定（デフォルト false）であり、Markdown コンテンツ中の生HTML（`<form>` など）はレンダリングされない。既存の拡張ポイントとして `assets/css/extended/custom.css`（PaperMod のカスタムCSS差し込み場所）と `layouts/partials/extend_head.html`（テーマの `head.html` から呼ばれるサイト全体スクリプト差し込み場所、現在は Google Analytics 用途）がある。ローカルの `layouts/` はテーマの `themes/papermod/layouts/` より優先される。

## Goals / Non-Goals

**Goals:**
- `/contact/` に問い合わせフォームページを追加し、グローバルメニュー末尾に "Contact" を配置する
- フォーム送信を n8n Webhook に対して非同期(fetch)で行い、ページ遷移なしで結果を表示する
- 軽量なスパム対策（ハニーポット・送信時刻トラップ）用のフィールドをフォームに含める
- サイト全体の Markdown レンダリング設定 (`unsafe`) を変更せずに、フォームページのみHTMLを直書きできるようにする

**Non-Goals:**
- n8n 側のワークフロー（Webhook受信 → スパム判定 → Discord通知）の構築。これは n8n インスタンス上で著者が別途行うインフラ作業であり、このリポジトリのコード変更には含まれない
- reCAPTCHA / Turnstile 等の外部スクリプトを使った高度なスパム対策
- 問い合わせへの自動返信・メール送信機能
- フォーム送信履歴の保存・管理画面

## Decisions

### 1. バックエンドは自己ホスティング n8n の Webhook、Discordへは n8n が中継
外部フォームSaaS（Formspree等）ではなく、既に稼働している n8n を使う。Discord Webhook URL のようなシークレットは n8n ワークフロー内にのみ保持され、静的サイトのコードやリポジトリには一切含まれない。サイト側が知るのは公開して問題ない n8n の Webhook URL のみ。

代替案として検討したもの:
- Formspree / Web3Forms 等の外部SaaS: セットアップは容易だが、データが第三者を経由し、著者の既存インフラ活用方針と合わない
- Google Forms 埋め込み/リダイレクト: メンテナンスフリーだがサイトの外観から外れる

### 2. `/contact/` はコンテンツ非依存の専用 layout で実装（サイト全体の unsafe HTML は有効化しない）
`content/contact.md` に `layout: "contact"` を指定するフロントマターのみを置き、実際のフォームHTML・JS は `layouts/contact/single.html`（ローカル `layouts/` 配下、テーマを上書きしない新規ディレクトリ）に直接記述する。Hugo のテンプレートは Goldmark を経由しないため、`markup.goldmark.renderer.unsafe` の設定に関係なく任意のHTMLを描画できる。

代替案として検討したもの:
- サイト全体で `unsafe: true` にして `content/contact.md` に生HTMLを書く: 今後すべての記事コンテンツで生HTMLが有効になり、意図しないマークアップ混入のリスクが広がるため却下
- shortcode 化: 現時点ではこのページ専用の用途しかなく、再利用の見込みがないため、専用 layout の方がシンプル

### 3. スパム対策はハニーポット＋送信時刻トラップのみ（判定はn8n側）
フロントエンドは以下の2つの hidden フィールドを送信データに含めるだけで、判定ロジックは持たない:
- ハニーポット: CSSで視覚的に隠した入力欄（例: `name="website"`）。人間は入力せず、bot は埋めがちなため、値が空でない場合は n8n 側で無視する想定
- 送信時刻トラップ: フォーム描画時刻を hidden フィールドとして送信し、n8n 側で「送信までの経過時間が短すぎる」場合を bot 疑いとして扱う想定

外部スクリプト（reCAPTCHA/Turnstile）を読み込まないことで、サイトのパフォーマンスと独立性を保つ。判定ロジック自体は n8n ワークフロー側の実装であり、このリポジトリのスコープ外。

### 4. n8n Webhook URL は `config.yml` の `Params` で管理
`layouts/contact/single.html` 内のテンプレート変数として `site.Params.contactWebhookURL`（仮称）を参照し、JS の `fetch()` 呼び出し先に埋め込む。ハードコードを避け、URLが変わった場合も `config.yml` の1箇所を直すだけで済む。

### 5. 送信結果はページ内にインライン表示
`<form>` の `submit` イベントを JS で `preventDefault()` し、`fetch()` の成否に応じて成功/失敗メッセージをDOMに表示する。ページ遷移を伴う素朴な `<form action="...">` POST は採用しない（CORS対応が前提になるが、これは n8n 側で対応済みの想定）。

## Risks / Trade-offs

- [n8n インスタンスがダウン/未設定の間はフォームが機能しない] → n8n ワークフロー構築が完了するまでは `/contact/` ページの公開（メニュー掲載）を見送る運用で対応する
- [Webhook URL が公開HTML/JSに含まれるため、誰でも直接POSTできる] → ハニーポット・時刻トラップは万能ではないが、コスト低く一定の自動投稿を抑制できる。より強固な対策が必要になった場合は将来的にTurnstile等の追加を検討する
- [n8n 側のCORS設定漏れによりfetchが失敗する] → design上の既知のリスクとして明記し、実装時・n8nワークフロー構築時に動作確認を行う（このリポジトリのタスクではなく運用上の確認事項）

## Migration Plan

新規ページ・新規メニュー項目の追加のみで、既存コンテンツやテンプレートへの破壊的変更はない。ロールバックは `config.yml` のメニューエントリと `content/contact.md` を削除するだけで完了する。

## Open Questions

- n8n ワークフロー（Webhook → スパム判定 → Discord通知）の構築タイミング。フロントエンド実装完了後、公開前に著者が別途行う想定
