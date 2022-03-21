import random

import aiohttp
import discord
from discord.ext import commands
from datetime import datetime


class Fun(commands.Cog):
    """A Cog dedicated to various Fun Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball",
                      aliases=["eight_ball", "eightball", "8-ball"],
                      )
    async def eight_ball(self, ctx):
        """Answers a yes/no question."""
        possible_responses = [
            "That is a resounding no",
            "It is not looking likely",
            "Too hard to tell",
            "It is quite possible",
            "Definitely",
            "Why don\'t you figure it out yourself you lazy motherfucker",
            "Yes, but do it drunk as fuck!",
            "My sources say no, but they also said Hillary would win.",
            "Do not swipe right, it\'s your cousin",
            "Do swipe right, it\'s your cousin!",
            "Do what Jesus would do, die at the age of 33",
            "Trump uses me when deciding to go to war"

        ]
        em = discord.Embed(color=self.bot.config["colors"]["default"])
        em.title = ":mage: The 8 ball wizard says..."
        em.description = (random.choice(possible_responses) + ", " + ctx.message.author.mention)
        await ctx.send(embed=em)

    @commands.command()
    async def ping(self, ctx):
        """Pong! Get the bots response time"""
        em = discord.Embed(color=self.bot.config["colors"]["default"])
        em.title = ":ping_pong: Pong!"
        em.description = f"{round(self.bot.latency * 1000)} ms"
        await ctx.send(embed=em)

    @commands.command(aliases=["minecraft"])
    async def mc(self, ctx, url):
        """Check the status of your favorite Minecraft Server!"""
        if url is None:
            return await ctx.send("Please provide a valid server URL or IP!")
        else:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.mcsrvstat.us/2/{url}") as r:
                    resp = await r.json()

            if resp["online"]:
                embed = discord.Embed(
                    title=f"Server status for {url}",
                    color=self.bot.config["colors"]["default"],
                    description=f"Server Online!!! \n Players:{resp['players']['online']}",
                    timestamp=datetime.utcnow())
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title=f"Server status for {url}",
                    color=self.bot.config["colors"]["default"],
                    description="Server is Offline!",
                    timestamp=datetime.utcnow())
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
