## Context

- サイトは Hugo(テーマ: PaperMod)。`content/about.md`・`content/playground.md` はいずれも `layout: "page"` の単一 Markdown ページで、専用テンプレートは持たない。
- `content/about.md` の「実績・関わってきた領域」セクションには既に箇条書きレベルの実績一覧があるが、案件単位の詳細(課題・対応・成果)は書かれていない。
- ナビゲーションは `config.yml` の `menu.main` で管理。現在は About(weight 1)→ Playground(weight 5)→ Posts(weight 10)→ Contact(weight 20)の順。
- ケーススタディの元データは `resume2/data/career.yaml`(本リポジトリの外、`resume2` ワーキングディレクトリ)。narrative(challenge/actions/outcome)をそのまま転記はせず、匿名化・サイト向けの文体に書き直す。

## Goals / Non-Goals

**Goals:**
- 実務実績を課題・対応・成果の3構成で伝える新規ページを追加し、発注判断の材料を提供する
- 既存ページ(about.md, playground.md)と同じ Markdown + `layout: "page"` パターンを踏襲し、新規レイアウト/ショートコードの実装は行わない
- config.yml の menu に導線を追加し、About の次に見つけやすい位置に配置する

**Non-Goals:**
- 案件データを Hugo の data ファイル(YAML/JSON)化して汎用テンプレートで描画する仕組みは作らない(対象2件のみのため、Markdown 直書きで十分)
- Playground ページの内容・構成変更は行わない
- Contact フォームの事前ヒアリング、ブログのカテゴリ分離は行わない(スコープ外)
- about.md の「実績・関わってきた領域」箇条書きの扱い(残す/リンクする/統合する)の最終判断は tasks 側で軽微な調整に留め、大規模な書き直しはしない

## Decisions

- **URL / ファイル**: `content/achievements.md` を新規作成し、`url: "/achievements/"` とする。about.md / playground.md と同じ front matter パターン(`title` / `layout: "page"` / `url`)を使う。
  - 代替案として `/services/` や `/work/` も検討したが、`/services/` は「発注できる仕事」という誤解を再び招きうる(レビュー指摘の反省点)ため避け、`/work/` より実績の意味が明確な `/achievements/` を採用。
- **メニュー配置**: `config.yml` の `menu.main` に `identifier: achievements, name: "実績", url: /achievements/, weight: 3` を追加し、About(1)と Playground(5)の間に配置する。見込みクライアントが About の次に実績を見つけられる導線にする。
- **匿名化方針**: career.yaml のコメント方針(`employer.name` は匿名化対象、`employment` は実名可)に従い、ケーススタディ本文では employer 実名を出さず業種ベースの匿名表現(例:「大手ニュース配信・データ企業」「受託開発企業経由のBtoB SaaS企業」)を用いる。`u-rei-com-improvement-notes.md` 内のたたき台(気象データ配信基盤ケーススタディ)の表現をベースに、BtoB SaaS 案件も同トーンで書き起こす。
- **ページ構成**: 案件ごとに「見出し(案件名)」→「課題」→「対応」→「成果」→「技術スタック(technologies から抜粋)」の順で記載する固定フォーマットとする。career.yaml の narrative をそのまま転記せず、対外向けに簡潔化した文章に書き直す。
- **about.md との重複整理**: about.md の「実績・関わってきた領域」箇条書きはそのまま残し、末尾に実績ページへのリンク(例: `詳しいケーススタディは [実績ページ](/achievements/) を参照`)を1行追加する程度の軽微な変更に留める。大きな書き直しは行わない。

## Risks / Trade-offs

- [匿名化した表現が抽象的すぎて説得力が下がる] → 業種・規模感(週4日稼働、5名体制など)は career.yaml から具体的に引用し、社名以外の情報量は落とさない
- [対象2件のみでは実績ページとして手薄に見える可能性] → 今回はスコープを2件に絞る合意済み。将来的に案件を追加できるよう、ページ内は案件ごとの見出し区切り(`##`)で拡張しやすい構造にする
- [about.md との実績記載が重複し情報が分散する] → about.md 側は一覧のみに留め、詳細は実績ページに一本化するリンク構成にすることで役割分担を明確にする

## Migration Plan

- 新規ファイル追加とメニュー変更のみで、既存コンテンツの削除・URL変更は発生しない。ロールバックは該当ファイル・menu エントリの削除で完結する。
