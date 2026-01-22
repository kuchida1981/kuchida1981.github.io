## 1. Implementation (実装)
- [x] 1.1 Create `scripts/requirements.txt` with `google-generativeai` and `feedparser`.
    - `google-generativeai` と `feedparser` を含む `scripts/requirements.txt` を作成する。
- [x] 1.2 Create `scripts/generate_daily_post.py` to fetch RSS, select topic, and generate Markdown.
    - RSSを取得し、トピックを選択し、Markdownを生成する `scripts/generate_daily_post.py` を作成する。
- [x] 1.3 Create `.github/workflows/daily-post.yaml` to schedule the job and create PR.
    - ジョブをスケジュール実行し、PRを作成する `.github/workflows/daily-post.yaml` を作成する。
- [x] 1.4 Add documentation in `README.md` or `GEMINI.md` about the `GEMINI_API_KEY` requirement.
    - `GEMINI_API_KEY` が必要である旨のドキュメントを `README.md` または `GEMINI.md` に追加する。
