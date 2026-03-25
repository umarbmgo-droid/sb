import discord
from discord.ext import commands
import asyncio
import os
import json
import time
from typing import Optional

# ===== CONFIG =====
PREFIX = "!"
OWNER_ID = 361069640962801664  # Your Discord ID

# ===== GET TOKENS FROM RAILWAY VARIABLES =====
def get_tokens_from_env():
    """Get tokens from TOKEN1, TOKEN2, TOKEN3... environment variables"""
    tokens = []
    i = 1
    while True:
        token = os.environ.get(f'TOKEN{i}')
        if token:
            tokens.append(token)
            print(f"📂 Loaded TOKEN{i}")
            i += 1
        else:
            break
    
    # Also check single TOKEN variable for backwards compatibility
    single_token = os.environ.get('TOKEN')
    if single_token and not tokens:
        tokens.append(single_token)
        print(f"📂 Loaded TOKEN (single)")
    
    return tokens

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
        
        @self.bot.command()
        async def stats(ctx):
            """Show connected accounts"""
            if ctx.author.id != OWNER_ID:
                return
            await ctx.message.delete()
            await ctx.send(f"Account: {self.bot.user.name} | Streaming: MAR")
        
        try:
            await self.bot.start(self.token)
        except Exception as e:
            print(f"❌ [{self.username}] Failed: {e}")

# ===== MAIN =====
async def main():
    tokens = get_tokens_from_env()
    
    if not tokens:
        print("❌ No tokens found! Add TOKEN1, TOKEN2, etc. in Railway Variables")
        print("\nExample:")
        print("  TOKEN1 = your_first_token_here")
        print("  TOKEN2 = your_second_token_here")
        print("  TOKEN3 = your_third_token_here")
        return
    
    print(f"\n🚀 Starting {len(tokens)} selfbots...\n")
    
    clients = []
    for i, token in enumerate(tokens):
        # Get username
        try:
            import requests
            headers = {'Authorization': token}
            r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            if r.status_code == 200:
                username = r.json()['username']
            else:
                username = f"Account_{i+1}"
        except:
            username = f"Account_{i+1}"
        
        client = SelfbotClient(token, username, i+1)
        clients.append(client)
        asyncio.create_task(client.start())
        await asyncio.sleep(1.5)  # Delay between logins to avoid rate limits
    
    print(f"\n✅ All {len(tokens)} selfbots connected!\n")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
