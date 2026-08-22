## ADDED Requirements

### Requirement: Publish Date Correction on Merge
新規に追加された記事ファイルの `date:` フロントマターが現在時刻以下（過去または現在）である場合、システムは公開が確定した時刻（`+09:00` JST表記）に自動的に書き換える。既存の過去記事の `date:` は対象としない。

#### Scenario: AI生成記事のマージ確定時に日時を補正する
- **WHEN** `automerge.yaml` がAI生成記事のPRを24時間経過後にマージしようとする
- **AND** そのPR内の記事ファイルの `date:` が現在時刻以下である
- **THEN** マージ前にPRブランチ上で `date:` をマージ確定時刻（`+09:00`表記）に書き換えてcommitする
- **AND** その後PRをマージする

#### Scenario: 手動記事はマージ前にPRブランチ上で日時を補正する
- **WHEN** 人間が作成した手動記事のPR（`automerge-24h` ラベルが付いていない）が `opened` または `synchronize` される
- **AND** そのPRで新規に追加された記事ファイルの `date:` が現在時刻以下である
- **THEN** 当該PRブランチ上で `date:` を現在時刻（`+09:00`表記）に書き換えてcommit & pushする
- **AND** 人間が後からそのPRをGitHub UIまたは `gh pr merge` でマージした際には、既に補正済みの日時のままmasterに反映される

#### Scenario: 既存の過去記事は補正対象にならない
- **WHEN** いずれかの日時補正ワークフローが実行される
- **THEN** 当該PR・pushで新規に追加されたファイル以外の既存記事の `date:` は一切変更されない

#### Scenario: masterへの直接pushによる補正は行わない
- **WHEN** 日時補正ロジックが動作する
- **THEN** 補正commitは常にPRのブランチに対して行われ、`master` ブランチへの直接pushは一切行われない（`master` はbranch protectionにより直接pushを受け付けないため）

### Requirement: Future-Dated Posts Are Preserved As Reservations
記事ファイルの `date:` が現在時刻より未来である場合、システムはその日時を書き換えず、予約投稿として扱う。

#### Scenario: 未来日付のAI生成記事はマージ時に書き換えられない
- **WHEN** `automerge.yaml` がPRをマージしようとする
- **AND** 対象記事ファイルの `date:` が現在時刻より未来である
- **THEN** `date:` は変更されずにマージされる

#### Scenario: 未来日付の手動記事はPRブランチ上でも書き換えられない
- **WHEN** 人間が未来日付を指定した手動記事のPRを作成・更新する
- **THEN** 日時補正ワークフローは当該ファイルの `date:` を変更しない

### Requirement: Scheduled Publish Polling
システムは、未来日付が指定された記事の公開予定時刻が到来したことを15分間隔でポーリング検知し、検知した場合はデプロイを起動する。

#### Scenario: 予約時刻到来時にデプロイが起動する
- **WHEN** `publish-checker.yaml` が15分毎に実行される
- **AND** `content/posts/**` 内の記事に、直近のルックバック窓内で `date:` が現在時刻を過ぎたものが存在する
- **THEN** `hugo.yaml` を `workflow_dispatch` で起爆する

#### Scenario: 該当記事が無ければデプロイは起動しない
- **WHEN** `publish-checker.yaml` が実行される
- **AND** ルックバック窓内で公開時刻が到来した記事が存在しない
- **THEN** `hugo.yaml` は起爆されない

### Requirement: Immediate Deploy After Bot Merge
AI生成記事のPRがマージされた直後、6時間毎のスケジュール実行を待たずにデプロイが起動する。

#### Scenario: automergeのマージ直後にデプロイが起動する
- **WHEN** `automerge.yaml` がAI生成記事のPRを正常にマージする
- **THEN** `automerge.yaml` は `hugo.yaml` を `workflow_dispatch` で明示的に起爆する

### Requirement: Deploy Workflow Documentation
デプロイフロー全体の役割分担と根本原因（`GITHUB_TOKEN` によるpushトリガー制限を含む）が、リポジトリ内のドキュメントとして参照可能である。

#### Scenario: デプロイフローのドキュメントが存在する
- **WHEN** 開発者が `.github/workflows/README.md` を参照する
- **THEN** `automerge.yaml` / `hugo.yaml` / `publish-checker.yaml` それぞれの役割、日時補正ルール、`GITHUB_TOKEN` のpushトリガー制限という根本原因の説明が記載されている
