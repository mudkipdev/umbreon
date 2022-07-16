import random

import aiohttp
import discord
from discord.ext import commands
from datetime import datetime

MINECRAFT_ENDPOINT = "https://api.mcsrvstat.us/2/{}"

class Fun(commands.Cog):
    """A cog dedicated to various fun commands such as 8 ball."""

    def __init__(self, bot):
        self.bot = bot

        with open("res/dadjokes.txt") as jokes:
            self.jokes = jokes.readlines()

        with open("res/8ball.txt") as _8ball_responses:
            self._8ball_responses = _8ball_responses.readlines()

    @commands.command(aliases=["joke"])
    async def dadjoke(self, ctx):
        embed = discord.Embed(
            title="Joke",
            description=" ".join(random.choice(self.jokes).split("<>")),
            color=self.bot.config["colors"]["default"]
        )
        await ctx.reply(embed=embed)

    @commands.command(name="8ball", aliases=["eightball"], help="Helps you answer a yes/no question.")
    async def _8ball(self, ctx):
        embed = discord.Embed(color=self.bot.config["colors"]["default"])
        embed.title = ":8ball: The 8 ball says..."
        embed.description = (random.choice(self._8ball_responses))
        await ctx.send(embed=embed)

    @commands.command(help="Get the bot's response time.")
    async def ping(self, ctx):
        embed = discord.Embed(color=self.bot.config["colors"]["default"])
        embed.title = ":ping_pong: Pong!"
        embed.description = f"{round(self.bot.latency * 1000)} ms"
        await ctx.send(embed=embed)

    @commands.command(aliases=["mc"])
    async def minecraft(self, ctx, ip):
        """Check the uptime of your favorite Minecraft server."""
        async with self.bot.client_session.get(MINECRAFT_ENDPOINT.format(ip)) as r:
            resp = await r.json()

        embed = discord.Embed(
            title=f"{ip} Status",
            color=self.bot.config["colors"]["default"],
            timestamp=datetime.utcnow(),
        )

        embed.description = "Server is online." if resp["online"] else "Server is offline."

        if resp.get("motd"):
            motd = "```\n" + "\n".join(resp["motd"]["clean"]) + "```"
            embed.add_field(name="MOTD", value=motd)

        if resp.get("players"):
            embed.add_field(
                name="Players",
                value=f"{resp['players']['online']}/{resp['players']['max']}",
                inline=False,
            )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
