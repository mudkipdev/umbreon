import random

import aiohttp
import discord
import requests as requests
from discord.ext import commands
from datetime import datetime


class Fun(commands.Cog):
    """Fun Bot Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball',
                      description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['eight_ball', 'eightball', '8-ball'],
                      pass_context=True)
    async def eight_ball(self, ctx):
        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Definitely',
            'Why don\'t you figure it out yourself you lazy motherfucker',
            'Yes, but do it drunk as fuck!',
            'My sources say no, but they also said Hillary would win.',
            'Do not swipe right, it\'s your cousin',
            'Do swipe right, it\'s your cousin!',
            'Do what Jesus would do, die at the age of 33',
            'Trump uses me when deciding to go to war'

        ]
        em = discord.Embed(color=self.bot.config['colors']['default'])
        em.title = ":mage: The 8 ball wizard says..."
        em.description = (random.choice(possible_responses) + ", " + ctx.message.author.mention)
        await ctx.send(embed=em)

    @commands.command(name="covid")
    async def covid(self, ctx, *, country=None):
        """Updated information about Covid-19."""
        try:
            if country is None:
                embed = discord.Embed(title="This command is used like this: ```?covid [country]```", color=self.bot.config['colors']['default'],
                                      timestamp=ctx.message.created_at)
                await ctx.send(embed=embed)


            else:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{country}"
                stats = requests.get(url)
                json_stats = stats.json()
                country = json_stats["country"]
                total_cases = json_stats["cases"]
                today_cases = json_stats["todayCases"]
                total_deaths = json_stats["deaths"]
                today_deaths = json_stats["todayDeaths"]
                recovered = json_stats["recovered"]
                active = json_stats["active"]
                critical = json_stats["critical"]
                cases_per_one_million = json_stats["casesPerOneMillion"]
                deaths_per_one_million = json_stats["deathsPerOneMillion"]
                total_tests = json_stats["totalTests"]
                tests_per_one_million = json_stats["testsPerOneMillion"]

                embed2 = discord.Embed(title=f"**COVID-19 Status Of {country}**!",
                                       description="This Information Isn't Live Always, Hence It May Not Be Accurate!",
                                       color=self.bot.config['colors']['default'], timestamp=ctx.message.created_at)
                embed2.add_field(name="**Total Cases**", value=f'{total_cases:,}' if total_cases is not None else "Null",
                                 inline=True)
                embed2.add_field(name="**Today Cases**", value=f'{today_cases:,}' if today_cases is not None else "Null",
                                 inline=True)
                embed2.add_field(name="**Total Deaths**",
                                 value=f'{total_deaths:,}' if total_deaths is not None else "Null", inline=True)
                embed2.add_field(name="**Today Deaths**",
                                 value=f'{today_deaths:,}' if today_deaths is not None else "Null", inline=True)
                embed2.add_field(name="**Recovered**", value=f'{recovered:,}' if recovered is not None else "Null",
                                 inline=True)
                embed2.add_field(name="**Active**", value=f'{active:,}' if active is not None else "Null", inline=True)
                embed2.add_field(name="**Critical**", value=f'{critical:,}' if critical is not None else "Null",
                                 inline=True)
                embed2.add_field(name="**Cases Per One Million**",
                                 value=f'{cases_per_one_million:,}' if cases_per_one_million is not None else "Null",
                                 inline=True)
                embed2.add_field(name="**Deaths Per One Million**",
                                 value=f'{deaths_per_one_million:,}' if deaths_per_one_million is not None else "Null",
                                 inline=True)
                embed2.add_field(name="**Total Tests**", value=f'{total_tests:,}' if total_tests is not None else "Null",
                                 inline=True)
                embed2.add_field(name="**Tests Per One Million**",
                                 value=f'{tests_per_one_million:,}' if tests_per_one_million is not None else "Null",
                                 inline=True)

                embed2.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.send(embed=embed2)

        except:
            embed3 = discord.Embed(title="Invalid Country Name Try Again..!", color=self.bot.config['colors']['default'],
                                   timestamp=ctx.message.created_at)
            embed3.set_author(name="Error!")
            await ctx.send(embed=embed3)

    @commands.command()
    async def ping(self, ctx):
        """Pong! Get the bot's response time"""
        await ctx.channel.purge(limit=1)
        em = discord.Embed(color=self.bot.config['colors']['default'])
        em.title = ":ping_pong: Pong!"
        em.description = f'{round(self.bot.latency * 1000)} ms'
        await ctx.send(embed=em)

    @commands.command()
    async def mc(self, ctx, url=None):
        """Check the status of your favorite Minecraft Server!"""
        if url is None:
            return await ctx.send('Please provide a valid server URL or IP!')
        else:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://api.mcsrvstat.us/2/{url}') as r:
                    resp = await r.json()

            if resp["online"] is True:
                embed = discord.Embed(
                    title=f"Server status for {url}",
                    color=self.bot.config['colors']['default'],
                    description=f"Server Online!!! \n Players:{resp['players']['online']}",
                    timestamp=datetime.utcnow())
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title=f"Server status for {url}",
                    color=self.bot.config['colors']['default'],
                    description="Server is Offline!",
                    timestamp=datetime.utcnow())
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
