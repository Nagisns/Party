<div align="center">

# Party

[English](README.md) | **日本語**

discord.py で作られた Discord Bot です。
投票、サイコロ、応答速度の確認、ページ切り替え式のコマンドガイドを提供します。
スラッシュコマンドで操作でき、Discord の言語設定に合わせて日本語・英語で応答します。

![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-ECD53F?logo=dotenv&logoColor=black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

バージョン **0.4.0** · プレリリースとして開発中 · [変更履歴](CHANGELOG.md)

[できること](#できること) · [はじめかた](#はじめかた) · [使い方](#使い方) · [困ったときは](#困ったときは) · [詳しいドキュメント](#詳しいドキュメント)

## できること

| やりたいこと | コマンド | 動作 |
| --- | --- | --- |
| 使えるコマンドを知る | `/help` | コマンドと説明を一覧表示します。 |
| コマンドの使い方を調べる | `/commands` | ボタンでページを切り替えられるガイドを表示します。 |
| Bot の応答速度を確認する | `/ping` | Discord との接続の遅延をミリ秒で表示します。 |
| サイコロを振る | `/roll` | 2〜1000 面のサイコロを 1 回振ります。 |
| 投票を作成する | `/poll` | 2〜3 個の選択肢から 1 つを選ぶ投票を、1〜240 時間の受付期間で作成します。 |

Bot をサーバーに追加すると、システムチャンネルへ歓迎メッセージを送ります。
送信には、システムチャンネルの設定と Bot の送信権限が必要です。

## はじめかた

### 1. 必要なものを用意する

- **Python 3.15 以降**（[プロジェクト設定](pyproject.toml)で指定）
- **Discord Bot と Bot トークン**
- **Bot を追加できる Discord サーバー**

Bot の作成や招待がまだの場合は、[セットアップガイド](docs/ja/SETUP.ja.md)を先に進めてください。
続いて、このリポジトリをクローンまたはダウンロードし、**README があるフォルダー**でターミナルを開きます。
以下のコマンドは、すべてそのフォルダーで実行します。

### 2. 必要なパッケージをインストールする

```bash
python -m pip install "discord.py>=2.7.1" "python-dotenv>=1.2.4"
```

uv を使う場合の手順は、[セットアップガイド](docs/ja/SETUP.ja.md)を参照してください。

### 3. Bot トークンを設定する

README と同じフォルダーに `.env` ファイルを作成し、次の内容を保存します。
`your_bot_token_here` は、自分の Bot トークンに置き換えてください。

```env
TOKEN=your_bot_token_here
```

> **トークンは秘密にしてください。** `.env` を公開したり、Git にコミットしたりしないでください。
> このプロジェクトでは `.gitignore` で `.env` を除外しています。

### 4. 起動して動作を確認する

```bash
python src/bot.py
```

ターミナルに `Logged in as ...` と表示されたら、Discord に接続できています。
Bot を追加したサーバーで `/help` を実行し、コマンド一覧が表示されることを確認してください。
Bot を動かしている間は、起動したプログラムを実行したままにしておきます。
停止するときは、ターミナルで `Ctrl+C` を押します。

## 使い方

Discord のメッセージ入力欄で `/` を入力し、候補から Party のコマンドを選びます。

**例：6 面のサイコロを振る**

`/roll` を選び、`maximum`（面数）に `6` を指定して送信します。

```text
/roll maximum:6
```

1〜6 のいずれかの結果が表示されます。`maximum` には **2〜1000 の整数**を指定できます。

**例：投票を作成する**

`/poll` を選び、質問と 2 つの選択肢を入力します。`hour` を `1` にすると、受付期間は 1 時間です。

```text
/poll question:ピザにしますか？ option1:はい option2:いいえ hour:1
```

`option3` で 3 つ目の選択肢も追加できます。`hour` を省略した場合は 24 時間です。
すべての引数は、[投票の使い方](docs/ja/COMMANDS.ja.md#投票)で確認できます。

- **一覧を見る：** `/help` を使います。`!help` は無効です。
- **詳しい使い方を見る：** `/commands` を使い、左右のボタンでページを切り替えます。
  180 秒間操作しないとボタンが無効になるため、続けて使う場合は再実行してください。
  全 5 ページで `/help`・`/ping`・`/roll`・`/poll` を扱います。
- **日本語で使う：** Discord の言語設定を日本語にします。コマンド名は英語のままです。
- **表示範囲：** 通常の応答はチャンネルに表示され、共通のエラーメッセージは実行した本人にだけ表示されます。

連続実行の制限や表示言語の詳細は、[コマンドガイド](docs/ja/COMMANDS.ja.md)で確認できます。

## 困ったときは

| 状況 | 確認すること |
| --- | --- |
| `TOKEN` が未設定・空というエラーで終了する | README と同じフォルダーに `.env` があるか、`TOKEN` に値を設定したか確認してください。 |
| コマンドが候補に表示されない | Bot の起動ログを確認し、[セットアップガイド](docs/ja/SETUP.ja.md)で招待設定やコマンドの利用権限を見直してください。 |
| コマンドの連続実行でエラーになる | 実行間隔に制限があります。[コマンドガイド](docs/ja/COMMANDS.ja.md#クールダウン)を確認し、少し待ってから再実行してください。 |
| 歓迎メッセージが届かない | サーバーのシステムチャンネル設定と、そこでの Bot の送信・埋め込みリンクの権限を確認してください。 |

## 詳しいドキュメント

| 読みたい内容 | ガイド |
| --- | --- |
| Bot の作成・招待、権限設定、uv での起動 | [セットアップ](docs/ja/SETUP.ja.md) |
| コマンドの引数、実行間隔、表示言語、応答の公開範囲 | [コマンド](docs/ja/COMMANDS.ja.md) |
| コマンド・イベントの拡張機能の追加、自動読み込み、エラー処理、手動テスト | [開発](docs/ja/DEVELOPMENT.ja.md) |
| バージョンごとの変更点 | [変更履歴](CHANGELOG.md) |

## ライセンス・謝辞

[MIT ライセンス](LICENSE)で公開しています。
[discord.py](https://discordpy.readthedocs.io/) と [python-dotenv](https://github.com/theskumar/python-dotenv) を使用しています。

この README は ChatGPT の支援を受けて作成しました。
