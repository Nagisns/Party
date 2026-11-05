# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from mybot import MyBot

class CommandsView(discord.ui.View):
    def __init__(self, bot: MyBot) -> None:
        super().__init__(timeout=180)
        self.page: int = 0
        self._page_lock = asyncio.Lock()
        self.bot: MyBot = bot
        self.MIN_PAGES: int = 0
        self.MAX_PAGES: int = 4

    def create_embed(self) -> discord.Embed:
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
                title="Commands List",
                description=(
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
                title="Help Command",
                description=(
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
                title=("Ping Command"),
                description=(
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
                title="Roll Command",
                description=(
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

        view: CommandsView = CommandsView(self.bot)
        embed: discord.Embed = view.create_embed()

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandsCog(bot))
