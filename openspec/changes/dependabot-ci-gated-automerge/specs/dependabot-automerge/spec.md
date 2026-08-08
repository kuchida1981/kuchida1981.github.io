## ADDED Requirements

### Requirement: Dependabot による更新PRの生成
リポジトリは `.github/dependabot.yml` を通じて、`github-actions` エコシステム（`.github/workflows/` 配下）および `pip` エコシステム（`scripts/requirements.txt`, `scripts/requirements-dev.txt`）の依存更新を定期的にチェックし、更新PRを自動生成しなければならない（MUST）。git submodule（`themes/papermod`）および `docker` エコシステム（`Dockerfile`）は対象に含めてはならない（MUST NOT）。

#### Scenario: GitHub Actions の更新PRが生成される
- **WHEN** `.github/workflows/` 配下のワークフローで使用されている action に新しいバージョンが公開される
- **THEN** Dependabot がそのバージョンへの更新PRを作成する

#### Scenario: pip 依存の更新PRが生成される
- **WHEN** `scripts/requirements.txt` または `scripts/requirements-dev.txt` に記載されたパッケージに新しいバージョンが公開される
- **THEN** Dependabot がそのバージョンへの更新PRを作成する

#### Scenario: submodule と Dockerfile は更新PRの対象にならない
- **WHEN** `themes/papermod`（submodule）や `Dockerfile` の base image に新しいバージョンが存在する
- **THEN** Dependabot はこれらに対する更新PRを作成しない

### Requirement: 必須ステータスチェックによるマージ制御
master ブランチへのマージは、`hugo.yaml` の build ジョブおよび `scripts-tests.yaml` のテストジョブの両方が成功していない限り許可されてはならない（MUST NOT）。

#### Scenario: CIが red の場合マージがブロックされる
- **WHEN** build ジョブまたはテストジョブのいずれかが失敗している状態で PR をマージしようとする
- **THEN** GitHub はマージを拒否する

#### Scenario: CIが green の場合マージが許可される
- **WHEN** build ジョブとテストジョブの両方が成功している
- **THEN** PR は（他の必須条件を満たしていれば）マージ可能な状態になる

### Requirement: 更新種別に応じた自動マージ
Dependabot が作成した PR のうち、更新種別が patch または minor であるものは、必須ステータスチェックが green になった時点で自動的にマージされなければならない（MUST）。更新種別が major であるものは、自動マージを有効化してはならず（MUST NOT）、人間によるレビューとマージを必要としなければならない（MUST）。

#### Scenario: patch 更新が自動マージされる
- **WHEN** Dependabot が patch バージョンの更新PRを作成し、必須ステータスチェックがすべて green になる
- **THEN** PR は人手を介さず自動的にマージされる

#### Scenario: minor 更新が自動マージされる
- **WHEN** Dependabot が minor バージョンの更新PRを作成し、必須ステータスチェックがすべて green になる
- **THEN** PR は人手を介さず自動的にマージされる

#### Scenario: major 更新は自動マージされない
- **WHEN** Dependabot が major バージョンの更新PRを作成する
- **THEN** 自動マージは有効化されず、PRは人間がレビューしてマージするまでオープンのままになる

#### Scenario: CIが red のままの更新PRはマージされない
- **WHEN** Dependabot が作成した patch/minor の更新PRで、必須ステータスチェックのいずれかが失敗する
- **THEN** 自動マージは実行されず、PRはオープンのまま残る
