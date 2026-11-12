# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging
from pkgutil import iter_modules
from types import ModuleType

from discord.ext import commands

import events
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
        def _get_extensions(package: ModuleType) -> list[str]:
            return sorted(
                module.name
                for module in iter_modules(
                    package.__path__, prefix=f"{package.__name__}."
                )
                if not module.name.rsplit(".", 1)[-1].startswith("_")
            )

        extensions_cogs: list[str] = _get_extensions(cogs)
        extensions_events: list[str] = _get_extensions(events)

        for extension in extensions_cogs:
            await self.load_extension(extension)

        for extension in extensions_events:
            await self.load_extension(extension)

        await self.tree.set_translator(JapaneseTranslator())

        logging.info(f"Registered {self.event_count} event listeners.")

        synced = await self.tree.sync()
        logging.info(f"Synced {len(synced)} commands.")
