import time
import discord
import shelve
from discord.ext import commands
from pynput.keyboard import Key, Controller
from dotenv import load_dotenv
import os

# Load environment variables, specify in .env file
load_dotenv()
AUTHROLE = os.getenv('AUTHROLE') # role that can use the addcredits and setcredits commands, default is 'door'
TOKEN = os.getenv('TOKEN') # bot token, get this from the discord developer portal

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# set bot prefix, change here if you want to use something other than $
bot = commands.Bot(command_prefix='$', intents=intents)

# utility functions
def deductCredit(ctx):
    db[str(ctx.author.id)] = db[str(ctx.author.id)] - 1

async def hascredit(ctx):
    return db[str(ctx.author.id)] >= 1

# BOT COMMANDS START HERE
## sync slash commands to discord, has a pretty harsh ratelimit so call this only when you make changes to the commands
@bot.command()
@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("synced")

## Set credits for a user using an absolute value, use if values are messed up
@bot.hybrid_command(aliases=['scr'])
@commands.has_role(AUTHROLE)
async def setcredits(ctx, user: discord.Member, amount: int):
    db[str(user.id)] = amount
    await ctx.send(f"set credits for {user} to {amount}")  

@setcredits.error
async def setcredits_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"you do not have the {AUTHROLE} role")

## Increment a user's credits by a certain amount, you'll use this most of the time
@bot.hybrid_command(aliases=['acr'])
@commands.has_role(AUTHROLE)
async def addcredits(ctx, user: discord.Member, amount: int):
    db[str(user.id)] = db[str(user.id)] + amount
    await ctx.send(f"added {amount} credits to {user}, {user} now has {db[str(user.id)]} credits")

@addcredits.error
async def addcredits_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"you do not have the {AUTHROLE} role")

## check a user's credits
@bot.hybrid_command(aliases=['cr'])
async def credits(ctx, user: discord.Member):
    await ctx.send(f"{user} has {db[str(user.id)]} credits")

## send a single keypress to the computer, costs credits
@bot.hybrid_command(aliases=['si'])
@commands.check(hascredit)
async def sendinput(ctx, input: str):
    deductCredit(ctx)
    keyboard.press(input)
    keyboard.release(input)
    await ctx.send(f"sent input <{input}>, you now have {db[str(ctx.author.id)]} credits")

@sendinput.error
async def sendinput_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"you do not have enough credits (1 credit per keypress)")

## send a string of keypresses to the computer with a given delay in ms, costs credits
@bot.hybrid_command(aliases=['sis'])
@commands.check(hascredit)
async def sendinputstring(ctx, inputs: str, delay: int = 15):
    deductCredit(ctx)
    for i in inputs:
        keyboard.tap(i)
        time.sleep(delay / 1000)
    await ctx.send(f"sent <{inputs}> with a delay of {delay} ms, you now have {db[str(ctx.author.id)]} credits")

@sendinputstring.error
async def sendinput_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"you do not have enough credits")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# run the bot
with shelve.open('credits', writeback=True) as db: # We use shelve for persistent credit count
    keyboard = Controller()
    bot.run(TOKEN)
