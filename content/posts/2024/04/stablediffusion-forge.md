---
title: "Stable Diffusion WebUI forge 試してみた"
date: 2024-04-21T09:00:00+09:00
draft: false
tags:
- Stable Diffusion WebUI
---

いまさら感あるが, Stable Diffusion WebUI forge を試してみた.
しょぼいグラボでも高解像度の画像を出力できるというのと, 高速化を実現できているという.

<!--more-->

[stable-diffusion-webui-forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)

グラボはGTX1660SUPER. VRAM容量は6GBで, Stable Diffusionで遊ぶのに十分とはいえない性能.
少しチューニングしないとVRAMの割当てでクラッシュしてしまう.

forge版はVRAM 6GBくらいだと60%から70%のスピードアップを期待できるのだという.

実際に動かしてみて, AUTOMATIC1111版とforge版の処理時間を比較してみると, 確かに期待以上の効果がありそうだった.

## AUTOMATIC1111 版の場合

AUTOMATIC1111 版を動かすために, 次のようなオプションと環境変数を指定して使っている.

```plaintext
webui_args=( \
  "--precision" \
  "full" \
  "--no-half" \
  "--lowvram" \
  "--opt-split-attention" \
)

export COMMANDLINE_ARGS="${webui_args[@]}"
export LAUNCH_SCRIPT="launch.py"
export PYTORCH_CUDA_ALLOC_CONF="garbage_collection_threshold:0.6, max_split_size_mb:128"
```

適当な画像を1枚出力してみたときの実行時間がこれ.

```
Time taken: 1 min. 41.4 sec.
```

おおよそ102秒.

## forge版

README読むと, しょぼい環境のためのオプション指定は非推奨で, 手を加えずに実行することを勧められている.

容量が大きいモデルのデータ等は共有させたいので多少は手を加えているが,
前述のAUTOMATIC1111版と同じ条件で実行してみた結果がこれ.

```
Time taken: 49.1 sec.
```

50秒.

50%の性能向上. 75%もスピードアップしていないが, 十分であるとは思う.

## 比較はしないけど, 性能向上はかなり感じる

AUTOMATIC1111だと, バッチサイズを増やしたり, スケーラーを指定したときなどに,
VRAM割り当てでクラッシュしてしまうことが多々あった.

Forge版で試してみると, AUTOMATIC1111版ではクラッシュしていた程度の指定なら,
実行完了させられることがけっこうあった.

この点でも, 低スペマシンで遊ぶならなかなか有力な選択肢であるなと思った.

そのあたりまで比較すると, より性能向上の度合いがわかるかもしれまい.


## ちなみに

ぼくはsystemdのServiceユニットでStable Diffusionを起動できるようにしていて,
AUTOMATIC1111版とForge版をサフィックスの指定でどちらを起動するか指定できるようにしてみた.

```plaintext
$ systemctl --user start stable-diffusion@forge.service
```

```plaintext
$ systemctl --user cat stable-diffusion@.service
# /home/kosuke/.config/systemd/user/stable-diffusion@.service
[Unit]
Description=Stable Diffusion on local

[Service]
WorkingDirectory=%h/Documents/Projects/stable-diffusion-on-local
ExecStart=bash kind/%i/start-webui.sh
StandardOutput=journal
```

Stable Diffusionで画像を生成している最中に, GNOMEがロック画面を経てディスプレイがオフになったとき,
そこから復帰しようとするとGNOME Shell がクラッシュしてしまうことが多い.
しょうがないような気もするので, Stable Diffusionで遊ぶときはロック画面への移行やディスプレイをオフにする設定を止めたり,
GDMも止めておいて別のマシンからアクセスして使うなどして割り切っている.

本当はもっとつよつよなグラボにしたいけど, いまの円安傾向ではちょっと厳しい.
