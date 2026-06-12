## Context

Hugo + PaperMod テーマを使用した静的サイト（GitHub Pages）。現状、アクセス解析の仕組みは存在しない。PaperMod の `extend_head.html` パーシャルは、web-analytics を挿入するためのオーバーライドポイントとして明示的に設計されている。

## Goals / Non-Goals

**Goals:**
- GA4 トラッキングスクリプトを全ページの `<head>` に挿入する
- 本番ビルドのみで計測し、ローカル開発中は GA にデータを送信しない
- テーマファイル（`themes/`）を変更せず、テーマ更新耐性を確保する
- 測定 ID をコード内に散在させず、`config.yml` で一元管理する

**Non-Goals:**
- Cookie 同意バナー・プライバシーポリシーページの作成
- イベントトラッキング（ページビュー以外のカスタムイベント）
- Google Tag Manager の利用

## Decisions

### D1: extend_head.html オーバーライドを使用する

`layouts/partials/extend_head.html` を新規作成することで、テーマのオーバーライドポイントを活用する。

- **採用理由**: PaperMod が web-analytics 用途に設計した公式の拡張ポイント。テーマのアップデートで `themes/papermod/` が書き変わっても影響を受けない
- **代替案**: Hugo 組み込みの `_internal/google_analytics.html` テンプレート（`services.googleAnalytics.ID` で有効化）
  - 却下理由: Hugo の内部テンプレートは gtag.js の形式が古い場合があり、Google が生成する最新のスニペットと一致しない可能性がある

### D2: 測定 ID は config.yml の Params に置く

```yaml
Params:
  googleAnalyticsID: "G-QSVPG0XQ59"
```

テンプレート内でハードコードせず、`{{ site.Params.googleAnalyticsID }}` で参照する。

- **採用理由**: 設定の一元管理、ID の変更時に1箇所のみ修正すればよい

### D3: hugo.IsProduction で本番限定にする

```html
{{- if hugo.IsProduction }}
... gtag.js ...
{{- end }}
```

`hugo server` 時は `hugo.IsProduction` が `false` になるため、開発中は GA にデータが送信されない。

## Risks / Trade-offs

- **外部スクリプト依存** → `https://www.googletagmanager.com` が利用不可の場合、スクリプト読み込みがブロックされる可能性がある。`async` 属性によりページ描画はブロックしない。
- **プライバシー** → 訪問者のデータが Google に送信される。必要に応じて将来的にプライバシーポリシーの整備を検討。
- **本番判定の依存** → GitHub Actions での `hugo build` が `--environment production` なしで実行される場合、`hugo.IsProduction` が `false` になり計測されない。CI/CD の設定を確認する必要がある。
