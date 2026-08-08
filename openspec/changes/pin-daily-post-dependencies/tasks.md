## 1. 依存バージョンの固定

- [ ] 1.1 `scripts/requirements.txt` の `google-genai` を `google-genai==2.17.0` に固定する
- [ ] 1.2 `scripts/requirements.txt` の `feedparser` を `feedparser==6.0.14` に固定する
- [ ] 1.3 `scripts/requirements.txt` の `python-dotenv` を `python-dotenv==1.2.2` に固定する

## 2. 検証

- [ ] 2.1 ローカルまたは CI 上で `pip install -r scripts/requirements.txt` を実行し、エラーなくインストールできることを確認する
- [ ] 2.2 `.github/workflows/daily-post.yaml` を `workflow_dispatch` で手動実行し、固定バージョンで正常に投稿が生成されることを確認する
