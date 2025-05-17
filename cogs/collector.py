import ast
import sqlite3
import discord
from discord.ext import commands
from utilities.collector import add_collector

with open("source/names.txt", "r") as f:
    pokemon_names = ast.literal_eval(f.read())

async def autocomplete_pokemon(ctx: discord.AutocompleteContext):
    return pokemon_names

class CollectorCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="collect", description="Add a Pokémon to your collector list")
    async def collect(
        self,
        ctx: discord.ApplicationContext,
        pokemon_name: discord.Option(str, "Select Pokémon", autocomplete=discord.utils.basic_autocomplete(autocomplete_pokemon))
    ):
        user_id = ctx.user.id
        add_collector(user_id, pokemon_name)

        await ctx.respond(f"✅ You are now collecting **{pokemon_name}**!")

def setup(bot):
    bot.add_cog(CollectorCOG(bot))
