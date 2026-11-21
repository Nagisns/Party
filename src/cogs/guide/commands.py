# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import discord
from discord import app_commands
from discord.ext import commands

from ._view import CommandsView


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
        embed: discord.Embed = view.create_embed(view.page)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandsCog(bot))
