# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import discord
from discord import app_commands
from discord.ext import commands

from ._xp import XpRepository


class GetLevelCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="level", description=app_commands.locale_str("View your level in this server."))
    @app_commands.checks.cooldown(rate=1, per=5.0)
    async def get_level(self, interaction: discord.Interaction) -> None:
        guild: discord.Guild | None = interaction.guild

        if guild is None:
            raise app_commands.NoPrivateMessage()

        member: discord.User | discord.Member = interaction.user
        xp: int | None = XpRepository.get_user_xp(guild.id, member.id)

        if xp is None:
            await interaction.response.send_message("You haven't earned any XP in this server yet.")
            return

        embed = discord.Embed(title=f"{xp:,} XP", color=discord.Color.green())
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.set_footer(text=guild.name)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GetLevelCog(bot))
