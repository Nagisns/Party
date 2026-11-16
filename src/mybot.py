# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging

from discord.ext import commands

import events
import cogs
from localization import JapaneseTranslator
from tools import ExtensionManager

class MyBot(commands.Bot):
    @property
    def event_count(self) -> int:
        return sum(
            len(cog.get_listeners())
            for cog in self.cogs.values()
        )

    async def setup_hook(self) -> None:
        cogs_ext_mrg: ExtensionManager = ExtensionManager()
        events_ext_mrg: ExtensionManager = ExtensionManager()

        extensions_cogs: list[str] = cogs_ext_mrg.discover_extensions(cogs)
        extensions_events: list[str] = events_ext_mrg.discover_extensions(events)

        for extension in extensions_cogs:
            await self.load_extension(extension)

        for extension in extensions_events:
            await self.load_extension(extension)

        await self.tree.set_translator(JapaneseTranslator())

        logging.info(f"Registered {self.event_count} event listeners.")

        synced = await self.tree.sync()
        logging.info(f"Synced {len(synced)} commands.")
