import random

import discord
from discord import app_commands
from discord.ext import commands

from localization import translate

class RollCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="roll", description=app_commands.locale_str("Roll a die with the specified number of sides."))
    @app_commands.describe(maximum=app_commands.locale_str("Number of sides on the die (2-1000)."))
    @app_commands.checks.cooldown(rate=3, per=10.0)
    async def roll(self, interaction: discord.Interaction, maximum: app_commands.Range[int, 2, 1000]) -> None:

        MIN_NUMBER: int = 1
        MAX_NUMBER: int = maximum
        result: int = random.randint(MIN_NUMBER, MAX_NUMBER)

        title: str = translate(interaction, "Rolling result: {result}")
        embed = discord.Embed(title=title.format(result=result), color=discord.Color.green())

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RollCog(bot))
