import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

from signings import start_signing

@bot.command()
async def sign(ctx, member: discord.Member, *, extra=None):
    await start_signing(ctx, member, extra)

bot.run(TOKEN)







