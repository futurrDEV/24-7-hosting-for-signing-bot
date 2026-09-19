import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import threading
from server import start as start_server
from signings import start_signing

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Start the fake web server for Render free hosting
threading.Thread(target=start_server).start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=None, intents=intents)  # NO PREFIX

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Detect "sign" at the start
    if message.content.lower().startswith("sign"):
        ctx = await bot.get_context(message)

        # Must mention a player
        if len(message.mentions) == 0:
            return await message.channel.send("You must mention a player to sign.")

        player = message.mentions[0]

        # Extract extra text
        extra = (
            message.content.lower()
            .replace("sign", "")
            .replace(player.mention.lower(), "")
            .strip()
        )

        await start_signing(ctx, player, extra)

    await bot.process_commands(message)

bot.run(TOKEN)
