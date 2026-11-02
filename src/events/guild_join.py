import logging
from typing import Optional

import discord
from discord import TextChannel
from discord.ext import commands

from localization import translate_for_locale

class GuildJoinCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:

        locale: discord.Locale = guild.preferred_locale
        embed: discord.Embed = discord.Embed(
            title=translate_for_locale(locale, "Thanks for inviting me!"),
            description=translate_for_locale(
                locale, 
                "Hello, everyone!\n" "I'm happy to be here. Check out my commands to see how I can help.",
            ),
            color=discord.Color.green(),
        )
        channel: Optional[TextChannel] = guild.system_channel

        if channel is not None:
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                logging.warning(f"Missing permissions to send greeting in guild: {guild.id}")
            except discord.HTTPException:
                logging.exception(f"Failed to send greeting in guild: {guild.id}")

async def setup(bot: commands.Bot):
    await bot.add_cog(GuildJoinCog(bot))
