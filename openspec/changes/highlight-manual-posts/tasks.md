## 1. 自動投稿スクリプトの修正

- [ ] 1.1 `scripts/generate_daily_post.py` 内のフロントマターテンプレートを変更し、`author: "Ghost Writer"` を追加する

## 2. Hugo テンプレートのカスタマイズ

- [ ] 2.1 テーマの `themes/papermod/layouts/_default/list.html` を `layouts/_default/list.html` にコピーする
- [ ] 2.2 コピーした `layouts/_default/list.html` 内の各記事カードのクラス設定（`$class`）ロジックを修正し、手動記事判定（`author != "Ghost Writer"` かつファイル名に `-daily-news` が含まれない）のときに `post-self` クラスを付与する処理を追加する

## 3. スタイリングの追加

- [ ] 3.1 `assets/css/extended/custom.css` ファイルを作成する
- [ ] 3.2 `custom.css` にライトモードおよびダークモード用の `.post-entry.post-self` の背景色およびボーダー色を定義する

## 4. 動作確認

- [ ] 4.1 ローカルのHugoサーバーを起動する
- [ ] 4.2 ブラウザで記事一覧ページを表示し、手動記事（例: `hello-world.md`）が指定した背景色でハイライトされ、自動生成されたニュース記事（例: `*-daily-news.md`）が標準の背景色で表示されていることを確認する
- [ ] 4.3 ライトモード・ダークモードを切り替え、それぞれの背景色が正しく表示されることを確認する
