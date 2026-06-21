## 1. Slug 生成機能の追加

- [x] 1.1 `generate_slug(title: str) -> str` 関数を追加する。Gemini API にタイトルを渡して英語スラッグを生成する。プロンプトは「2〜6語、kebab-case、ASCII only、スラッグのみ出力」を指示する内容にする
- [x] 1.2 `sanitize_slug(raw: str) -> str` 関数を追加する。ASCII 英数字・ハイフン以外の除去、連続ハイフン統合、先頭末尾ハイフン除去、6語制限、空文字時の `daily-news` フォールバックを行う

## 2. save_post の変更

- [x] 2.1 `save_post()` の引数に slug を追加し、ファイル名を `{today_str}-{slug}.md` に変更する
- [x] 2.2 `main()` で記事生成後に title を使って `generate_slug()` を呼び出し、取得した slug を `save_post()` に渡すように修正する。`generate_slug()` が例外を投げた場合は `daily-news` にフォールバックする
