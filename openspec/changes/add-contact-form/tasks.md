## 1. 設定

- [x] 1.1 `config.yml` の `menu.main` に `identifier: contact, name: Contact, url: /contact/, weight: 15` を追加する
- [x] 1.2 `config.yml` の `Params` に n8n Webhook URL を保持するキー（例: `contactWebhookURL`）を追加する（値は仮のプレースホルダでよい。実URLは著者が後で設定する）

## 2. コンテンツページ

- [x] 2.1 `content/contact.md` を新規作成し、`layout: "contact"` を指定するフロントマターのみを記述する
  - 実装時に `layout: "contact"` ではなく `type: "contact"` を採用（Hugoのテンプレート探索ルール上、`layouts/contact/single.html` を解決するには `type` の指定が必要なため）

## 3. レイアウト（フォームHTML・JS）

- [x] 3.1 `layouts/contact/single.html` を新規作成し、お名前・メールアドレス・本文の入力欄と送信ボタンを持つ `<form>` を実装する
- [x] 3.2 フォームに、CSSで視覚的に隠したハニーポット用の隠しフィールドを追加する
- [x] 3.3 フォームに、描画時刻を保持する送信時刻トラップ用の hidden フィールドを追加し、テンプレート側またはJS側でページ描画時刻をセットする
- [x] 3.4 フォームの `submit` イベントをJSで `preventDefault()` し、`site.Params.contactWebhookURL` を送信先として `fetch()` によるJSON POSTを実装する
  - 実装時に判明: `{{ site.Params.contactWebhookURL | jsonify }}` をそのまま `<script>` に埋め込むと、Hugoのコンテキスト依存オートエスケープにより二重エスケープされてしまうバグがあった。`| safeJS` を追加して解消
- [x] 3.5 送信成功時・失敗時それぞれについて、ページ遷移なしでインラインにメッセージを表示するJSを実装する（成功メッセージ／失敗メッセージの出し分け）
- [x] 3.6 送信中は多重送信を防ぐため送信ボタンを一時的に無効化する

## 4. スタイル

- [x] 4.1 `assets/css/extended/custom.css` にフォーム・入力欄・送信ボタン・結果メッセージのスタイルを追加し、サイトの既存デザイン（PaperMod）と調和させる
- [x] 4.2 ハニーポットフィールドが画面上に見えず、かつスクリーンリーダー等の支援技術にも極力干渉しないスタイル（`position: absolute; left: -9999px` 等の一般的手法）になっていることを確認する

## 5. 動作確認

- [x] 5.1 `hugo server` でローカル起動し、グローバルメニューに "Contact" が表示され `/contact/` に遷移できることを確認する
- [x] 5.2 ブラウザの開発者ツールで、フォーム送信時に `fetch()` が `contactWebhookURL` 宛にお名前・メールアドレス・本文・ハニーポット・送信時刻を含むJSONをPOSTしていることを確認する
  - 実URLの代わりにダミーの `http://localhost:9999/webhook/contact-test` を一時設定し、ネットワークログで OPTIONS(CORSプリフライト) → POST の順にリクエストが飛ぶことを確認
- [x] 5.3 送信先エンドポイントが未設定/エラーを返す状態でも、失敗メッセージが正しく表示され、ページがクラッシュしないことを確認する
- [x] 5.4 モバイル幅でのフォーム表示・グローバルメニューの折りたたみ表示を確認する
  - 実行環境の制約でブラウザウィンドウの実リサイズができず、実機スクリーンショットでの確認は未実施。追加CSSは `max-width: 480px` の指定以外はすべて相対単位・flexboxで、PaperModの既存ブレークポイント（768px/900px/340px、`themes/papermod/assets/css/core/zmedia.css`）と衝突する固定px要素がないことをコードレビューで確認した
