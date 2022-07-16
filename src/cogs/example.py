from discord.ext import commands

class ExampleCog(commands.Cog):
    """Example cog for future reference."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="repeat", aliases=["copy", "mimic"], help="A simple command which repeats our input.",
    async def do_repeat(self, ctx, *, our_input: str):
        await ctx.send(our_input)

    @commands.command(name="add", aliases=["plus"], help="A simple command which does addition on two integer values.")
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        await ctx.send(f"The sum of **{first}** and **{second}**  is  **{first + second}**")

# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case ExampleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
    bot.add_cog(ExampleCog(bot))
