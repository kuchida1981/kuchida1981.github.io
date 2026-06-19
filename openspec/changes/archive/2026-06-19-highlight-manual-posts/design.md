## Context

現在、手動で作成した記事（例: `hello-world.md`）と、毎日自動生成される記事（`YYYY-MM-DD-daily-news.md`）が混在していますが、どちらもフロントマターに `author` が設定されていません。また、一覧ページではすべて同じスタイル（デフォルトのカード形式）で表示されています。
ユーザーが自身の記事を視覚的にアピールし、かつAIによる自動投稿であることを明確にするために、これらを区別する仕組みが必要です。

## Goals / Non-Goals

**Goals:**
- 自動生成される記事に `author: "Ghost Writer"` を設定する。
- 過去の自動生成記事（`*-daily-news.md`）に対しても `author: "Ghost Writer"` を一括付与し、データを綺麗に揃える。
- 手動記事を記事一覧ページでハイライト表示する。
- ライトモード・ダークモード両方において、自然に調和するハイライトカラーを設定する。

**Non-Goals:**
- 特になし（すべてのAI記事にauthorをパッチするため、後方互換用の複雑な条件分岐は不要となります）。

## Decisions

### Decision 1: AI記事の判別ロジックの簡素化
過去の自動生成記事に `author: "Ghost Writer"` を一括で付与するため、テンプレート（`list.html`）内でのAI記事・手動記事の判別ロジックを大幅にシンプルにします。

- **AI記事の条件**:
  - `author` が `"Ghost Writer"` であるもの
- **手動記事の条件**:
  - `author` が上記以外、または未指定であるもの

**Hugo テンプレートでの実装コードイメージ:**
```go-html-template
{{- $isAI := eq (.Param "author") "Ghost Writer" }}
{{- if not $isAI }}
  {{- $class = printf "%s post-self" $class }}
{{- end }}
```

### Decision 2: 過去記事のパッチ処理
過去の自動生成記事（`content/posts/*-daily-news.md`）に対して、フロントマターに `author: "Ghost Writer"` を自動挿入する Python スクリプト（`scripts/patch_past_posts.py`）を作成・実行します。
これにより、フロントマターに `author` フィールドが存在しない古いAI記事が一括で更新されます。

### Decision 3: スタイリングとダークモード対応
PaperModテーマが提供するカスタムCSS拡張機能を利用し、`assets/css/extended/` 配下にカスタムCSSを配置してハイライトを行います。

PaperModのテーマカラー変数（`--entry` など）と調和しつつ、手動記事（`.post-self`）が引き立つように以下の配色を採用します。

- **ライトモード**:
  - 背景色 (`background`): `rgba(30, 144, 255, 0.05)` (極めて薄いブルー)
  - 枠線 (`border`): `1px solid rgba(30, 144, 255, 0.15)`
- **ダークモード (`.dark` クラスが body に付与される、またはシステム設定)**:
  - 背景色 (`background`): `rgba(30, 144, 255, 0.1)` (少し濃いめのブルー)
  - 枠線 (`border`): `1px solid rgba(30, 144, 255, 0.25)`

これにより、テーマの文字色（`--primary` などのコントラスト）を崩すことなく、カード単体の背景のみを上品に浮き上がらせることができます。

## Risks / Trade-offs

- **[Risk]** 130以上の過去記事ファイルを一括で書き換えるため、Gitコミットの差分が一時的に大きくなる。
  - **[Mitigation]** 自動化スクリプトを用いて正確に変更を適用し、レビューが容易なように `author: "Ghost Writer"` を追加する以外の変更を行わないようにする。
