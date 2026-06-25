## Why

記事の author でフィルタ（一覧表示）できる仕組みがない。現在すべての記事に `author` front matter があるが、taxonomy として登録されていないため `/authors/<name>/` のようなリストページが生成されない。AI 生成記事（Ghost Writer）と手書き記事（Kosuke Uchida）を区別して閲覧できるようにしたい。

## What Changes

- `config.yml` に `taxonomies` 定義を追加し、`authors` taxonomy を有効化する
- `layouts/partials/author.html` を作成し、記事ページの author 名から `/authors/<name>/` への リンクを付ける（PaperMod テーマのオーバーライド）
- 記事の front matter は変更不要（既存の `author: "Ghost Writer"` がそのまま taxonomy として機能する）

## Capabilities

### New Capabilities
- `author-taxonomy`: Hugo の taxonomy 機能を使った author 別記事フィルタリングと、記事ページからの author リンク

### Modified Capabilities

なし

## Impact

- `config.yml`: taxonomies セクション追加
- `layouts/partials/author.html`: 新規ファイル（テーマオーバーライド）
- Hugo が `/authors/` および `/authors/<name>/` ページを自動生成するようになる
