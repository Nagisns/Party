from discord.ext import commands

class ReadyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Logged in as {self.bot.user}")

async def setup(bot: commands.Bot):
    await bot.add_cog(ReadyCog(bot))
