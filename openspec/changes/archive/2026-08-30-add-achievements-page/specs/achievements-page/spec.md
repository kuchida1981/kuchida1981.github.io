## ADDED Requirements

### Requirement: 実績ケーススタディページの提供
サイトは `/achievements/` に実務実績をケーススタディ形式で紹介するページを提供しなければならない(SHALL)。ページは `content/about.md` / `content/playground.md` と同じ `layout: "page"` を用いた静的 Markdown ページとして実装しなければならない(SHALL)。

#### Scenario: 実績ページへのアクセス
- **WHEN** ユーザーが `/achievements/` にアクセスする
- **THEN** ケーススタディ形式で構成された実績ページが表示される

### Requirement: ケーススタディの構成
ページに掲載する各ケーススタディは、案件名(見出し)・課題(Challenge)・対応(Actions)・成果(Outcome)・技術スタックの5要素をこの順で含まなければならない(SHALL)。

#### Scenario: 1件のケーススタディの構成要素
- **WHEN** 実績ページ内の1つのケーススタディが表示される
- **THEN** 案件名、課題、対応、成果、使用した技術スタックの一覧がこの順で含まれる

### Requirement: 掲載対象案件
ページには以下の2件のケーススタディを掲載しなければならない(SHALL)。
- 気象データ配信基盤の新規構築・運用(career.yaml の `jx-data-distribution-service-2023` を基にした内容)
- BtoB向けクラウドサービスの新規開発・保守運用(career.yaml の `btob-web-service-2019` を基にした内容)

#### Scenario: 2件のケーススタディが掲載されている
- **WHEN** 実績ページが表示される
- **THEN** 気象データ配信基盤のケーススタディと、BtoB向けクラウドサービスのケーススタディの2件が含まれる

### Requirement: employer 実名の匿名化
ケーススタディ本文は常駐先(employer)の実名を含んではならない(SHALL NOT)。実名の代わりに業種ベースの匿名表現を用いなければならない(SHALL)。

#### Scenario: 実名が含まれていないことの確認
- **WHEN** 実績ページの本文を確認する
- **THEN** career.yaml 上で匿名化対象とされている employer 実名が一切含まれていない

### Requirement: メニューからの導線
サイトのメインメニューは既存の `About` / `Playground` / `Posts` / `Contact` に加えて `実績` エントリを含み、`/achievements/` へリンクしなければならない(SHALL)。`実績` エントリは `About` と `Playground` の間に配置しなければならない(SHALL)。

#### Scenario: メインメニューに実績エントリが表示される
- **WHEN** サイトの任意のページでメインメニューが表示される
- **THEN** `実績` というラベルのメニュー項目が表示され、`/achievements/` へのリンクになっている

#### Scenario: メニュー内の並び順
- **WHEN** メインメニューが表示される
- **THEN** `About` の次、`Playground` の前に `実績` エントリが表示される

#### Scenario: 既存メニュー項目への影響がないこと
- **WHEN** `実績` メニュー項目が追加される
- **THEN** 既存の `About` / `Playground` / `Posts` / `Contact` メニュー項目のラベル・リンク先・並び順(相対順序)は変更されない
