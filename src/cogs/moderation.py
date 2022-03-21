from discord.ext import commands
import discord


class ModerationCog(commands.Cog):
    """Useful commands for moderators of a Discord server."""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = ''):
        """Temporarily removes a member from the server."""
        for member in members:
            await member.kick(reason=reason)

        wording = ' have been kicked from the server.' if len(members) > 1 else ' has been kicked from the server.'
        embed = discord.Embed(
            color=self.bot.config['colors']['moderation'],
            description=', '.join([member.name for member in members]) + wording
        )

        embed.set_author(name='Moderation', icon_url = self.bot.config['icons']['moderation'])
        await ctx.reply(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = ''):
        """Permanently removes a member from the server."""
        for member in members:
            await member.ban(reason=reason)

        wording = ' have been banned from the server.' if len(members) > 1 else ' has been banned from the server.'
        embed = discord.Embed(
            color=self.bot.config['colors']['moderation'],
            description=', '.join([member.name for member in members]) + wording
        )

        embed.set_author(name='Moderation', icon_url=self.bot.config['icons']['moderation'])
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(ModerationCog(bot))
