# Project Context

## Purpose
このプロジェクトは、内田康介氏の個人ウェブサイト「U-REI.com」です。GitHub Pagesを利用してホスティングされています。

## Tech Stack
- **Static Site Generator**: Hugo
- **Theme**: PaperMod
- **Content Language**: Markdown
- **Templating**: Go (via Hugo)
- **Deployment**: GitHub Pages
- **CI/CD**: GitHub Actions
- **Containerization**: Docker

## Project Conventions

### Code Style
- **Content**: Markdownファイルは、タイトル、日付、ドラフト状態、要約などのメタデータを含むfront matterで構成されます。
- **Date Format**: `YYYY-MM-DD HH:MM:SS+TZ` (例: `2025-04-18T01:02:57+09:00`)

### Architecture Patterns
- **Directory Structure**: 標準的なHugoのプロジェクト構成に従います。
  - `content/`: Markdownコンテンツ
  - `static/`: 画像などの静的アセット
  - `config.yml`: サイト全体の設定
  - `docs/`: 生成されたサイトの出力先

### Testing Strategy
- 現在、自動化されたテストフレームワークは導入されていません。
- テストは `hugo server` コマンドでローカルサーバーを起動し、手動で表示確認を行うことを基本とします。

### Git Workflow
- **Branching**: featureブランチを作成し、Pull Requestを通じてmasterブランチにマージするワークフローを採用しています。
- **Commit Messages**: Conventional Commitsの規約に従います (例: `feat: ...`, `fix: ...`)。コミットメッセージは、件名と、必要に応じて本文で構成されます。

## Domain Context
- 内田康介氏の個人ブログとして、技術的な知見や日常の出来事などを投稿する場です。

## Important Constraints
- 静的サイトであるため、サーバーサイドでの動的な処理は行えません。すべてのコンテンツはビルド時に生成されます。

## External Dependencies
- **Hugo Theme**: `papermod` を主要な外部依存関係として利用しています。