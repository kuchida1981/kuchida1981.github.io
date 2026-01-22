# Change: Add Daily Automated Blog Post (毎日記事自動投稿の追加)

## Why
To maintain an active blog presence and leverage AI for content creation, we want to automate the drafting of daily blog posts. This system will reduce the friction of starting a new post while keeping a human in the loop for quality control.

ブログの更新頻度を維持し、AIをコンテンツ作成に活用するため、毎日のブログ記事の下書き作成を自動化したいと考えています。このシステムにより、記事を書き始めるハードルを下げつつ、最終的な品質管理は人間が行う形を維持します。

## What Changes
- Add a Python script to generate blog posts using Google's Gemini API.
- Create a GitHub Actions workflow (`.github/workflows/daily-post.yaml`) that runs daily.
- The workflow will:
    1.  Execute the script to generate a post about a recent news topic.
    2.  Create a Pull Request with the new content for user review.

変更点:
- Google Gemini APIを使用してブログ記事を生成するPythonスクリプトを追加します。
- 毎日実行されるGitHub Actionsワークフロー (`.github/workflows/daily-post.yaml`) を作成します。
- ワークフローの動作:
    1.  スクリプトを実行し、最近のニュース・トピックに関する記事を生成します。
    2.  ユーザーレビュー用に、新しいコンテンツを含むPull Requestを作成します。

## Impact
- **Affected specs**: `blog`
- **Affected code**:
    - New script: `scripts/generate_daily_post.py`
    - New workflow: `.github/workflows/daily-post.yaml`
    - New dependency management (e.g., `requirements.txt` for the script)

影響範囲:
- **影響を受ける仕様**: `blog`
- **影響を受けるコード**:
    - 新規スクリプト: `scripts/generate_daily_post.py`
    - 新規ワークフロー: `.github/workflows/daily-post.yaml`
    - 新規依存関係管理 (例: スクリプト用の `requirements.txt`)