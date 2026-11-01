# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from pkgutil import iter_modules

from discord.ext import commands

import cogs
from localization import JapaneseTranslator

class MyBot(commands.Bot):
    async def setup_hook(self) -> None:
        extensions = sorted(
            module.name
            for module in iter_modules(cogs.__path__, prefix=f"{cogs.__name__}.")
            if not module.name.rsplit(".", 1)[-1].startswith("_")
        )
        for extension in extensions:
            await self.load_extension(extension)

        await self.tree.set_translator(JapaneseTranslator())

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands.")
