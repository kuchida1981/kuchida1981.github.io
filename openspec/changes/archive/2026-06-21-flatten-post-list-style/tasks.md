## 1. ページ背景色の統一

- [x] 1.1 `assets/css/extended/custom.css` で `.list` の背景を `var(--theme)` にオーバーライドする

## 2. カードスタイルの廃止

- [x] 2.1 `assets/css/extended/custom.css` で `.post-entry` の `background`, `border`, `border-radius` をリセットし、`.post-entry:active` の `scale(0.96)` アニメーションを無効化する

## 3. ユーザー記事の左ボーダーアクセント

- [x] 3.1 `assets/css/extended/custom.css` で `.post-self` スタイルを左ボーダーに置換する（ライト: `rgba(60, 130, 210, 0.45)` / ダーク: `rgba(100, 170, 245, 0.50)`）

## 4. スクロールバーの修正

- [x] 4.1 `assets/css/extended/custom.css` で `.list:not(.dark)` のスクロールバー track/thumb を `var(--theme)` にオーバーライドする
