import asyncio
import random
from fuzzywuzzy import fuzz
import discord
from discord.ext import commands
import json

from src.bot import config


class Jeopardy(commands.Cog):
    """A Jeopardy question answer game utilizing Levenshtein Distance to calculate answer matching (beta)."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.attempts = 0

    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    @commands.command()
    async def jeopardy(self, ctx):
        """Generates a Jeopardy question from over 200,000 historical Jeopardy Questions."""
        try:
            with open('JEOPARDY_QUESTIONS1.json') as f:
                data = json.loads(f.read())
                position = random.randint(0, 199999)
                question = data[position]['question']
                answer = data[position]['answer']

                category = data[position]['category']
                value = data[position]['value']
                airDate = data[position]['air_date']
                em = discord.Embed(color=config["game_color"])
                em.title = "Jeopardy!"
                em.add_field(name='Question', value=str(question))
                em.add_field(name='Value', value=str(value))
                em.set_thumbnail(url='https://miro.medium.com/max/10000/1*34zoBTjiSqQsq9Ptswrg0A.jpeg')
                em.description = category
                em.add_field(name='Air Date', value=airDate)
                await ctx.send(embed=em)

        except (KeyError, FileNotFoundError) as e:
            raise e

        correct_answer = answer

        def check(m):
            return m.channel.id == ctx.channel.id and m.author.bot is False and m.content.startswith(ctx.prefix) is False

        while self.attempts < 3:
            try:
                message = await self.bot.wait_for('message', check=check, timeout=20.0)
                ratio = fuzz.ratio(message.content.lower(), correct_answer.lower())
                try:
                    partial_ratio = fuzz.partial_ratio(message.content.lower(), correct_answer.lower())

                # Catch and ignore invalid characters that can not be parsed by fuzzy
                except ValueError as e:
                    continue

                if len(answer.split()) >= 2:
                    if ratio >= 60 and partial_ratio >= 75:
                        self.attempts = 0
                        return await message.reply(f'Correct! {correct_answer}---{ratio,partial_ratio}% Match.')

                    else:
                        self.attempts += 1
                        attempts_left = 3 - self.attempts
                        await message.reply(f'Incorrect! {attempts_left} attempts remaining.')

                elif ratio >= 75:
                    self.attempts = 0
                    return await message.reply(f'Correct! {correct_answer}---{ratio}% Match.')

                else:
                    self.attempts += 1
                    attempts_left = 3 - self.attempts
                    await message.reply(f'Incorrect! {attempts_left} attempts remaining.')

            except asyncio.TimeoutError:
                self.attempts = 0
                return await ctx.send(f'Sorry you ran out of time! The correct answer was \'{answer}\'.')

        else:
            self.attempts = 0
            return await ctx.send(f'Sorry you ran out of attempts! The correct answer was \'{answer}\'.')


def setup(bot):
    bot.add_cog(Jeopardy(bot))
