# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import math
import logging

from discord.ext import commands

logger: logging.Logger = logging.getLogger(__name__)

class ReadyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        guild_count: int = len(self.bot.guilds)
        user_count: int = 0
        latency: float = self.bot.latency * 1000

        for guild in self.bot.guilds:
            if guild.member_count is not None:
                user_count += guild.member_count
        
        logger.info(f"Logged in as {self.bot.user}")
        logger.info(f"Servers: {guild_count}")
        logger.info(f"Users: {user_count}")

        if math.isfinite(latency):
            logger.info(f"Gateway latency: {latency:.2f} ms")
            return
        
        logger.info("Gateway latency: unavailable")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReadyCog(bot))
