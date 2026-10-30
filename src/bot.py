# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import sys
import logging
import random

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
bot: MyBot = MyBot(command_prefix="!", intents=intents, help_command=None)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:

    message = "An unexpected error occurred."

    if isinstance(error, app_commands.MissingPermissions):
        message = "You do not have permission to use this command."
    elif isinstance(error, app_commands.CommandOnCooldown):
        message = "This command is on cooldown."
    else:
        logging.error("Command error: %s", error, exc_info=error)

    message = translate(interaction, message)

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="ping", description=app_commands.locale_str("Check bot latency."))
@app_commands.checks.cooldown(rate=1, per=5.0)
async def ping(interaction: discord.Interaction) -> None:
    try:
        latency: int = round(bot.latency * 1000)
        message = translate(interaction, "Pong! {latency}ms")
    except (OverflowError, ValueError):
        message = translate(interaction, "Error: Could not measure ping.")
        await interaction.response.send_message(message)
        return

    await interaction.response.send_message(message.format(latency=latency))

@bot.tree.command(name="roll", description=app_commands.locale_str("Roll a die with the specified number of sides."))
@app_commands.describe(maximum=app_commands.locale_str("Number of sides on the die (2-1000)."))
@app_commands.checks.cooldown(rate=3, per=10.0)
async def roll(interaction: discord.Interaction, maximum: app_commands.Range[int, 2, 1000]) -> None:

    MIN_NUMBER: int = 1
    MAX_NUMBER: int = maximum
    result: int = random.randint(MIN_NUMBER, MAX_NUMBER)

    title: str = translate(interaction, "Rolling result: {result}")
    embed = discord.Embed(title=title.format(result=result), color=discord.Color.green())

    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN, root_logger=True)
