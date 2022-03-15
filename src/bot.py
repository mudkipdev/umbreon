import json
import sys
import traceback

from discord.ext import commands
from dotenv import load_dotenv
import discord
import logging
import toml
import os

load_dotenv()

CONFIG_FILE = 'config/config.toml'

cogs = ("cogs.help", "cogs.jeopardy", "cogs.error")
config = toml.load(open(CONFIG_FILE))


class Umbreon(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = toml.load(open(CONFIG_FILE))
        self.load_extension("jishaku")

        for extension in cogs:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def is_owner(self, user: discord.User):
        return await super().is_owner(user) or user.id in self.config["owners"]

if __name__ == "__main__":
    bot = Umbreon(command_prefix=config['prefix'])
    bot.run(os.environ.get('TOKEN'), reconnect=True)
