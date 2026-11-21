<div align="center">

# Party

[English](README.md) | **日本語**

Party は、Discord のスラッシュコマンドで投票を作ったり、サイコロを振ったりできる Bot です。
Discord の表示言語が日本語なら日本語で、それ以外なら英語で応答します。

![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-ECD53F?logo=dotenv&logoColor=black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

バージョン **0.4.3**（プレリリース） · [変更履歴](CHANGELOG.md)

[はじめかた](#はじめかた) · [使い方](#使い方) · [困ったときは](#困ったときは) · [プロジェクト構成](#プロジェクト構成)

## はじめかた

Python 3.15 以降と、Bot を追加できる Discord サーバーを用意します。
以下は pip を使う手順です。Bot の作成、トークンの取得、サーバーへの招待、uv を使う場合の手順は[セットアップガイド](docs/ja/SETUP.ja.md)を参照してください。

1. このリポジトリをクローンまたはダウンロードし、README のあるフォルダーで次のコマンドを実行します。

   ```bash
   python -m pip install "discord.py>=2.7.1" "python-dotenv>=1.2.4"
   ```

2. 同じフォルダーに `.env` を作成し、`your_bot_token_here` を自分の Bot トークンに置き換えます。トークンは非公開にしてください。`.env` は Git の管理対象から除外されています。

   ```env
   TOKEN=your_bot_token_here
   ```

3. Bot を起動します。

   ```bash
   python src/bot.py
   ```

ターミナルに `Logged in as ...` と表示されたら、Bot を招待したサーバーで `/help` を実行します。
コマンド一覧が表示されれば準備完了です。利用中は Bot を起動したままにし、停止するときはターミナルで `Ctrl+C` を押します。

## 使い方

Discord のメッセージ入力欄に `/` を入力し、候補から Party のコマンドを選びます。引数がある場合は、各欄に値を入力して送信します。

| 入力例 | 動作 |
| --- | --- |
| `/help` | 利用できるコマンドとその説明を一覧表示します。 |
| `/commands` | コマンドの使い方を表示します。左右の矢印ボタンでページをめくれます。 |
| `/ping` | Bot と Discord 間の WebSocket の遅延をミリ秒で表示します。 |
| `/roll maximum:6` | 6 面のサイコロを 1 回振ります。面数には 2〜1000 の整数を指定できます。 |
| `/poll question:ピザにしますか？ option1:はい option2:いいえ hour:1` | 2 択の投票を 1 時間受け付けます。`option3` で 3 択にできます。各自が選べるのは 1 つです。 |

投票の受付期間は 1〜240 時間で、`hour` を省略すると 24 時間です。各引数、連続実行の制限、応答の公開範囲は[コマンドガイド](docs/ja/COMMANDS.ja.md)で確認できます。

## 困ったときは

| 状況 | 確認すること |
| --- | --- |
| `TOKEN` が未設定または空というエラーで終了する | README と同じフォルダーの `.env` に `TOKEN` の値があるか確認してください。環境変数にも `TOKEN` を設定している場合は、そちらが優先されます。 |
| コマンドが候補に出ない | 起動ログに `Synced ... commands.` があるか確認し、招待時のスコープとチャンネルでのコマンド利用権限を見直してください。[セットアップガイド](docs/ja/SETUP.ja.md) |
| コマンドを続けて使うとエラーになる | 少し待ってから実行してください。一定時間内に使える回数は、コマンドごとの[クールダウンの一覧](docs/ja/COMMANDS.ja.md#クールダウン)で確認できます。 |
| Bot を招待しても歓迎メッセージが届かない | サーバーのシステムチャンネルを設定し、そのチャンネルで Bot に「チャンネルを見る」「メッセージを送信」「埋め込みリンク」の権限を付与してください。 |

## プロジェクト構成

主なファイルとディレクトリの構成は次のとおりです。

```text
Party/
├── .github/
│   └── workflows/
│       └── tests.yml     # GitHub Actions で pytest を実行
├── docs/
│   ├── en/               # 英語のセットアップ・コマンド・開発ガイド
│   └── ja/               # 日本語の各ガイド
├── src/
│   ├── bot.py            # エントリーポイント、トークンの読み込み、Bot の起動
│   ├── mybot.py          # Bot クラス、拡張機能の読み込み、コマンドの同期
│   ├── error_handler.py  # スラッシュコマンド共通のエラー処理
│   ├── localization.py   # 日本語訳と言語設定に応じた翻訳処理
│   └── cogs/             # コマンドとイベントリスナーを機能ごとに配置
│       ├── activities/   # /poll と /roll
│       ├── diagnostics/  # /ping と接続情報のログ出力
│       ├── guide/        # /help とページ切り替え式の /commands
│       └── guilds/       # Bot がサーバーに参加したときの歓迎メッセージ
├── tests/                # イベントのログ出力とコマンドガイドのページ移動の自動テスト
├── .python-version       # ローカル開発で使う Python のバージョン
├── pyproject.toml        # プロジェクト情報、依存関係、pytest の設定
├── uv.lock               # uv 用の依存関係のバージョン固定ファイル
├── start.ps1             # pytest の実行を選択できる PowerShell 起動スクリプト
├── README.md             # 英語版 README
├── README.ja.md          # 日本語版 README
├── CHANGELOG.md          # 変更履歴
├── SECURITY.md           # セキュリティポリシー
└── LICENSE               # MIT ライセンス
```

コマンドやイベントリスナーの追加方法は、[開発ガイド](docs/ja/DEVELOPMENT.ja.md)を参照してください。

## ライセンス・謝辞

[MIT ライセンス](LICENSE)で公開しています。
[discord.py](https://discordpy.readthedocs.io/) と [python-dotenv](https://github.com/theskumar/python-dotenv) を使用しています。

この README は ChatGPT の支援を受けて作成しました。
