import asyncio
import logging
from typing import cast
from unittest.mock import MagicMock

import pytest
from discord.ext import commands

from events.ready import ReadyCog

def test_guild_count(caplog: pytest.LogCaptureFixture) -> None:
    bot_mock: MagicMock = MagicMock(spec=commands.Bot)

    bot_mock.configure_mock(guilds=[MagicMock(), MagicMock()], latency=0.05)

    bot: commands.Bot = cast(commands.Bot, bot_mock)
    cog: ReadyCog = ReadyCog(bot)

    with caplog.at_level(logging.INFO):
        asyncio.run(cog.on_ready())

    assert "Servers: 2" in caplog.text
