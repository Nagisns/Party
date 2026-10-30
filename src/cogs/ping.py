import discord
from discord import app_commands
from discord.ext import commands

from localization import translate

class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description=app_commands.locale_str("Check bot latency."))
    @app_commands.checks.cooldown(rate=1, per=5.0)
    async def ping(self, interaction: discord.Interaction) -> None:
        try:
            latency: int = round(self.bot.latency * 1000)
            message = translate(interaction, "Pong! {latency}ms")
        except (OverflowError, ValueError):
            message = translate(interaction, "Error: Could not measure ping.")
            await interaction.response.send_message(message)
            return

        await interaction.response.send_message(message.format(latency=latency))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCog(bot))
