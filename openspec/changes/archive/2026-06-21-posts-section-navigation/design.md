## Context

現在のサイトはグローバルメニューに Services / Posts / Archives の3項目を持つ。Archives は PaperMod 組み込みの `archives.html` テンプレートを使った年月別一覧ページ。Hugo のタクソノミーページ（`/categories/`, `/tags/`）やセクションページ（`/posts/YYYY/MM/`）はビルド時に自動生成されているが、サイト内からの導線がない。

Posts セクションのテンプレートは PaperMod テーマの `_default/list.html` と `_default/single.html` がそのまま使われている。プロジェクト側の `layouts/` には Posts 用のオーバーライドは存在しない。

## Goals / Non-Goals

**Goals:**
- Archives ページとグローバルメニュー項目を廃止する
- Posts セクションの全ページ（list / single）の下部に、カテゴリ・タグ・年月へのナビゲーションブロックを表示する
- ナビゲーションは控えめな存在感で、記事コンテンツの補助的な導線として機能する

**Non-Goals:**
- タクソノミーページ（`/categories/`, `/tags/`）やセクションページ（`/posts/YYYY/MM/`）自体のデザイン変更
- PaperMod テーマファイルの直接編集
- JavaScript を使った動的な切り替えUI（タブ、フィルタ等）
- Archives ページのURLリダイレクト設定

## Decisions

### 1. ナビゲーションを partial に切り出す

`layouts/partials/posts_nav.html` にナビゲーションブロックのロジックを集約し、list.html と single.html の両方から `{{ partial "posts_nav.html" . }}` で呼び出す。

**理由:** 1箇所で管理でき、list/single 間の表示差異が生じない。

### 2. テンプレートオーバーライドのスコープ

`layouts/posts/list.html` と `layouts/posts/single.html` を作成する。Hugo のテンプレートルックアップ順により、`posts` セクション配下のページにだけ適用され、Services 等には影響しない。

**代替案:** `_default/list.html` をオーバーライドする方法もあるが、全セクションに影響するため不採用。

### 3. タグの表示件数制限

タグは現在約100種あり、全件表示すると冗長になる。件数上位15件を表示し、「すべてのタグ →」リンクで `/tags/` に誘導する。

Hugo テンプレートでは `site.Taxonomies.tags` を件数順にソートし、`first 15` で切り出す。

**理由:** 利用頻度の高いタグだけを見せることで、ナビゲーションの実用性と簡潔さを両立する。

### 4. 年月アーカイブのリンク先

年月リンクは Hugo のセクションページ `/posts/YYYY/MM/` にリンクする。既存のディレクトリ構造（`content/posts/2026/01/` 等）により、セクションページは自動生成済み。

**代替案:** 年月ごとにタクソノミーを定義する方法もあるが、既存のディレクトリ構造をそのまま活かせるのでセクションページを採用。

### 5. ナビゲーションの配置位置

- **list.html**: ページネーションの下
- **single.html**: `post-footer`（タグ一覧・前後リンク）の下、comments の前

### 6. PaperMod テンプレートのベースコピー方針

`layouts/posts/list.html` と `layouts/posts/single.html` は PaperMod の対応テンプレートをコピーし、ナビ partial の呼び出しを追加する。テーマのアップデート時にはこれらのオーバーライドファイルの同期が必要になる。

## Risks / Trade-offs

- **テーマ更新時の追従コスト** → PaperMod の `_default/list.html` / `_default/single.html` が更新された場合、プロジェクト側のオーバーライドファイルとの差分確認が必要。ナビ partial の呼び出し1行だけの追加なので、差分は最小限に抑えられる。
- **`/archives/` URL の断絶** → 既存の `/archives/` URLにアクセスした場合、404 になる。外部からのリンクや検索エンジンのインデックスが残っている可能性があるが、個人ブログのため影響は軽微と判断。
