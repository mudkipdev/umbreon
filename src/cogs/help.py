from discord.ext import commands
import discord

class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=self.context.bot.config["colors"]["default"])

        for cog, commands in mapping.items():
            signatures = [c.qualified_name for c in commands]

            if not signatures:
                continue

            cog_name = getattr(cog, "qualified_name", "(no category)")
            embed.add_field(
                name=cog_name,
                value=" ".join(f"`{s}`" for s in signatures) or "(no commands)",
                inline=False,
            )

        await (self.get_destination()).send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Help: {command.qualified_name}",
            color=self.context.bot.config["colors"]["default"],
        )
        embed.description = f"```{self.get_command_signature(command)}```"
        embed.add_field(name="Description", value=command.help, inline=False)
        if command.aliases:
            embed.add_field(
                name="Aliases",
                value=" ".join([f"`{c}`" for c in command.aliases]),
                inline=False,
            )
        await (self.get_destination()).send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(
            title=f"Help: {group.qualified_name}",
            color=self.context.bot.config["colors"]["default"],
        )
        if group.short_doc:
            embed.add_field(name="Description", value=group.short_doc, inline=False)
        embed.add_field(
            name="Commands",
            value=" ".join([f"`{c}`" for c in group.commands]) or "(no commands)",
            inline=False,
        )

        await (self.get_destination()).send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"Help: {cog.qualified_name}",
            color=self.context.bot.config["colors"]["default"],
        )
        if cog.description:
            embed.add_field(name="Description", value=cog.description, inline=False)
        embed.add_field(
            name="Commands",
            value=" ".join([f"`{c}`" for c in cog.get_commands()]) or "(no commands)",
            inline=False,
        )
        await (self.get_destination()).send(embed=embed)

class Help(commands.Cog):
    """Loads the help command."""

    def __init__(self, bot):
        self.bot = bot
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.original_help_command

def setup(bot):
    bot.add_cog(Help(bot))
