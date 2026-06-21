## Why

自動生成ブログ記事のファイル名が `YYYY-mm-dd-daily-news.md` で固定されており、ファイル名から記事の内容を判別できない。記事タイトルは毎回ユニークに生成されているので、ファイル名（= URL スラッグ）にも内容を反映させたい。

## What Changes

- 記事生成後に Gemini API を追加で1回呼び出し、日本語タイトルから英語スラッグ（2〜6語、kebab-case）を生成する
- ファイル名を `YYYY-mm-dd-<slug>.md` 形式に変更する（例: `2026-06-20-adobe-ai-agents-creative-cloud.md`）
- スラッグ生成に失敗した場合は従来の `daily-news` にフォールバックする
- 記事生成プロンプトは一切変更しない（関心の分離）
- 既存記事のファイル名は変更しない

## Capabilities

### New Capabilities

- `filename-slug-generation`: 記事タイトルからファイル名用の英語スラッグを生成する機能

### Modified Capabilities

- `blog`: "Automated Daily Content" の要件変更 — ファイル名が固定の `daily-news` から内容に応じたスラッグに変わる

## Impact

- `scripts/generate_daily_post.py`: slug 生成関数の追加、`save_post()` のファイル名生成ロジック変更
- URL 構造: 新規記事の URL が `/posts/YYYY/MM/YYYY-mm-dd-<slug>/` になる（既存記事は影響なし）
- API コスト: Gemini API 呼び出しが1日あたり1回追加（入出力トークン数はごくわずか）
- ワークフロー (`daily-post.yaml`): 変更不要
