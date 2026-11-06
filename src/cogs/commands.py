# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging
import asyncio
from asyncio import Lock

import discord
from discord import app_commands
from discord.ext import commands

from mybot import MyBot
from localization import translate_for_locale

class CommandsView(discord.ui.View):
    def __init__(self, bot: MyBot, interaction: discord.Interaction) -> None:
        super().__init__(timeout=180)
        self.page: int = 0
        self._page_lock: Lock = asyncio.Lock()
        self.bot: MyBot = bot
        self.locale: discord.Locale = interaction.locale
        self._last_interaction: discord.Interaction = interaction
        self.MIN_PAGES: int = 0
        self.MAX_PAGES: int = 4

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        self._last_interaction = interaction
        return True

    async def on_timeout(self):
        async with self._page_lock:
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True

            notice = translate_for_locale(self.locale, "This guide has expired. Run `/commands` again.")

            try:
                await self._last_interaction.edit_original_response(content=notice, view=self)
            except discord.NotFound:
                return
            except discord.HTTPException:
                logging.exception("Failed to disable command guide buttons.")

    def create_embed(self) -> discord.Embed:
        def translate(message: str) -> str:
            return translate_for_locale(self.locale, message)

        def _embed_template(title: str, description: str, page: int) -> discord.Embed:
            embed: discord.Embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Colour.green(),
            )
            embed.set_footer(text=f"page: {page}/{self.MAX_PAGES}")
            return embed

        #Home Page
        if self.page == 0:
            return _embed_template(
                title=translate("Commands List"),
                description=translate(
                    "Use the buttons below to view command details.\n\n"
                    "**Table of Contents**\n\n"
                    "**1. `/help`**\n"
                    "View available commands and their descriptions.\n\n"
                    "**2. `/ping`**\n"
                    "Check the bot's latency in milliseconds (ms).\n\n"
                    "**3. `/roll`**\n"
                    "Roll a die with 2 to 1,000 sides."
                ),
                page=self.page + 1,
            )

        #Help Command Page
        if self.page == 1:
            return _embed_template(
                title=translate("Help Command"),
                description=translate(
                    "Display a list of available commands.\n\n"
                    "**Response**\n"
                    "An embed listing command names and descriptions.\n\n"
                    "**Parameters**\n"
                    "None.\n\n"
                    "**Cooldown**\n"
                    "Once every 5 seconds."
                ),
                page=self.page + 1,
            )

        #Ping Command Page
        if self.page == 2:
            return _embed_template(
                title=translate("Ping Command"),
                description=translate(
                    "Check the bot's latency in milliseconds (ms).\n\n"
                    "**Response**\n"
                    "`Pong! <latency>ms`\n\n"
                    "**Parameters**\n"
                    "None.\n\n"
                    "**Cooldown**\n"
                    "Once every 5 seconds."
                ),
                page=self.page + 1,
            )

        #Roll Command Page
        if self.page == 3:
            return _embed_template(
                title=translate("Roll Command"),
                description=translate(
                    "Roll a die with the specified number of sides.\n\n"
                    "**Response**\n"
                    "An embed showing `Rolling result: <result>`.\n"
                    "The result ranges from 1 to `maximum` (inclusive).\n\n"
                    "**Parameters**\n"
                    "`maximum` (required): Number of sides, from 2 to 1,000.\n\n"
                    "**Cooldown**\n"
                    "Up to 3 uses every 10 seconds."
                ),
                page=self.page + 1,
            )

        raise ValueError(f"Unsupported page: {self.page}")

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        async with self._page_lock:

            self.page -= 1

            if self.page < self.MIN_PAGES:
                self.page = self.MAX_PAGES - 1

            embed: discord.Embed = self.create_embed()

            await interaction.edit_original_response(embed=embed)

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        async with self._page_lock:

            self.page += 1

            if self.page == self.MAX_PAGES:
                self.page = self.MIN_PAGES

            embed: discord.Embed = self.create_embed()

            await interaction.edit_original_response(embed=embed)

class CommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="commands", 
            description=app_commands.locale_str("Browse command details using navigation buttons."),
        )
    @app_commands.checks.cooldown(rate=1, per=5.0)
    async def commands(self, interaction: discord.Interaction) -> None:

        view: CommandsView = CommandsView(self.bot, interaction)
        embed: discord.Embed = view.create_embed()

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandsCog(bot))
