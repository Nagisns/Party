# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from typing import Optional
from datetime import timedelta

import discord
from discord import app_commands, Poll
from discord.ext import commands

class PollCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="poll", description=app_commands.locale_str("Create a poll."))
    @app_commands.describe(
        question=app_commands.locale_str("Question for the poll (1-300 characters)."),
        option1=app_commands.locale_str("First answer option (1-55 characters)."),
        option2=app_commands.locale_str("Second answer option (1-55 characters)."),
        option3=app_commands.locale_str("Third answer option (optional, 1-55 characters)."),
    )
    @app_commands.checks.cooldown(rate=1, per=10.0)
    async def pollfunc(
        self, 
        interaction: discord.Interaction,
        question: app_commands.Range[str, 1, 300],
        option1: app_commands.Range[str, 1, 55],
        option2: app_commands.Range[str, 1, 55],
        option3: Optional[app_commands.Range[str, 1, 55]],
        ) -> None:

        poll: Poll = Poll(question=question, duration=timedelta(hours=24.0))

        for option in (option1, option2, option3):
            if option is not None:
                poll.add_answer(text=option)

        await interaction.response.send_message(poll=poll)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PollCog(bot))
