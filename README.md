# kuchida1981.github.io

blog


## デバッグ方法

次のコマンドを実行し, http://localhost:1313/ を開く.

```
hugo server -D
```

```
$ hugo server -D
Start building sites …
hugo v0.111.3+extended linux/amd64 BuildDate=unknown

                   | EN
-------------------+-----
  Pages            | 22
  Paginator pages  |  0
  Non-page files   |  0
  Static files     |  1
  Processed images |  0
  Aliases          |  6
  Sitemaps         |  1
  Cleaned          |  0

Built in 107 ms
Watching for changes in /home/kosuke/Documents/Projects/kuchida1981.github.io/{archetypes,content,static,themes}
Watching for config changes in /home/kosuke/Documents/Projects/kuchida1981.github.io/config.yml
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

## 新しく記事を書く

次のコマンドで記事を作成.

```
hugo new posts/archlinux-checkupdates-command.md
```

書き方等はHugoのドキュメントを参照する.

## 記事や変更の公開

masterブランチにマージすると, 変更を反映するようになっている.

## Docker上でのデバッグと記事の作成

デバッグ用サーバを起動する.

```
docker compose up -d
```

記事を作成する.

```
docker compose run --rm hugo new posts/2024/03/hoge.md
```
