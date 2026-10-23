# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from discord.ext import commands

from localization import JapaneseTranslator

class MyBot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.tree.set_translator(JapaneseTranslator())

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands.")
