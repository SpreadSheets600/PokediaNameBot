import os
import re
import aiohttp
import asyncio
import datetime

import discord
from discord.ext import bridge

intents = discord.Intents.all()
bot = bridge.Bot(command_prefix="nb!", intents=intents)

import dotenv

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))


@bot.event
async def on_ready():

    print("--------------------------------")
    print("----- + PokeDia Name Bot + -----")
    print("--------------------------------")

    await bot.change_presence(activity=discord.Game(name="Naming Stuffs"))

    start_time = datetime.datetime.now()
    bot.start_time = start_time

    print("----- + LOADING COMMANDS + -----")
    print("--------------------------------")

    commands = 0

    for command in bot.walk_application_commands():
        commands += 1

        print(f"----- + Loaded : {command.name} ")

    print("--------------------------------")
    print(f"---- + Loaded : {commands}  Commands + -")
    print("--------------------------------")

    print("------- + LOADING COGS + -------")
    print(f"----- + Loaded : {len(bot.cogs)} Cogs + ------")
    print("--------------------------------")


@bot.bridge_command(
    name="ping",
    description="Check Bot's Latency & Uptime",
)
async def ping(ctx: discord.ApplicationContext):
    latency = bot.latency * 1000
    uptime = datetime.datetime.now() - bot.start_time

    uptime_seconds = uptime.total_seconds()
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds)).split(".")[0]

    embed = discord.Embed(
        title=":ping_pong: _*Pong !*_",
        description=f"Uptime : {uptime_str}\nLatency : {latency:.2f} ms",
        color=0x2F3136,
    )

    await ctx.respond(embed=embed)


bot.load_extension("cogs.commands")
bot.load_extension("cogs.predictor")

bot.run(token)
