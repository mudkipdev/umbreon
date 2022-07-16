from discord.ext import commands
import traceback
import discord

errors = {
    commands.MissingRequiredArgument: "{e.param.name} is a required argument.",
    commands.BadArgument: "Invalid argument.",
    commands.PrivateMessageOnly: "This command can only be used in private messages.",
    commands.NoPrivateMessage: "This command can only be used in a server.",
    commands.CommandNotFound: "This command does not exist.",
    commands.CommandOnCooldown: "Please wait another {round(e.retry_after)} seconds before using this command again.",
    commands.MaxConcurrencyReached: "This command has reached its maximum uses.",
    commands.NotOwner: "You must be the owner of this bot to use this command.",
    commands.MemberNotFound: "A member named {e.argument} does not exist.",
    commands.GuildNotFound: "A server named {e.argument} does not exist.",
    commands.RoleNotFound: "A role named {e.argument} does not exist.",
    commands.ChannelNotFound: "A channel named {e.argument} does not exist.",
    commands.MessageNotFound: "A message named {e.argument} does not exist.",
    commands.EmojiNotFound: "An emoji named {e.argument} does not exist.",
    commands.MissingPermissions: "You don't have permission to use this command.",
    commands.BotMissingPermissions: "I don't have permissions to execute this command.",
    commands.MissingRole: "You don't have the required role to use this command.",
    commands.MissingRole: "You don't have any of the required roles to use this command.",
    commands.BotMissingRole: "I don't have the required role to execute this command.",
    commands.BotMissingRole: "I don't have the required role to execute this command.",
    commands.NSFWChannelRequired: "This command can only be used in an NSFW channel.",
}

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception: Exception):
        embed = discord.Embed(color=self.bot.config["colors"]["error"])
        embed.set_author(name="Error", icon_url=self.bot.config["icons"]["error"])

        try:
            embed.description = errors[type(exception)].format(e=exception)
        except KeyError:
            raise exception

        else:
            await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
