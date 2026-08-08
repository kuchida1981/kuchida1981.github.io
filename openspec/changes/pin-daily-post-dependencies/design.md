## Context

`scripts/requirements.txt` は `google-genai` / `feedparser` / `python-dotenv` をバージョン指定なしで列挙しており、`daily-post.yaml` が実行されるたびに `pip install -r scripts/requirements.txt` が「その時点の最新版」を解決してインストールする。直近の成功実行（2026-08-07T23:38 UTC, run 31227758521）のログから、実際に解決されたトップレベルパッケージのバージョンは以下の通り確認できた。

```
google-genai==2.17.0
feedparser==6.0.14
python-dotenv==1.2.2
```

この change は、この「現在実際に動作しているバージョン」をそのまま `requirements.txt` に固定するだけであり、依存パッケージそのものの入れ替えやコードの変更は行わない。

## Goals / Non-Goals

**Goals:**
- `scripts/requirements.txt` のトップレベル依存を `==` で固定し、`pip install` の結果を実行のたびに再現可能にする
- 今後 Dependabot（pip エコシステム）を導入した際に、更新PRが正しく生成される状態にする

**Non-Goals:**
- `google-genai` / `feedparser` / `python-dotenv` の推移的依存（`anyio`, `httpx`, `pydantic` など）まで個別にピン留めすること（lock ファイル化は行わない。トップレベルのみを対象とする）
- `scripts/generate_daily_post.py` のコードやロジックの変更（別 change で対応）
- Dependabot 設定自体の追加（別 change で対応）
- `scripts/patch_past_posts.py`（対象パッケージへの依存がないため無関係）

## Decisions

- **トップレベルのみをピン留めし、フルの lock ファイル（`pip-compile` 等）は導入しない**
  理由: 現状の運用規模（個人ブログの日次投稿スクリプト）に対して lock ファイル管理の運用コストは見合わない。`requirements.txt` に列挙された3パッケージを `==` で固定するだけで「予期しない最新版の混入」というリスクは十分に防げる。
- **固定するバージョンは「直近の成功実行で実際に使われたバージョン」を採用する**
  理由: 新たにテストなどで検証されたわけではないバージョンを恣意的に選ぶより、すでに本番相当（GitHub Actions 上のスケジュール実行）で動作実績のあるバージョンを基準にする方がリスクが低い。

## Risks / Trade-offs

- [ピン留めしたバージョンが将来的に脆弱性報告の対象になっても自動では上がらない] → 別 change で Dependabot（pip エコシステム）を導入し、更新PRベースで追従する運用に移行する
- [トップレベル以外の推移的依存はピン留めされないため、`pip install` のたびに微妙に異なるバージョンが解決される可能性が残る] → 現状のリスク許容度（個人ブログ、致命的な被害なし）では許容範囲と判断。問題が顕在化した場合に lock ファイル化を再検討する
