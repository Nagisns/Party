# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from textwrap import dedent

import discord
from discord import app_commands

JA_COMMON: dict[str, str] = {
    "An unexpected error occurred.": "予期しないエラーが発生しました。",
    "This command is on cooldown.": "このコマンドはクールダウン中です。",
    "You do not have permission to use this command.": "このコマンドを実行する権限がありません。",
}

JA_COMMANDS: dict[str, str] = {
    "Browse command details using navigation buttons.": "ボタンを使ってコマンドの詳細を確認します。",
    "This guide has expired. Run `/commands` again.": "このガイドの有効期限が切れました。`/commands` をもう一度実行してください。",
    "Commands List": "コマンド一覧",
    dedent("""
        Use the buttons below to view command details.

        **Table of Contents**

        **1. `/help`**
        View available commands and their descriptions.

        **2. `/ping`**
        Check the bot's latency in milliseconds (ms).

        **3. `/roll`**
        Roll a die with 2 to 1,000 sides.

        **4. `/poll`**
        Create a poll with two or three answers.
    """).strip(): dedent("""
        下のボタンでコマンドの詳細を確認できます。

        **目次**

        **1. `/help`**
        利用可能なコマンドとその説明を表示します。

        **2. `/ping`**
        Botの応答速度をミリ秒（ms）で確認します。

        **3. `/roll`**
        2〜1,000面のサイコロを1回振ります。

        **4. `/poll`**
        2〜3個の選択肢で投票を作成します。
    """).strip(),
    "Help Command": "/help コマンド",
    dedent("""
        Display a list of available commands.

        **Response**
        An embed listing command names and descriptions.

        **Parameters**
        None.

        **Cooldown**
        Once every 5 seconds.
    """).strip(): dedent("""
        利用可能なコマンドの一覧を表示します。

        **応答**
        コマンド名と説明を一覧にした埋め込みメッセージを表示します。

        **引数**
        なし。

        **クールダウン**
        5秒に1回使用できます。
    """).strip(),
    "Ping Command": "/ping コマンド",
    dedent("""
        Check the bot's latency in milliseconds (ms).

        **Response**
        `Pong! <latency>ms`

        **Parameters**
        None.

        **Cooldown**
        Once every 5 seconds.
    """).strip(): dedent("""
        Botの応答速度をミリ秒（ms）で確認します。

        **応答**
        `応答速度: <latency>ms`

        **引数**
        なし。

        **クールダウン**
        5秒に1回使用できます。
    """).strip(),
    "Roll Command": "/roll コマンド",
    dedent("""
        Roll a die with the specified number of sides.

        **Response**
        An embed showing `Rolling result: <result>`.
        The result ranges from 1 to `maximum` (inclusive).

        **Parameters**
        `maximum` (required): Number of sides, from 2 to 1,000.

        **Cooldown**
        Up to 3 uses every 10 seconds.
    """).strip(): dedent("""
        指定した面数のサイコロを1回振ります。

        **応答**
        `サイコロの結果: <result>` を埋め込みメッセージで表示します。
        結果は1から `maximum` まで（両端を含む）の整数です。

        **引数**
        `maximum`（必須）: サイコロの面数。2〜1,000で指定します。

        **クールダウン**
        10秒間に最大3回使用できます。
    """).strip(),
    "Poll Command": "/poll コマンド",
    dedent("""
        Create a poll with two or three answers.

        **Response**
        A Discord poll where each voter can select one answer.

        **Parameters**
        `question` (required): Question, from 1 to 300 characters.
        `option1` (required): First answer, from 1 to 55 characters.
        `option2` (required): Second answer, from 1 to 55 characters.
        `option3` (optional): Third answer, from 1 to 55 characters.
        `hour` (optional): Duration, from 1 to 240 hours. Defaults to 24.

        **Cooldown**
        Once every 10 seconds.
    """).strip(): dedent("""
        2〜3個の選択肢で投票を作成します。

        **応答**
        各ユーザーが選択肢を1つ選べるDiscordの投票を表示します。

        **引数**
        `question`（必須）: 質問。1〜300文字で指定します。
        `option1`（必須）: 1つ目の選択肢。1〜55文字で指定します。
        `option2`（必須）: 2つ目の選択肢。1〜55文字で指定します。
        `option3`（任意）: 3つ目の選択肢。1〜55文字で指定します。
        `hour`（任意）: 受付時間。1〜240時間で指定します。省略すると24時間です。

        **クールダウン**
        10秒に1回使用できます。
    """).strip(),
}

JA_HELP: dict[str, str] = {
    "Party Commands": "Party コマンド一覧",
    "Display a list of available commands.": "利用可能なコマンドの一覧を表示します。",
}

JA_PING: dict[str, str] = {
    "Check bot latency.": "Botの応答速度を確認します。",
    "Error: Could not measure ping.": "Pingが測定できませんでした。",
    "Pong! {latency}ms": "応答速度: {latency}ms"
}

JA_ROLL: dict[str, str] = {
    "Roll a die with the specified number of sides.": "指定した面数のサイコロを1回振ります。",
    "Number of sides on the die (2-1000).": "サイコロの面数（2〜1000）。",
    "Rolling result: {result}": "サイコロの結果: {result}"
}

JA_POLL: dict[str, str] = {
    "Create a poll.": "投票を作成します。",
    "Question for the poll (1-300 characters).": "投票の質問（1〜300文字）。",
    "First answer option (1-55 characters).": "1つ目の選択肢（1〜55文字）。",
    "Second answer option (1-55 characters).": "2つ目の選択肢（1〜55文字）。",
    "Third answer option (optional, 1-55 characters).": "3つ目の選択肢（任意、1〜55文字）。",
    "Poll duration in hours (1-240; default: 24).": "投票の受付時間（1〜240時間、既定値: 24）。",
}

JA_GUILD_JOIN: dict[str, str] = {
    "Thanks for inviting me!": "招待ありがとうございます！",
    (
    "Hello, everyone!\n"
    "I'm happy to be here. Check out my commands to see how I can help."
    ): (
    "みなさん、こんにちは！\n"
    "このサーバーに参加できてうれしいです。"
    "コマンド一覧を確認して、ぜひ使ってみてください。"
    ),
}

JA_TRANSLATIONS: dict[str, str] = (
    JA_COMMON | JA_COMMANDS | JA_HELP | JA_PING | JA_ROLL | JA_POLL | JA_GUILD_JOIN
)

def translate_for_locale(locale: discord.Locale, message: str) -> str:
    if locale == discord.Locale.japanese:
        return JA_TRANSLATIONS.get(message, message)

    return message

def translate(interaction: discord.Interaction, message: str) -> str:
    return translate_for_locale(interaction.locale, message)

class JapaneseTranslator(app_commands.Translator):
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext) -> str | None:
        if locale == discord.Locale.japanese:
            return JA_TRANSLATIONS.get(string.message)

        return None
