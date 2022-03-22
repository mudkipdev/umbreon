import os
import json
import sys
import asyncio
import logging
import traceback

from discord.ext import commands
from dotenv import load_dotenv
import discord
import aiohttp
import toml

load_dotenv()

CONFIG_FILE = "config/config.toml"

config = toml.load(open(CONFIG_FILE))
cogs = config["cogs"]


class Umbreon(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = toml.load(open(CONFIG_FILE))
        self.client_session = asyncio.get_event_loop().run_until_complete(self.create_client_session())
        self.load_extension("jishaku")

        for extension in cogs:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()

    async def is_owner(self, user: discord.User) -> bool:
        return await super().is_owner(user) or user.id in self.config["owners"]

    async def create_client_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def close(self) -> None:
        await self.client_session.close()
        await super().close()


if __name__ == "__main__":
    bot = Umbreon(command_prefix=config["prefix"])
    bot.run(os.environ.get("TOKEN"), reconnect=True)
