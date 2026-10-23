# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import sys

import discord
from discord import app_commands
from dotenv import load_dotenv

from mybot import MyBot
from localization import translate

load_dotenv()

try:
    TOKEN: str = os.environ["TOKEN"]

    if not TOKEN.strip():
        print("The TOKEN environment variable is empty.")
        sys.exit(1)

except KeyError:
    print("The TOKEN environment variable is not set.")
    sys.exit(1)

intents: discord.Intents = discord.Intents.default()
bot: MyBot = MyBot(command_prefix="!", intents=intents)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    print(f"Command error: {error}")

    message = "An unexpected error occurred."

    if isinstance(error, app_commands.MissingPermissions):
        message = "You do not have permission to use this command."
    elif isinstance(error, app_commands.CommandOnCooldown):
        message = "This command is on cooldown."

    message = translate(interaction, message)

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True,)

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="help", description=app_commands.locale_str("Display a list of available commands."))
@app_commands.checks.cooldown(rate=1, per=5.0)
async def help(interaction: discord.Interaction) -> None:
    embed = discord.Embed(title=translate(interaction, "Party Commands"), color=discord.Color.green(),)

    for command in bot.tree.get_commands():
        description = translate(interaction, command.description)

        embed.add_field(name=command.name, value=description, inline=False,)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping",description=app_commands.locale_str("Check bot latency"))
@app_commands.checks.cooldown(rate=1, per=5.0)
async def ping(interaction: discord.Interaction) -> None:
    latency = round(bot.latency * 1000)

    message = translate(interaction, "Pong! {latency}ms")
    await interaction.response.send_message(message.format(latency=latency))

if __name__ == "__main__":
    bot.run(TOKEN)
