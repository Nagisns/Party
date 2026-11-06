# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import discord
from discord import app_commands

JA_COMMON: dict[str, str] = {
    "An unexpected error occurred.": "予期しないエラーが発生しました。",
    "This command is on cooldown.": "このコマンドはクールダウン中です。",
    "You do not have permission to use this command.": "このコマンドを実行する権限がありません。",
}

JA_COMMANDS: dict[str, str] = {
    "Browse command details using navigation buttons.": "ボタンを使ってコマンドの詳細を確認します。",
    "Commands List": "コマンド一覧",
    (
        "Use the buttons below to view command details.\n\n"
        "**Table of Contents**\n\n"
        "**1. `/help`**\n"
        "View available commands and their descriptions.\n\n"
        "**2. `/ping`**\n"
        "Check the bot's latency in milliseconds (ms).\n\n"
        "**3. `/roll`**\n"
        "Roll a die with 2 to 1,000 sides."
    ): (
        "下のボタンでコマンドの詳細を確認できます。\n\n"
        "**目次**\n\n"
        "**1. `/help`**\n"
        "利用可能なコマンドとその説明を表示します。\n\n"
        "**2. `/ping`**\n"
        "Botの応答速度をミリ秒（ms）で確認します。\n\n"
        "**3. `/roll`**\n"
        "2〜1,000面のサイコロを1回振ります。"
    ),
    "Help Command": "/help コマンド",
    (
        "Display a list of available commands.\n\n"
        "**Response**\n"
        "An embed listing command names and descriptions.\n\n"
        "**Parameters**\n"
        "None.\n\n"
        "**Cooldown**\n"
        "Once every 5 seconds."
    ): (
        "利用可能なコマンドの一覧を表示します。\n\n"
        "**応答**\n"
        "コマンド名と説明を一覧にした埋め込みメッセージを表示します。\n\n"
        "**引数**\n"
        "なし。\n\n"
        "**クールダウン**\n"
        "5秒に1回使用できます。"
    ),
    "Ping Command": "/ping コマンド",
    (
        "Check the bot's latency in milliseconds (ms).\n\n"
        "**Response**\n"
        "`Pong! <latency>ms`\n\n"
        "**Parameters**\n"
        "None.\n\n"
        "**Cooldown**\n"
        "Once every 5 seconds."
    ): (
        "Botの応答速度をミリ秒（ms）で確認します。\n\n"
        "**応答**\n"
        "`応答速度: <latency>ms`\n\n"
        "**引数**\n"
        "なし。\n\n"
        "**クールダウン**\n"
        "5秒に1回使用できます。"
    ),
    "Roll Command": "/roll コマンド",
    (
        "Roll a die with the specified number of sides.\n\n"
        "**Response**\n"
        "An embed showing `Rolling result: <result>`.\n"
        "The result ranges from 1 to `maximum` (inclusive).\n\n"
        "**Parameters**\n"
        "`maximum` (required): Number of sides, from 2 to 1,000.\n\n"
        "**Cooldown**\n"
        "Up to 3 uses every 10 seconds."
    ): (
        "指定した面数のサイコロを1回振ります。\n\n"
        "**応答**\n"
        "`サイコロの結果: <result>` を埋め込みメッセージで表示します。\n"
        "結果は1から `maximum` まで（両端を含む）の整数です。\n\n"
        "**引数**\n"
        "`maximum`（必須）: サイコロの面数。2〜1,000で指定します。\n\n"
        "**クールダウン**\n"
        "10秒間に最大3回使用できます。"
    ),
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
    JA_COMMON | JA_COMMANDS | JA_HELP | JA_PING | JA_ROLL | JA_GUILD_JOIN
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
