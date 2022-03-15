from discord.ext import commands
from dotenv import load_dotenv
import discord
import toml
import os

load_dotenv()

CONFIG_FILE = "config/config.toml"

class Umbreon(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = toml.load(open(CONFIG_FILE))

config = toml.load(open(CONFIG_FILE))
bot = Umbreon(command_prefix = config["prefix"])

@bot.event
async def on_ready():
    print("Ready!")

bot.run(os.environ.get("TOKEN"))
