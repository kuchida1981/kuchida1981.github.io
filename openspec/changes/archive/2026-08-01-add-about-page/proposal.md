## Why

フリーランスエンジニアとして業務委託の案件がエージェント経由で回ってくるため、営業的な訴求は不要だが、サイト訪問者（主にエージェントや案件関係者）に経歴・得意技術・実績を簡潔に伝えるページがサイト内に存在しない。トップページは PaperMod の profileMode によるミニマルな表示のみで、`/services/` は個人のセルフホスティング実験の紹介であり、自己紹介の役割を代替できない。

## What Changes

- `content/about.md` を新規追加し、`/about/` として公開する（`layout: page`、`content/services.md` と同じパターン）
- ページ構成は以下の骨組みとし、実際の記述は後日ユーザーが埋める前提でプレースホルダー相当の例文を入れる：
  - タイトル・肩書き
  - 経歴（一段落の文章）
  - 得意技術スタック（箇条書き）
  - 実績・関わってきた領域（箇条書き）
- `config.yml` の `menu.main` に `About` エントリを追加し、`Services` / `Posts` と並べて表示する
- 連絡導線（メール・SNS・フォーム等）は今回のスコープ外
- トップページの `profileMode.subtitle` および `content/services.md` は変更しない

## Capabilities

### New Capabilities
- `about-page`: フリーランスエンジニアとしての自己紹介ページ（経歴・技術スタック・実績の骨組み）とメニュー導線を提供する

### Modified Capabilities
(なし)

## Impact

- 影響ファイル: `content/about.md`（新規）、`config.yml`（menu 追加のみ）
- 既存ページ（トップページ、`/services/`、`/posts/`）への変更なし
- Hugo のビルド・デプロイフローへの影響なし（静的ページ追加のみ）
