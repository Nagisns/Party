import asyncio
from pathlib import Path
from unittest.mock import AsyncMock

import discord
from discord.ext import commands
from discovery import ExtensionManager
import pytest

import cogs
from cogs.leveling import _xp
from localization import JapaneseTranslator
from mybot import MyBot


def test_setup_hook_loads_cogs_before_sync(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(_xp, "DB_FILE", tmp_path / "level.db")
    expected_extensions = set(ExtensionManager.discover_extensions(cogs))

    async def run_test() -> None:
        async with MyBot(
            command_prefix="!", intents=discord.Intents.default(), help_command=None
        ) as bot:
            def check_registrations() -> list[discord.app_commands.AppCommand]:
                assert set(bot.extensions) == expected_extensions
                assert bot.tree.get_commands()
                assert bot.extra_events
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
