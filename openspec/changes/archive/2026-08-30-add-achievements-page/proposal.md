## Why

経営顧問レビュー(`u-rei-com-improvement-notes.md`)により、現在のサイトには「発注判断の材料」が一つも提供されていないことが指摘された。career.yaml には単価交渉の武器になる実務実績(気象データ配信基盤の新規構築・運用、BtoB向けクラウドサービスの技術選定〜保守運用まで一貫リード)が言語化済みだが、サイト側には反映されていない。現在の Playground ページには趣味プロジェクトしか掲載されておらず、見込みクライアントが「個人の実験場」としか認識できない状態になっている。

## What Changes

- 実務実績を「ケーススタディ」として掲載する新規ページを追加する(Playground ページとは別ページ)
- 対象案件は以下の2件(career.yaml の narrative を基に、業種ベースの匿名表現へ変換)
  - 気象データ配信基盤の新規構築・運用(id: `jx-data-distribution-service-2023`)
  - BtoB向けクラウドサービスの新規開発・保守運用(id: `btob-web-service-2019`)
  - career.yaml のコメント方針上、匿名化対象とされている employer 実名は NDA未確認のため出さず、業種ベースの匿名表現(例:「大手ニュース配信・データ企業」)にとどめる
- 各ケーススタディは「課題(Challenge)」「対応(Actions)」「成果(Outcome)」の3構成で記載する
- config.yml の main menu に新規ページへの導線を追加する

## Capabilities

### New Capabilities
- `achievements-page`: 実務実績をケーススタディ形式で紹介する新規ページ。ページの構成・掲載内容・匿名化ルール・ナビゲーション導線を定義する

### Modified Capabilities
(なし)

## Impact

- 追加: `content/achievements.md`(新規ページ、URLは design.md で確定)
- 変更: `config.yml`(main menu にエントリ追加)
- 影響なし: `content/playground.md`(内容変更なし)、Contact フォーム、ブログのカテゴリ構成(いずれも今回のスコープ外)
