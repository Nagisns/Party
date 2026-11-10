# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import sys

import discord
from dotenv import load_dotenv

from mybot import MyBot
from error_handler import ErrorHandler

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

error_handler: ErrorHandler = ErrorHandler()
bot.tree.error(error_handler.on_app_command_error)

if __name__ == "__main__":
    bot.run(TOKEN, root_logger=True)
