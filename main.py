# This example requires the 'message_content' intent.
import time
import discord
import shelve
from discord.ext import commands
from pynput.keyboard import Key, Controller

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

async def is_allowed(ctx, user):
    role = discord.utils.find(lambda r: r.name == AUTHROLE, ctx.message.guild.roles)
    return role in user.roles

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def setCredits(ctx, user: discord.Member, amount: int):
    db[str(user.id)] = amount
    await ctx.send(f"set credits for {user} to {amount}")

@bot.command()
async def addCredits(ctx, user: discord.Member, amount: int):
    db[str(user.id)] = db[str(user.id)] + amount
    await ctx.send(f"added {amount} credits to {user}, {user} now has {db[str(user.id)]} credits")

@bot.command()
async def credits(ctx, user: discord.Member):
    await ctx.send(f"{user} has {db[str(user.id)]} credits")

@bot.command()
async def sendInput(ctx, input: str):
    keyboard.tap(input)
    await ctx.send(input)

@bot.command()
async def sendInputs(ctx, inputs: str, delay: int):
    for i in inputs:
        keyboard.tap(i)
        time.sleep(delay / 1000)
    await ctx.send(f"sent {inputs} with a delay of {delay} ms")

with shelve.open('credits', writeback=True) as db:
    keyboard = Controller()
    AUTHROLE = 'door'
    TOKEN = '' # DONT LOOK AT THIS

    bot.run(TOKEN) 


# TODO
# finish auth checking
# add defaults and error checking
# add runtime setup

