## 1. 過去記事のパッチ処理

- [x] 1.1 過去の自動生成記事（`content/posts/*-daily-news.md`）のフロントマターに `author: "Ghost Writer"` を一括追加するスクリプト `scripts/patch_past_posts.py` を作成する
- [x] 1.2 スクリプトを実行し、過去の自動生成記事がすべて `author: "Ghost Writer"` を持つように更新されたことを確認する

## 2. 自動投稿スクリプトの修正

- [x] 2.1 `scripts/generate_daily_post.py` 内のフロントマターテンプレートを変更し、`author: "Ghost Writer"` を追加する

## 3. Hugo テンプレートのカスタマイズ

- [x] 3.1 テーマの `themes/papermod/layouts/_default/list.html` を `layouts/_default/list.html` にコピーする
- [x] 3.2 コピーした `layouts/_default/list.html` 内の各記事カードのクラス設定（`$class`）ロジックを修正し、手動記事判定（`author` が `"Ghost Writer"` ではない場合）のときに `post-self` クラスを付与する処理を追加する

## 4. スタイリングの追加

- [x] 4.1 `assets/css/extended/custom.css` ファイルを作成する
- [x] 4.2 `custom.css` にライトモードおよびダークモード用の `.post-entry.post-self` の背景色およびボーダー色を定義する

## 5. 動作確認

- [x] 5.1 ローカルのHugoサーバーを起動する
- [x] 5.2 ブラウザで記事一覧ページを表示し、手動記事（例: `hello-world.md`）が指定した背景色でハイライトされ、自動生成されたニュース記事（例: `*-daily-news.md`）が標準の背景色で表示されていることを確認する
- [x] 5.3 ライトモード・ダークモードを切り替え、それぞれの背景色が正しく表示されることを確認する

