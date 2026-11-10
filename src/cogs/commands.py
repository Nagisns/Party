# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging
import asyncio
from asyncio import Lock
from textwrap import dedent

import discord
from discord import app_commands
from discord.ext import commands

from localization import translate_for_locale
from error_handler import ErrorHandler

class CommandsView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction) -> None:
        super().__init__(timeout=180)
        self.page: int = 0
        self._page_lock: Lock = asyncio.Lock()
        self.locale: discord.Locale = interaction.locale
        self._last_interaction: discord.Interaction = interaction
        self.MIN_PAGES: int = 0
        self.MAX_PAGES: int = 4

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        self._last_interaction = interaction
        return True

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item) -> None:
        logging.error("Command guide interaction failed: %r", item, exc_info=error)

        message: str = translate_for_locale(interaction.locale, "An unexpected error occurred.")
        error_handler: ErrorHandler = ErrorHandler()

        await error_handler.send_error_message(interaction, message)

    async def on_timeout(self) -> None:
        async with self._page_lock:
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True

            notice: str = translate_for_locale(self.locale, "This guide has expired. Run `/commands` again.")

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
                    dedent("""
                        Use the buttons below to view command details.

                        **Table of Contents**

                        **1. `/help`**
                        View available commands and their descriptions.

                        **2. `/ping`**
                        Check the bot's latency in milliseconds (ms).

                        **3. `/roll`**
                        Roll a die with 2 to 1,000 sides.
                    """).strip()
                ),
                page=self.page + 1,
            )

        #Help Command Page
        if self.page == 1:
            return _embed_template(
                title=translate("Help Command"),
                description=translate(
                    dedent("""
                        Display a list of available commands.

                        **Response**
                        An embed listing command names and descriptions.

                        **Parameters**
                        None.

                        **Cooldown**
                        Once every 5 seconds.
                    """).strip()
                ),
                page=self.page + 1,
            )

        #Ping Command Page
        if self.page == 2:
            return _embed_template(
                title=translate("Ping Command"),
                description=translate(
                    dedent("""
                        Check the bot's latency in milliseconds (ms).

                        **Response**
                        `Pong! <latency>ms`

                        **Parameters**
                        None.

                        **Cooldown**
                        Once every 5 seconds.
                    """).strip()
                ),
                page=self.page + 1,
            )

        #Roll Command Page
        if self.page == 3:
            return _embed_template(
                title=translate("Roll Command"),
                description=translate(
                    dedent("""
                        Roll a die with the specified number of sides.

                        **Response**
                        An embed showing `Rolling result: <result>`.
                        The result ranges from 1 to `maximum` (inclusive).

                        **Parameters**
                        `maximum` (required): Number of sides, from 2 to 1,000.

                        **Cooldown**
                        Up to 3 uses every 10 seconds.
                    """).strip()
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
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(
            name="commands", 
            description=app_commands.locale_str("Browse command details using navigation buttons."),
        )
    @app_commands.checks.cooldown(rate=1, per=5.0)
    async def commands(self, interaction: discord.Interaction) -> None:

        view: CommandsView = CommandsView(interaction)
        embed: discord.Embed = view.create_embed()

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandsCog(bot))
