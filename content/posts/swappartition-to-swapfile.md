---
title: "スワップパーティションからスワップファイルへ移行"
date: 2023-08-15T15:44:31+09:00
draft: false
---

Ubuntuでスワップパーティションからスワップファイルへ移行する試み.

<!--more-->

## 背景

普段使いPCで運用しているUbuntu 22.04で, メモリ 8GB, スワップパーティション 8GB.

ブラウザを使っていると当たり前のようにスワップ含むメモリ使用量が8GBを超えるため,
ハイバネートに失敗してしまう. そのため, パソコンを閉じるときにわざわざブラウザ等を閉じるようにしていたが, いい加減めんどうになってきたので, スワップ領域を増やすことにしてみた.


## 対応内容

1. スワップファイルを作成する
1. `/etc/fstab` を編集して, スワップファイルをスワップ領域としてマウントする
1. `grub` 設定を変更して, スワップファイルにサスペンドイメージを保存するようにする
1. 再起動する

やることとしてはこんな感じ. 

注意点として, スワップ領域を増やすだけなら,
スワップファイルを追加してマウントしてやるだけでいいが,
サスペンドイメージは一つのパーティション,
またはスワップファイルに保存する形にしないとだめ [^wiki1]. そのため, 既存のパーティションに代えて大きめに指定するスワップファイルを使うことにする.

[^wiki1]: https://wiki.archlinux.jp/index.php/%E9%9B%BB%E6%BA%90%E7%AE%A1%E7%90%86/%E3%82%B5%E3%82%B9%E3%83%9A%E3%83%B3%E3%83%89%E3%81%A8%E3%83%8F%E3%82%A4%E3%83%90%E3%83%8D%E3%83%BC%E3%83%88


### スワップファイルを作成する

ddコマンドでスワップファイルを作成する. 実メモリの倍の16GBにしています.

```sh
sudo dd \
    if=/dev/zero of=/swapfile \
    bs=(cat /proc/meminfo | awk '/MemTotal/ {print $2}') \
    count=2048 \
    conv=notrunc
```

スワップファイルとしてファイルをフォーマット.

```sh
sudo mkswap /swapfile
```

### /etc/fstab を編集する

/etc/fstab にある次のエントリ.

```plaintext
UUID=c9e7ba59-90a6-4f71-8863-814d166064fa none swap sw 0 0
```

これを削除するかコメントアウトするなどして, 次のエントリに差し替える.

```plaintext
/swapfile none swap defaults 0 0
```

これで再起動すると, スワップ領域にパーティションではなく, /swapfile
が使われるようになる.

### grub設定を変更する

Ubuntuのgrub設定ファイルは `/etc/default/grub`.

サスペンドイメージの保存先をカーネルオプションで指定するようになっている.

既存の指定.

```plaintext
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash resume=UUID=c9e7ba59-90a6-4f71-8863-814d166064fa"
```

これを, 次のように編集する.

```plaintext
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash resume=UUID=208cb226-9265-43ed-b3a0-b6aa588e9e27 resume_offset=8992768"
```

`resume=UUID=` と `resume_offset=` この2つの指定を書き換える.

`resume=UUID=` これはスワップファイルを置いたボリュームのUUID. スワップファイルは `/` に置いたので, `/etc/fstab` の `/` にマウントされているボリュームのUUIDがそれ.

`resume_offset=` これはスワップファイルがボリューム上の物理的に配置されている場所のこと. これを `filefrag` コマンドで確認することができる.

```sh
$ sudo filefrag -v /swapfile
Filesystem type is: ef53
File size of /swapfile is 16414375936 (4007416 blocks of 4096 bytes)
 ext:     logical_offset:        physical_offset: length:   expected: flags:
   0:        0..    2047:    8992768..   8994815:   2048:
   1:     2048..    4095:   10039296..  10041343:   2048:    8994816:
省略
```

`physical_offset` の先頭の値がそれ. つまり `8992768` です.

`/etc/default/grub` を編集し終えたら, `/boot` 以下にあるgrub.cfgを更新してやる必要がある. Ubuntuの場合は次のコマンドを実行する [^memo1].

[^memo1]: Linuxディストリビューションによって異なるので, Ubuntu以外なら個別に確認が必要

```plaintext
$ sudo update-grub
```

### 再起動する

ここまでできたら再起動する.

## 動作確認と所感

使用メモリを8GBを大きく超える状態でハイバネートし, 復帰までできた.

いまのところパフォーマンス的な影響もさほどなさそうだった.

ハイバネートを多用する運用はあまり好きではないんだけど, 古いノートパソコンでバッテリがよわよわであることや, そんなに使わんPCなので電源を繋ぎっぱなしにもしたくない. ということで引き続きハイバネートで運用していく.

## 参考

ArchWikiに載ってる内容でほとんどわかった.

* [電源管理/サスペンドとハイバネート](https://wiki.archlinux.jp/index.php/%E9%9B%BB%E6%BA%90%E7%AE%A1%E7%90%86/%E3%82%B5%E3%82%B9%E3%83%9A%E3%83%B3%E3%83%89%E3%81%A8%E3%83%8F%E3%82%A4%E3%83%90%E3%83%8D%E3%83%BC%E3%83%88)
* [スワップ](https://wiki.archlinux.jp/index.php/%E9%9B%BB%E6%BA%90%E7%AE%A1%E7%90%86/%E3%82%B5%E3%82%B9%E3%83%9A%E3%83%B3%E3%83%89%E3%81%A8%E3%83%8F%E3%82%A4%E3%83%90%E3%83%8D%E3%83%BC%E3%83%88)
