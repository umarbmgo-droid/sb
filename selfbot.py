import discord
from discord.ext import commands
import asyncio
import os
import json
import time
import requests
from datetime import datetime

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
    await bot.process_commands(message)

# ===== COMMANDS =====
@bot.command()
async def ping(ctx):
    if ctx.author.id != OWNER_ID:
        return
    await ctx.message.delete()
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def status(ctx, *, text):
    if ctx.author.id != OWNER_ID:
        return
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Streaming(
        name=text,
        url="https://www.twitch.tv/mar"
    ))
    await ctx.send(f"Status changed to: {text}")

@bot.command()
async def stats(ctx):
    if ctx.author.id != OWNER_ID:
        return
    await ctx.message.delete()
    await ctx.send(f"Account: {bot.user.name} | ID: {bot.user.id}")

# ===== RUN =====
if __name__ == "__main__":
    print("🚀 Starting Selfbot...")
    bot.run(TOKEN)
