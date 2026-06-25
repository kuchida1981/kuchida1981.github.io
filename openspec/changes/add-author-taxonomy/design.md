## Context

Hugo ブログ（PaperMod テーマ）で、記事の `author` front matter は設定済みだが taxonomy として登録されていない。Hugo の taxonomy 機能を使えば、設定追加とテンプレートオーバーライドだけで author 別フィルタを実現できる。

現状:
- `config.yml` に `taxonomies` セクションなし（Hugo デフォルトの `tags` / `categories` のみ有効）
- 全142件の記事が `author: "Ghost Writer"` を持つ
- PaperMod の `author.html` パーシャルは author 名をプレーンテキストで表示（リンクなし）

## Goals / Non-Goals

**Goals:**
- Hugo taxonomy として `authors` を有効化し、`/author/` および `/author/<name>/` ページを自動生成する
- 記事ページの author 名から taxonomy ページへリンクする

**Non-Goals:**
- ナビゲーションメニューへの Authors リンク追加
- 共著（複数 author）対応
- author プロフィールページのカスタマイズ
- 既存記事の front matter 変更

## Decisions

### 1. Hugo 標準の taxonomy 機能を使う

Hugo に組み込みの taxonomy 機能があり、`config.yml` に1行追加するだけで有効化できる。カスタムテンプレートやプラグインは不要。

代替案: カスタムの list テンプレートを自前で作る → 不要な複雑さ。taxonomy で十分。

### 2. `taxonomies` セクションを明示定義する

Hugo はデフォルトで `tags` と `categories` を暗黙的に有効化するが、`taxonomies` セクションを明示すると**暗黙定義が上書きされる**。そのため `tag`, `category`, `author` の3つすべてを明示する必要がある。

```yaml
taxonomies:
  tag: tags
  category: categories
  author: authors
```

### 3. `layouts/partials/author.html` でテーマをオーバーライドする

PaperMod の `themes/papermod/layouts/partials/author.html` はプレーンテキスト表示。プロジェクトルートの `layouts/partials/author.html` に同名ファイルを置くことで Hugo のテンプレート優先順位により自動的にオーバーライドされる。テーマ本体は編集しない。

### 4. `urlize` でスラッグを生成する

Hugo の `urlize` 関数を使って author 名から URL スラッグを生成する（例: `"Ghost Writer"` → `ghost-writer`）。これは Hugo が taxonomy ページの URL を生成する方式と一致する。

## Risks / Trade-offs

- [Risk] `taxonomies` を明示定義する際に `tag`/`category` を書き忘れると既存の tags/categories ページが消える → 3つとも明示することで回避
- [Risk] author 名のスラッグ化で想定外の URL が生成される可能性 → 現状の author 名（`Ghost Writer`, `Kosuke Uchida`）は ASCII のみなので問題なし
