# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import sys

import discord
from dotenv import load_dotenv

from error_handler import ErrorHandler
from mybot import MyBot

def main() -> None:
    load_dotenv()

    token = os.getenv("TOKEN")

    if token is None:
        sys.exit("The TOKEN environment variable is not set.")

    if not token.strip():
        sys.exit("The TOKEN environment variable is empty.")

    intents = discord.Intents.default()
    intents.message_content = True

    bot = MyBot(command_prefix="!", intents=intents,help_command=None)

    error_handler = ErrorHandler()
    bot.tree.error(error_handler.on_app_command_error)

    bot.run(token, root_logger=True)

if __name__ == "__main__":
    main()
