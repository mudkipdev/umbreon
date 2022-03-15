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

cogs = (
    'cogs.example',
)

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

bot = Umbreon(command_prefix=config['prefix'])
await bot.run(os.environ.get('TOKEN'), reconnect=True)
