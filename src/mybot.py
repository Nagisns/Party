# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging

from discord.app_commands import AppCommand 
from discord.ext import commands
from discovery import ExtensionManager

import cogs
from localization import JapaneseTranslator


class MyBot(commands.Bot):
    @property
    def event_count(self) -> int:
        return sum(
            len(cog.get_listeners())
            for cog in self.cogs.values()
        )

    async def setup_hook(self) -> None:
        await ExtensionManager.load_extensions(self, cogs)

        await self.tree.set_translator(JapaneseTranslator())

        synced: list[AppCommand] = await self.tree.sync()

        logging.info(f"Registered {self.event_count} event listeners.")
        logging.info(f"Synced {len(synced)} commands.")
