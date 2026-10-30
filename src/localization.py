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

JA_TRANSLATIONS: dict[str, str] = (
    JA_COMMON | JA_HELP | JA_PING | JA_ROLL
)

def translate(interaction: discord.Interaction, message: str) -> str:
    if interaction.locale == discord.Locale.japanese:
        return JA_TRANSLATIONS.get(message, message)

    return message

class JapaneseTranslator(app_commands.Translator):
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext) -> str | None:
        if locale == discord.Locale.japanese:
            return JA_TRANSLATIONS.get(string.message)

        return None
