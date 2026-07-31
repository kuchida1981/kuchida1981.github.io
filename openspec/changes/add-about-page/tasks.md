## 1. About ページの追加

- [ ] 1.1 `content/about.md` を作成する（frontmatter: `title: "About"`, `layout: "page"`, `url: "/about/"`。`content/services.md` の書式を踏襲する）
- [ ] 1.2 本文に以下のセクションをこの順で記述する（経歴は一段落の文章、その他は箇条書き。実際の記述に差し替える前提の下書きとして書く）
  - タイトル・肩書き
  - 経歴
  - 得意技術スタック
  - 実績・関わってきた領域

## 2. メニュー導線の追加

- [ ] 2.1 `config.yml` の `menu.main` に `About`（`url: /about/`）エントリを追加する。`weight` は `Services`(5) と `Posts`(10) の間（例: `7`）に設定し、既存エントリの `weight` は変更しない

## 3. 確認

- [ ] 3.1 `hugo` （または `docker compose up`）でローカルビルドし、`/about/` ページが生成されメニューに `About` が表示されることを確認する
- [ ] 3.2 既存の `/services/` ページとトップページの表示に変化がないことを確認する
