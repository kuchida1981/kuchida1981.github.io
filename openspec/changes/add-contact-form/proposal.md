## Why

サイトに問い合わせ手段がなく、読者が著者に連絡する導線が存在しない。グローバルメニューに "Contact" を追加し、自己ホスティングしている n8n をバックエンドとして使うことで、外部SaaSに依存せず問い合わせフォームを実現する。

## What Changes

- グローバルメニュー (`config.yml` の `menu.main`) に `Contact`（`/contact/`, weight: 15、末尾）を追加
- `/contact/` 専用ページを新設。お名前・メールアドレス・本文を入力するフォームを設置
- フォーム送信は `fetch()` による非同期POSTで、config.yml の `Params` に持たせた n8n Webhook URL 宛に送信し、ページ遷移なしで成功/失敗メッセージをその場に表示
- スパム対策として、CSSで非表示にしたハニーポット隠しフィールドと、フォーム描画時刻を送る hidden フィールド（送信時刻トラップ）を送信データに含める（判定ロジック自体はn8n側で実装、この変更のスコープ外）
- Markdown内の生HTML描画（`markup.goldmark.renderer.unsafe`）はサイト全体では有効化せず、`/contact/` 専用の layout（`layout: "contact"`）でフォームHTML・JSを直書きする
- 既存の拡張ポイント `assets/css/extended/custom.css` にスタイルを追加し、PaperMod テーマ本体には手を入れない

## Capabilities

### New Capabilities
- `contact-form`: グローバルメニューからの `/contact/` ページ導線、フォーム項目、n8n Webhookへの非同期送信、スパム対策用フィールド、送信結果のインラインフィードバックを扱う

### Modified Capabilities
(なし。既存 capability の要件変更はない)

## Impact

- `config.yml`: `menu.main` にエントリ追加、`Params` に n8n Webhook URL を追加
- `content/contact.md`（新規、`layout: "contact"` を指定するフロントマターのみ）
- `layouts/contact/single.html`（新規、フォームHTML・JS）
- `assets/css/extended/custom.css`（追記、フォームのスタイル）
- 影響を受けないもの: 既存の記事コンテンツ、`layouts/posts/*`、`layouts/_default/list.html`、n8n側のワークフロー定義（このリポジトリの範囲外）
