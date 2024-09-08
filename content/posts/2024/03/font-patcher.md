---
title: "フォント合成は怖くない (nerdfont)"
date: 2024-03-26T12:00:00+09:00
draft: false
tags:
- プログラミングフォント
- Nerd Font
- HackGen
categories:
- software
---

Macのターミナル (Alacritty) でフォント HackGen を指定すると, ちゃんと表示されず豆腐になっちゃう文字 (Nerd Font) がありました.

GithubのReleasesにあるファイルから入れたり, homebrew でインストールしたもので試したりなど, いろいろやってみたのですが解決せず,
HackGen以外のてきとうなフォントにしてお茶を濁していたのですが…….

ふと思い至って自分でフォント合成することを試してみました.

```shell
# てきとうな作業用ディレクトリ
cd ~/work/path/to

# GitHubで取得してきたHackGenフォントのNerdFontではないほうを展開
unzip ~/Downloads/HackGen_v2.9.0.zip

# 出力先ディレクトリを作っておく
mkdir out

# フォント合成をcompleteオプションつきで実行
docker run --rm -v$PWD:/in:Z -v$PWD/out:/out:Z nerdfonts/patcher --complete
```

これでoutディレクトリに合成済みフォントが出力されます.

```shell
$ ll
total 200336
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGen35ConsoleNerdFont-Bold.ttf
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGen35ConsoleNerdFont-Regular.ttf
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGen35NerdFont-Bold.ttf
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGen35NerdFont-Regular.ttf
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGenConsoleNerdFont-Bold.ttf
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGenConsoleNerdFont-Regular.ttf
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGenNerdFont-Bold.ttf
-rw-r--r--  1 kosuke  staff    12M Mar 26 11:22 HackGenNerdFont-Regular.ttf
```

出力されたフォントをインストールし, Alacrittyに設定して解決しました.

フォント合成けっこう面倒かなと思って及び腰になっていたのですが,
提供されているDockerイメージだと予備知識もほとんど不要で簡単だったという話でした.

## 参考

* https://github.com/ryanoasis/nerd-fonts
* https://github.com/yuru7/HackGen
