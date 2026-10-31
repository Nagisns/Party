# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import sys
import logging

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

if __name__ == "__main__":
    bot.run(TOKEN, root_logger=True)
