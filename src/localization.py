# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import discord
from discord import app_commands

JA_TRANSLATIONS: dict[str, str] = {
    "Display a list of available commands.": "利用可能なコマンドの一覧を表示します。",
    "Check bot latency": "Botの応答速度を確認します。",
    "Party Commands": "Party コマンド一覧",
    "An unexpected error occurred.": "予期しないエラーが発生しました。",
    "You do not have permission to use this command.": "このコマンドを実行する権限がありません。",
    "This command is on cooldown.": "このコマンドはクールダウン中です。",
    "Pong! {latency}ms": "応答速度: {latency}ms",
}

def translate(interaction: discord.Interaction, message: str) -> str:
    if interaction.locale == discord.Locale.japanese:
        return JA_TRANSLATIONS.get(message, message)

    return message

class JapaneseTranslator(app_commands.Translator):
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext) -> str | None:
        if locale == discord.Locale.japanese:
            return JA_TRANSLATIONS.get(string.message)

        return None
