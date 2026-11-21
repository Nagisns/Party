import asyncio
import logging
from typing import cast
from unittest.mock import MagicMock

import discord
import pytest
from discord import app_commands

from error_handler import ErrorHandler


def _create_interaction(locale: discord.Locale, *, response_done: bool) -> MagicMock:
    response = MagicMock(spec=discord.InteractionResponse)
    response.is_done.return_value = response_done
    return MagicMock(
        spec=discord.Interaction,
        locale=locale,
        response=response,
        followup=MagicMock(spec=discord.Webhook),
    )


@pytest.mark.parametrize("response_done", [False, True], ids=["initial", "followup"])
@pytest.mark.parametrize(
    "locale", [discord.Locale.american_english, discord.Locale.japanese], ids=["en", "ja"]
)
@pytest.mark.parametrize(
    ("error", "english_message", "japanese_message"),
    [
        pytest.param(
            app_commands.CommandOnCooldown(app_commands.Cooldown(1, 5.0), 4.0),
            "This command is on cooldown.",
            "このコマンドはクールダウン中です。",
            id="cooldown",
        ),
        pytest.param(
            app_commands.MissingPermissions(["manage_messages"]),
            "You do not have permission to use this command.",
            "このコマンドを実行する権限がありません。",
            id="missing-permissions",
        ),
        pytest.param(
            app_commands.AppCommandError("Internal error details"),
            "An unexpected error occurred.",
            "予期しないエラーが発生しました。",
            id="unexpected-error",
        ),
    ],
)
def test_on_app_command_error_sends_localized_ephemeral_message(
    error: app_commands.AppCommandError,
    english_message: str,
    japanese_message: str,
    locale: discord.Locale,
    response_done: bool,
) -> None:
    interaction = _create_interaction(locale, response_done=response_done)

    asyncio.run(
        ErrorHandler().on_app_command_error(cast(discord.Interaction, interaction), error)
    )

    message = japanese_message if locale == discord.Locale.japanese else english_message
    if response_done:
        interaction.followup.send.assert_awaited_once_with(message, ephemeral=True)
        interaction.response.send_message.assert_not_called()
    else:
        interaction.response.send_message.assert_awaited_once_with(message, ephemeral=True)
        interaction.followup.send.assert_not_called()


@pytest.mark.parametrize("response_done", [False, True], ids=["initial", "followup"])
def test_send_error_message_logs_http_failure(
    response_done: bool, caplog: pytest.LogCaptureFixture
) -> None:
    interaction = _create_interaction(discord.Locale.american_english, response_done=response_done)
    response = MagicMock(status=500, reason="Internal Server Error")
    failure = discord.HTTPException(response, "Test failure")
    send = interaction.followup.send if response_done else interaction.response.send_message
    send.side_effect = failure

    message = "An unexpected error occurred."
    with caplog.at_level(logging.ERROR):
        asyncio.run(ErrorHandler().send_error_message(cast(discord.Interaction, interaction), message))

    send.assert_awaited_once_with(message, ephemeral=True)
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.ERROR
    assert record.getMessage() == "Failed to send error message."
    assert record.exc_info is not None
    assert record.exc_info[1] is failure
