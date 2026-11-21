# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from enum import IntEnum

import discord
from discord.ext import commands

from ._xp import XpRepository


class Rewards(IntEnum):
    SEND_MESSAGE = 10
    JOIN_VOICE_CHANNEL = 75
    STAY_VOICE_CHANNEL = 25

class LevelCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.guild is None or message.author.bot:
            return

        user_id: int = message.author.id
        guild_id: int = message.guild.id

        XpRepository.add_xp(guild_id=guild_id, user_id=user_id, xp=Rewards.SEND_MESSAGE)

async def setup(bot: commands.Bot) -> None:
    XpRepository.create()
    await bot.add_cog(LevelCog(bot))
