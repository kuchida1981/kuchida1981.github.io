---
title: "systemdサービスの失敗をデスクトップ通知する"
date: 2024-09-08T20:00:00+09:00
draft: false
tags:
- systemd
- linux
categories:
- linux
---

うちのarchlinuxマシンでは, systemdサービスの失敗をデスクトップ通知させています.

<!--more-->

systemdが動いているLinuxディストリビューション (つまりだいたいOK) なら適用できるはずです.

次のコマンドで通知用のsystemdサービスを作成します
(`--user` オプションを外せばシステムレベルに適用されることになります).

```plaintext
$ systemctl --user edit --full failure-notification@.service
```

次のファイル内容で保存します.

```systemd
[Unit]
Description = Send a notification about a failed systemd Unit
After = gnome-session.target

[Service]
Type = simple
ExecStart = notify-send -i "dialog-error" -a "systemd service failed" "%i failed" "%i"
```

これでユーザレベルのsystemdサービスの失敗がデスクトップ通知されるようになります.

こんな感じのコマンドを実行するとすぐに確認できるはずです (失敗するコマンドをsystemdで実行している).

```plaintext
$ systemd-run --user test 1 -eq 2
```

少し通知がうるさく感じてきたのでこの通知をやめることにしたのですが,
ニーズはあるかもしれないなと思ったので, 書き残しておきます.

`notify-send` コマンドはデスクトップ通知用のコマンドですが,
ここを調整して通知先を変えるのも有用じゃないかなと思います.
