import discord
from discord.ext import commands, tasks
import asyncio
import os
import json
import time
from typing import Optional

# ===== CONFIG =====
PREFIX = "!"
OWNER_ID = 361069640962801664  # Your Discord ID

# ===== BOT CLIENT CLASS =====
class SelfbotClient:
    def __init__(self, token, username, index):
        self.token = token
        self.username = username
        self.index = index
        self.bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all(), help_command=None)
        self.is_ready = False
        
    async def start(self):
        @self.bot.event
        async def on_ready():
            self.is_ready = True
            print(f"✅ [{self.username}] Logged in")
            # Set streaming status to "MAR"
            await self.bot.change_presence(activity=discord.Streaming(
                name="MAR",
                url="https://www.twitch.tv/mar"
            ))
            print(f"🎬 [{self.username}] Status set to: STREAMING MAR")
        
        @self.bot.event
        async def on_message(message):
            if message.author.id == self.bot.user.id:
                return
            await self.bot.process_commands(message)
        
        @self.bot.command()
        async def ping(ctx):
            if ctx.author.id != OWNER_ID:
                return
            await ctx.message.delete()
            await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")
        
        @self.bot.command()
        async def status(ctx, *, text):
            """Change status - !status streaming MAR"""
            if ctx.author.id != OWNER_ID:
                return
            await ctx.message.delete()
            await self.bot.change_presence(activity=discord.Streaming(
                name=text,
                url="https://www.twitch.tv/mar"
            ))
            await ctx.send(f"Status changed to: {text}")
        
        try:
            await self.bot.start(self.token)
        except Exception as e:
            print(f"❌ [{self.username}] Failed: {e}")

# ===== LOAD TOKENS =====
def load_tokens():
    """Load tokens from tokens.txt file"""
    tokens = []
    try:
        with open('tokens.txt', 'r') as f:
            for line in f:
                token = line.strip()
                if token and not token.startswith('#'):
                    tokens.append(token)
        print(f"📂 Loaded {len(tokens)} tokens")
        return tokens
    except FileNotFoundError:
        print("❌ tokens.txt not found!")
        return []

# ===== MAIN =====
async def main():
    tokens = load_tokens()
    
    if not tokens:
        print("No tokens found. Add tokens to tokens.txt")
        return
    
    print(f"\n🚀 Starting {len(tokens)} selfbots...\n")
    
    clients = []
    for i, token in enumerate(tokens):
        # Get username preview
        try:
            import requests
            headers = {'Authorization': token}
            r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            if r.status_code == 200:
                username = r.json()['username']
            else:
                username = f"Token_{i+1}"
        except:
            username = f"Token_{i+1}"
        
        client = SelfbotClient(token, username, i+1)
        clients.append(client)
        asyncio.create_task(client.start())
        await asyncio.sleep(1)  # Small delay between logins
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
