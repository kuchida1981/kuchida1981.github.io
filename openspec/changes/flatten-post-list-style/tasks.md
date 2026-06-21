## 1. ページ背景色の統一

- [ ] 1.1 `themes/papermod/assets/css/core/theme-vars.css` から `.list` と `.dark.list` のブロックを削除する

## 2. カードスタイルの廃止

- [ ] 2.1 `themes/papermod/assets/css/common/post-entry.css` の `.post-entry` から `background: var(--entry)`, `border-radius: var(--radius)`, `border: 1px solid var(--border)` を削除する

## 3. ユーザー記事の左ボーダーアクセント

- [ ] 3.1 `assets/css/extended/custom.css` の `.post-self` スタイルを左ボーダーに置換する（ライト: `border-left: 3px solid rgba(60, 130, 210, 0.45)` / ダーク: `border-left: 3px solid rgba(100, 170, 245, 0.50)`、hover の背景色も削除、`padding-left` を調整）
