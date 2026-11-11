import asyncio
from typing import cast
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from cogs.commands import CommandsView, GuidePage

def _create_interaction() -> MagicMock:
    interaction_mock: MagicMock = MagicMock(spec=discord.Interaction)
    interaction_mock.configure_mock(
        locale=discord.Locale.american_english,
        response=MagicMock(defer=AsyncMock()),
        edit_original_response=AsyncMock(),
    )
    return interaction_mock

@pytest.mark.parametrize(
    ("direction", "expected_page"),
    [("next_page", GuidePage.HELP), ("previous_page", GuidePage.POLL)],
)
def test_failed_update_preserves_page(direction: str, expected_page: GuidePage) -> None:
    async def run_test() -> None:
        interaction_mock: MagicMock = _create_interaction()
        interaction: discord.Interaction = cast(discord.Interaction, interaction_mock)
        view: CommandsView = CommandsView(interaction)
        button: discord.ui.Button = getattr(view, direction)
        response_mock: MagicMock = MagicMock(status=500, reason="Test failure")
        edit_response_mock: AsyncMock = cast(AsyncMock, interaction_mock.edit_original_response)
        edit_response_mock.side_effect = discord.HTTPException(
            response_mock, "Test failure"
        )

        with pytest.raises(discord.HTTPException):
            await button.callback(interaction)

        assert view.page == GuidePage.HOME

        retry_mock: MagicMock = _create_interaction()
        await button.callback(cast(discord.Interaction, retry_mock))

        retry_edit_mock: AsyncMock = cast(AsyncMock, retry_mock.edit_original_response)
        retry_edit_mock.assert_awaited_once()
        assert retry_edit_mock.call_args is not None
        embed: discord.Embed = retry_edit_mock.call_args.kwargs["embed"]
        assert view.page == expected_page
        assert embed.footer.text == f"page: {expected_page.value + 1}/5"

    asyncio.run(run_test())
