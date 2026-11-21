import asyncio
from unittest.mock import AsyncMock

import discord
from discord.ext import commands
import pytest

from localization import JapaneseTranslator
from mybot import MyBot


def test_setup_hook_loads_cogs_before_sync(monkeypatch: pytest.MonkeyPatch) -> None:
    async def run_test() -> None:
        async with MyBot(
            command_prefix="!", intents=discord.Intents.default(), help_command=None
        ) as bot:
            def check_registrations() -> list[discord.app_commands.AppCommand]:
                command_names = sorted(command.name for command in bot.tree.get_commands())
                assert command_names == ["commands", "help", "ping", "poll", "roll"]

                listener_counts = {
                    name: len(listeners) for name, listeners in bot.extra_events.items()
                }
                assert listener_counts == {"on_guild_join": 1, "on_ready": 1}
                assert "cogs.guide._view" not in bot.extensions
                assert isinstance(bot.tree.translator, JapaneseTranslator)
                return []

            sync = AsyncMock(side_effect=check_registrations)
            monkeypatch.setattr(bot.tree, "sync", sync)

            await bot.setup_hook()

            sync.assert_awaited_once_with()

    asyncio.run(run_test())


def test_setup_hook_skips_sync_when_extension_loading_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def run_test() -> None:
        async with MyBot(
            command_prefix="!", intents=discord.Intents.default(), help_command=None
        ) as bot:
            failure = commands.ExtensionFailed(
                "cogs.activities.poll", RuntimeError("extension setup failed")
            )
            monkeypatch.setattr(bot, "load_extension", AsyncMock(side_effect=failure))
            sync = AsyncMock()
            monkeypatch.setattr(bot.tree, "sync", sync)

            with pytest.raises(commands.ExtensionFailed) as exc_info:
                await bot.setup_hook()

            assert exc_info.value is failure
            sync.assert_not_called()

    asyncio.run(run_test())
