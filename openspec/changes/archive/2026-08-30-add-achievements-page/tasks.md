## 1. ケーススタディ本文の作成

- [x] 1.1 `resume2/data/career.yaml` の `jx-data-distribution-service-2023`(気象データ配信基盤)の narrative を基に、employer 実名を含まない匿名表現(業種ベース)でケーススタディ本文(課題・対応・成果)を書き起こす。`u-rei-com-improvement-notes.md` 内のたたき台をベースにしてよい
- [x] 1.2 `resume2/data/career.yaml` の `btob-web-service-2019`(BtoB向けクラウドサービス)の narrative を基に、同様に匿名表現でケーススタディ本文(課題・対応・成果)を書き起こす

## 2. 実績ページの追加

- [x] 2.1 `content/achievements.md` を新規作成する。front matter は `title: "実績"` / `layout: "page"` / `url: "/achievements/"` とし、`content/about.md` / `content/playground.md` と同じパターンに揃える
- [x] 2.2 ページ本文に、1.1・1.2 で作成した2件のケーススタディを「案件名(見出し)→課題→対応→成果→技術スタック」の順で記載する
- [x] 2.3 `hugo` または `docker compose up` でローカルビルドし、`/achievements/` が正しく表示されることを確認する

## 3. ナビゲーション導線の追加

- [x] 3.1 `config.yml` の `menu.main` に `identifier: achievements, name: "実績", url: /achievements/, weight: 3` を追加する(About の weight 1 と Playground の weight 5 の間)
- [x] 3.2 ローカルビルドでメインメニューに `About → 実績 → Playground → Posts → Contact` の順で表示されることを確認する

## 4. about.md との整合

- [x] 4.1 `content/about.md` の「実績・関わってきた領域」セクション末尾に、実績ページ(`/achievements/`)へのリンクを1行追加する(既存の箇条書きや他セクションは変更しない)

## 5. 最終確認

- [x] 5.1 実績ページ本文に career.yaml 上で匿名化対象とされている employer 実名が含まれていないことを確認する
- [x] 5.2 `git diff` で変更ファイルが `content/achievements.md`(新規)・`config.yml`・`content/about.md` のみであることを確認する
