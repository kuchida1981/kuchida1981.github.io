---
title: "使ってますか? checkupdates on Arch Linux"
date: 2023-12-24T00:00:00+09:00
draft: false
---

Ubuntu (または apt コマンド) で更新があるパッケージをリスト表示する場合に, `apt list --upgradable` コマンドを使います.

```plaintext
vagrant@ubuntu-jammy:~$ apt list --upgradable
Listing... Done
apparmor/jammy-updates 3.0.4-2ubuntu2.3 amd64 [upgradable from: 3.0.4-2ubuntu2]
apport/jammy-updates 2.20.11-0ubuntu82.5 all [upgradable from: 2.20.11-0ubuntu82]
apt-utils/jammy-updates 2.4.11 amd64 [upgradable from: 2.4.5]
apt/jammy-updates 2.4.11 amd64 [upgradable from: 2.4.5]
...
```

Arch Linux で同等のことを行なう場合, pacman-contrib パッケージに含まれている `checkupdates` コマンドを利用できます.

```plaintext
$ checkupdates
intellij-idea-community-edition 4:2023.3.1-1 -> 4:2023.3.2-1
xmlsec 1.2.37-1 -> 1.2.39-1
```

`apt` コマンドと違って, 実行するたびにパッケージのデータベースのダウンロードが行われるため, ちょっと時間がかかります.

ダウンロード済みのデータベースを使う場合は, `--nosync` オプションを利用できます.

