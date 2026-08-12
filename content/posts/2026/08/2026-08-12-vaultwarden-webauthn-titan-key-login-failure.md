---
title: "Titanセキュリティキーが登録はできるのにログインだけ失敗する: VaultwardenのWebAuthn 2FAで踏んだ罠"
date: 2026-08-12T21:00:00+09:00
draft: true
tags: ["Vaultwarden", "WebAuthn", "FIDO2", "Self-hosted", "Security", "Debugging"]
categories: ["Tech", "Service"]
author: "Kosuke Uchida"
showtoc: true
tocopen: true
---

セルフホストの[Vaultwarden](https://github.com/dani-garcia/vaultwarden)にGoogle Titanセキュリティキーを2段階認証(FIDO2 WebAuthn)として登録したら、登録自体は一発で成功するのに、その後のログインが必ず失敗する、という不可解な症状にはまった。同じ物理キーはGoogleやwebauthn.ioでは何の問題もなく使える。原因を突き止めるのに数週間かかったので、記録として残しておく。

# 症状

- Titanキーを2FAとして登録すると成功する(タッチ要求 → 登録完了、というふつうの流れ)
- ログイン時、ブラウザの「セキュリティキーを挿入してタッチしてください」ダイアログが出たまま反応がなく、最終的に`NotAllowedError: The operation either timed out or was not allowed`でタイムアウトする
- 同じ現象がLinux(Chrome)、Mac mini(Chrome/Firefox)、スマートフォンでも再現。OSやマシンには依存しない
- 同じキーをGoogleアカウントやwebauthn.ioに登録すると問題なく動く。キー自体は壊れていない

# 除外していった仮説

原因を絞り込むまでに、以下をひとつずつ潰していった。

- **RP ID/ドメインの不一致** — ブラウザのネイティブダイアログには正しいドメインが表示されている
- **ブラウザ拡張機能・広告ブロッカーの干渉** — 無効化しても変化なし
- **`webauthn-connector.html`の`Permissions-Policy`ヘッダーに`publickey-credentials-get`が含まれていない** — Caddy側でヘッダーを上書きするテストを本番で実施したが変化なし
- **サーバー側での認証情報の保存/シリアライズ不具合** — DBに保存された`cred_id`はログイン時にそのままバイト単位で一致しており、サーバー側で壊れている様子はない
- **U2F互換用の`appid`拡張を無条件に送っていることが原因では?** — 移行済み(`migrated: true`)のクレデンシャルにだけ`appid`を送るようパッチしたVaultwardenをビルドして本番にデプロイし、Chromeの内部FIDO/CTAPログ(`--vmodule="*fido*=3,*webauthn*=3"`)で比較したが、タイムアウトまでの挙動パターンは無変化。この仮説は外れ
- **本家Bitwarden(C#実装)との差異** — `WebAuthnTokenProvider.cs`を確認したが、Vaultwardenとほぼ同じ流れ(`UserVerificationRequirement.Discouraged` + 無条件の`AppID`拡張)で組まれており、Vaultwarden固有のバグという線も薄い

# 突破口: Firefoxで登録し直すとPINを聞かれた

外堀を埋めていく中で、ふと「登録済みのキーを消して、Firefoxで登録し直してみたらどうなるか」を試した。すると、Chromeでは一度も出なかった**セキュリティキーのPIN入力を、Firefoxは要求してきた**。

このFirefoxで登録し直したクレデンシャルでログインすると、Chrome・Firefoxどちらからでも成功する。念のため2回繰り返して確認した。

- Chromeで再登録 → 失敗(何度やっても同じ)
- Firefoxで再登録 → 成功(Chrome/Firefoxどちらのログインも通る)

「登録時にPINによるユーザー検証(UV)が実際に行われたかどうか」が明暗を分けているのは間違いなさそうだった。

# DBレコードを直接比較する

同じ物理キーを、登録に使うブラウザだけ変えて2回登録し、Vaultwardenの`twofactor`テーブル(SQLite)に保存されるレコードを直接比較した。

| | Chromeで登録(PINなし) | Firefoxで登録(PINあり) |
|---|---|---|
| `user_verified` | `false` | `true` |
| `counter`(ログイン後) | `0`(一度も成功していない) | ログインのたびに増分 |
| クレデンシャルIDの長さ | 160 bytes | 288 bytes |

`registration_policy`はどちらも`discouraged`のまま変わらないが、実際にUVが行われたかどうかでクレデンシャルIDの長さそのものが変わっている。Titanキーは、UVなしで作られた短い方のクレデンシャルではログインの`GetAssertion`を完走できない、という個体差(あるいは仕様)を持っているらしい。

# 原因: 登録時に`Discouraged`が強制されている

Vaultwardenのソース(`src/api/core/two_factor/webauthn.rs`)を追うと、2FA登録のチャレンジを生成する`generate_webauthn_challenge`関数で、ユーザー検証ポリシーが明示的に`Discouraged`へ固定されていた。

```rust
if let Some(asc) = challenge.public_key.authenticator_selection.as_mut() {
    asc.user_verification = UserVerificationPolicy::Discouraged_DO_NOT_USE;
}
```

(`webauthn-rs`クレート自身がこの値を`Discouraged_DO_NOT_USE`という名前にしている……そのままの命名で笑った)

Chromeはこの指定を素直に受け取り、PINプロンプトなしで登録を完了させる。一方Firefoxは`discouraged`のヒントを無視して(?)PINを要求してくる。この実装差が、今回の症状の入口だったことになる。

# 応急処置として実際にやったこと

恒久的なコード修正を待たず、実運用としてはシンプルに解決できた。

1. Vaultwardenの設定から、Titanキーの2FA登録を削除
2. **Firefoxで**同じキーを2FAとして再登録(PIN入力あり)
3. ログアウトし、Chrome・Firefoxどちらからもログインできることを確認

これだけで、コード変更もサーバー再構築も不要だった。同じ問題に当たった人は、まずこれを試してみてほしい。

# 恒久対応はどうなっているか

「サーバー側で`Discouraged`を`Preferred`に変えればいいのでは」という仮説はコードレベルでは正しそうだが、これは本家Vaultwardenの挙動を変える話なので、独断でパッチを当てて終わりにはできない。

まず[GitHub Discussions](https://github.com/dani-garcia/vaultwarden/discussions/7556)に経緯をまとめて投稿したが、1週間ほど反応がなかった。READMEに載っているMatrix chatで一声かけたところ、実は自分が投稿する前から関連する議論が進んでいたことが分かった。

- [Issue #7437](https://github.com/dani-garcia/vaultwarden/issues/7437): Swissbit iShield Key 2 Proという別の認証器でも、似た(ただし発生条件は少し異なる)問題が報告されていた
- [PR #7500](https://github.com/dani-garcia/vaultwarden/pull/7500): そのIssueを受けて、`WEBAUTHN_2FA_USER_VERIFICATION`という設定でopt-inに`preferred`へ切り替えられるようにするPRがすでに出ていた
- ただしメンテナーから「本家Bitwardenにはこのオプション自体が存在せず、公式クライアントへの影響が予測できないので反対」というコメントがついており、まだマージには至っていない

自分でもフォーク上でパッチを試作していた(登録・ログイン両方を無条件に`Preferred`へ変更するだけの、設定なしのバージョン)が、比較してみるとPR #7500の「デフォルトは`discouraged`のまま、必要な人だけopt-inする」という設計のほうが、メンテナーの懸念に対して筋が良いと感じた。Issue #7437には自分のTitanキーのケース(単一クレデンシャルの初回登録でも再現する、という点でiShieldのケースより単純)を追加情報としてコメントしておいた。

現時点(2026年8月)ではまだ議論が続いている状態で、この記事を公開した後の展開も含めて動きがあれば追記したい。

# 本家Bitwardenでも再現するか

Vaultwardenは本家Bitwardenのサーバー実装を参考に作られているので、「そもそも本家でも同じことが起きるのでは?」という疑問が当然出てくる。手元にBitwardenサーバー(C#)のリポジトリをチェックアウトしてあったので、該当箇所を確認してみた。

2FAとしてのWebAuthn登録は`StartTwoFactorWebAuthnRegistrationCommand.cs`で組まれていて、

```csharp
var authenticatorSelection = new AuthenticatorSelection
{
    AuthenticatorAttachment = null,
    RequireResidentKey = false,
    UserVerification = UserVerificationRequirement.Discouraged
};
```

ログイン(assertion)側も`WebAuthnTokenProvider.cs`で同じく`UserVerificationRequirement.Discouraged`。Vaultwardenとほぼ同じ設計で、しかも本家には**設定でオーバーライドする手段が一切ない**。`excludeCredentials`(既存キーの除外リスト)を積む構造も同じなので、Issue #7437のiShieldのケース(複数キー登録時に発生)・自分のTitanキーのケース(単体登録でも発生)、どちらのパターンも本家Bitwardenサーバーで再現しうるコード構造になっている。

一方で興味深いのは、Bitwardenには**パスキー(パスワードレス)ログイン機能**があり(Vaultwardenにはまだ実装されていない)、そちらは`GetWebAuthnLoginCredentialCreateOptionsCommand.cs`/`GetWebAuthnLoginCredentialAssertionOptionsCommand.cs`で`UserVerificationRequirement.Required`を使っている。同じコードベースの中でも「2FA用WebAuthn」と「パスキーログイン用WebAuthn」でポリシーが違い、後者ならこの問題は起きないはずだ。つまり今回の症状は、あくまで**2FAとしてWebAuthnを使う場合に限定される**、という理解になる。

実際に本家Bitwardenで確認しようとも思ったが、無料プランではTOTP以外の2FA手段(WebAuthnを含む)が使えず、セルフホスティングして試すのも手間が大きいので、今回はコードの突き合わせだけに留めている。あくまで**未検証の推測**として書いておく。

# まとめ

- Vaultwarden(および、コードを見る限り本家Bitwardenも)は、WebAuthn 2FAの登録時にユーザー検証を`Discouraged`で要求している
- ブラウザによってこの指定への従い方が異なり(Chromeは素直にPINをスキップ、Firefoxは要求してくる)、その結果できあがるクレデンシャルの「強度」が変わる
- 一部の認証器(少なくともGoogle Titanキー、Swissbit iShield Key 2 Pro)は、UVなしで作られたクレデンシャルでは後のログインを完走できない
- 応急処置は「Firefoxなど、PINを要求してくるブラウザで登録し直す」だけで済む
- 恒久的な修正(サーバー側の設定でopt-in的に`Preferred`を選べるようにする)はコミュニティで議論中で、まだ着地していない
- 本家Bitwardenのコードも同じ`Discouraged`固定・オーバーライド不可という構造なので、条件が揃えば同じ症状が起きる可能性が高いと考えているが、実機での確認はできていない

似たような「セキュリティキーは登録できるのに認証だけ失敗する」現象に当たった人がいたら、まずは登録に使うブラウザを変えてPINが要求されるか試してみるとよいと思う。
