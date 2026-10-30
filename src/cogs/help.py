import discord
from discord import app_commands
from discord.ext import commands

from localization import translate

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description=app_commands.locale_str("Display a list of available commands."))
    @app_commands.checks.cooldown(rate=1, per=5.0)
    async def help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=translate(interaction, "Party Commands"), color=discord.Color.green())

        for command in self.bot.tree.get_commands():
            description = translate(interaction, command.description)

            embed.add_field(name=command.name, value=description, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))
