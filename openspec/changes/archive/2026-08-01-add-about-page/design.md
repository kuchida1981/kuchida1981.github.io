## Context

サイトは Hugo + PaperMod テーマの静的サイトで、`content/services.md` のような単一 Markdown ページ + `layout: page` の型で新規ページを追加する既存パターンがある。トップページは PaperMod の `profileMode`（`themes/papermod/layouts/partials/index_profile.html`）で構成されており、今回の変更では触れない。メニューは `config.yml` の `menu.main` に配列で定義されている（`weight` で順序制御）。

## Goals / Non-Goals

**Goals:**
- `/about/` に、経歴・技術スタック・実績の骨組みを持つ自己紹介ページを追加する
- `menu.main` に `About` を追加し、`Services` / `Posts` と並べて表示する
- 既存の `services.md` と同じ実装パターン（frontmatter + `layout: page`）を踏襲し、レイアウトやテンプレートの新規実装を避ける

**Non-Goals:**
- 連絡導線（メール・SNS・フォーム）の実装
- トップページ `profileMode` の変更
- `content/services.md` の内容変更
- 経歴・実績の本文の最終確定（今回は例文を含む骨組みのみ）

## Decisions

- **既存の `page` レイアウトを流用する**: PaperMod の `_default`/`page` レイアウトで十分に要件を満たせるため、カスタムレイアウトや `layouts/about/` の新設は行わない。`services.md` と同一パターンにすることで保守コストを増やさない。
- **メニューの `weight` は `Services`(5) と `Posts`(10) の間、または前後に配置する**: 具体的には `Services` の直後・`Posts` の前（`weight: 7` 程度）に置き、トップページに近い自己紹介 → サービス → 記事、という導線の自然さを優先する。
- **本文は例文込みの骨組みとして記述する**: ユーザーが後で実際の経歴・スキル・実績に差し替える前提のため、プレースホルダーではなくそのまま公開しても不自然でない程度の下書き文章を書く。

## Risks / Trade-offs

- [下書き文章がそのまま公開され、実態と異なる情報になる] → 実装後にユーザー自身が内容を確認・編集する前提とし、tasks.md に「内容の確認・編集は別途ユーザーが行う」旨を明記する
- [メニュー順序の変更がトップナビの見た目に影響する] → 影響は追加エントリ1件のみで、既存メニュー項目の位置・挙動は変えないため軽微
