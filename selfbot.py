import discord
from discord.ext import commands
import asyncio
import os
import time

# ===== CONFIG =====
TOKEN = os.environ.get('TOKEN')
OWNER_ID = 361069640962801664
PREFIX = "!"

if not TOKEN:
    print("❌ ERROR: TOKEN not set in Railway Variables")
    exit(1)

# ===== BOT SETUP =====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ===== STATUS LOOP =====
async def status_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Streaming(
            name="MAR",
            url="https://www.twitch.tv/mar"
        ))
        await asyncio.sleep(30)

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ SELFBOT ONLINE: {bot.user.name}")
    print(f"🆔 User ID: {bot.user.id}")
    print(f"📊 Servers: {len(bot.guilds)}")
    bot.loop.create_task(status_loop())

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if not message.content.startswith(PREFIX):
        return
    if message.author.id != OWNER_ID:
        return

    args = message.content[1:].split()
    command = args[0].lower() if args else ""
    await message.delete()

    if command == "ping":
        await message.channel.send(f"Pong! {round(bot.latency * 1000)}ms")
    elif command == "status":
        if len(args) > 1:
            new_status = " ".join(args[1:])
            await bot.change_presence(activity=discord.Streaming(
                name=new_status,
                url="https://www.twitch.tv/mar"
            ))
            await message.channel.send(f"Status changed to: {new_status}")
        else:
            await message.channel.send("Usage: !status <text>")
    elif command == "stats":
        await message.channel.send(f"Account: {bot.user.name} | ID: {bot.user.id}")

# ===== RUN =====
if __name__ == "__main__":
    print("🚀 Starting Selfbot...")
    bot.run(TOKEN)
