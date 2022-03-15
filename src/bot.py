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
    def __init__(self):
        super().__init__(command_prefix=config['prefix'])
        self.config = toml.load(open(CONFIG_FILE))

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

bot = Umbreon(command_prefix=config['prefix'], reconnect=True)
await bot.run(os.environ.get('TOKEN'))
