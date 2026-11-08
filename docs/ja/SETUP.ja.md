# セットアップガイド

[English](../en/SETUP.md) | [日本語](SETUP.ja.md)

[README](../../README.ja.md) | [コマンド](COMMANDS.ja.md) | [開発](DEVELOPMENT.ja.md)

## 必要なもの

- Python 3.15 以降（`pyproject.toml` で指定）
- Discord Bot のアプリケーションと、その Bot トークン
- Bot を追加できる Discord サーバー
- `discord.py` 2.7.1 以降
- `python-dotenv` 1.2.4 以降

## セットアップ

### 1. プロジェクトを取得する

このリポジトリをクローンまたはダウンロードし、
プロジェクトのディレクトリでターミナルを開いてください。

### 2. 依存パッケージをインストールする

```bash
python -m pip install "discord.py>=2.7.1" "python-dotenv>=1.2.4"
```

上記のバージョン要件は `pyproject.toml` と一致しています。
`uv.lock` に記録されたバージョンをインストールする場合は、uv を使います。

```bash
uv sync --locked --no-dev
```

### 3. Discord Bot を作成・設定する

1. [Discord Developer Portal](https://discord.com/developers/applications) を開きます。
2. アプリケーションを作成し、**Bot** の設定を開きます。
3. Bot トークンを生成またはリセットし、次の手順で使うためにコピーします。
4. [Discord のアプリ設定ガイド](https://docs.discord.com/developers/quick-start/getting-started) に従い、
   `bot` と `applications.commands` のスコープを使って、サーバーへのインストールを設定します。
5. [サーバーへのインストール](https://docs.discord.com/developers/resources/application#installation-context) に必要な
   **サーバー管理（Manage Server）** 権限を持つアカウントで Bot を招待します。
   サーバーのテキストチャンネルでコマンドを使うメンバーには、
   **チャンネルを見る（View Channels）**、**メッセージを送信（Send Messages）**、
   **アプリコマンドを使う（Use Application Commands）** の権限が必要です。
   チャンネルごとの権限設定や
   [アプリケーションコマンドの権限](https://docs.discord.com/developers/interactions/application-commands#permissions) により、
   利用が制限される場合もあります。
   [コマンド実行時の権限に関する Discord チームの説明](https://github.com/discord/discord-api-docs/discussions/5097) も参照してください。

現在のスラッシュコマンドについては、インストール時に Bot ロールの追加権限を
要求する必要はありません（`permissions=0`）。テキストや埋め込みメッセージの応答には
[インタラクションへの応答](https://docs.discord.com/developers/interactions/receiving-and-responding#responding-to-an-interaction) を使い、
通常のチャンネルへのメッセージ送信とは異なる権限ルールが適用されます。
[インタラクションと Webhook の権限に関する Discord の説明](https://docs.discord.com/developers/change-log#changes-to-bot-permissions-for-interactions-and-webhooks) を参照してください。
Bot に **管理者（Administrator）** 権限を付ける必要はありません。

歓迎メッセージを受け取るには、サーバー設定でシステムチャンネルを指定し、
そのチャンネルで Bot に **チャンネルを見る（View Channel）**、
**メッセージを送信（Send Messages）**、**埋め込みリンク（Embed Links）** の権限を許可してください。
歓迎メッセージは通常のチャンネルメッセージとして送信するため、
[チャンネルへのメッセージ送信の権限](https://docs.discord.com/developers/resources/message#create-message) が適用されます。
Bot のロールとチャンネルごとの権限設定の両方を確認してください。
システムチャンネルが未設定の場合、歓迎メッセージは送信しません。
権限エラーは警告として、それ以外の HTTP エラーはトレースバック付きでログに記録します。

Bot はデフォルトの Gateway インテントを使います。
現在のスラッシュコマンドには **Message Content Intent**、**Server Members Intent**、
**Presence Intent** は不要で、これら 3 つの特権インテントは無効のままで利用できます。
詳しくは [discord.py のインテントガイド](https://discordpy.readthedocs.io/en/stable/intents.html#message-content) を参照してください。

### 4. 環境変数を設定する

プロジェクトのディレクトリに `.env` というファイルを作成します。

```env
TOKEN=your_bot_token_here
```

`your_bot_token_here` を自分の Bot トークンに置き換えてください。
トークンは公開せず、`.env` を Git にコミットしないでください。
このプロジェクトの `.gitignore` では、すでに `.env` を除外しています。

`TOKEN` を環境変数として直接設定することもできます。
[python-dotenv のドキュメント](https://github.com/theskumar/python-dotenv#readme) にあるとおり、
既存の環境変数は `.env` から読み込む値より優先されます。

`TOKEN` が未設定、空文字列、または空白文字だけの場合、
Bot はエラーメッセージを表示し、終了コード `1` で終了します。

### 5. Bot を起動する

プロジェクトのディレクトリで、次のコマンドを実行します。

```bash
python src/bot.py
```

uv で依存パッケージをインストールした場合は、プロジェクトの仮想環境で起動します。

```bash
uv run --locked --no-dev python src/bot.py
```

拡張機能の読み込みと起動ログの詳細は、[開発ガイド](DEVELOPMENT.ja.md)を参照してください。

起動したら、サーバーで `/commands`、`/help`、`/ping`、`/roll maximum:6` を試してください。
プレフィックスコマンドの `!help` は無効です。
コマンド一覧には `/help`、各コマンドの詳細には `/commands` を使ってください。
