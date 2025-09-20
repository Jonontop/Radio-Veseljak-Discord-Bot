#Radio Veseljak Discord Bot

```py
import discord
from discord.ext import commands

TOKEN = "TOKEN_HERE"
RADIO_URL = "https://live.radio.si/Veseljak?t=1758375904462"  # Example radio stream

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def radio(ctx):
    if not ctx.author.voice:
        return await ctx.send("❌ Bejži v vc če me hočš čut gustek en!")

    channel = ctx.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice:
        voice = await channel.connect()

    if voice.is_playing():
        voice.stop()

    # Stream radio using ffmpeg
    voice.play(
        discord.FFmpegPCMAudio(RADIO_URL),
        after=lambda e: print("Radio stream ended:", e),
    )
    await ctx.send("📻 Zej ga pam, uživaj!")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send("⏹️ Ugasnil sem radio, adijo!")
    else:
        await ctx.send("⚠️ Gustek... nisem v vc.")


bot.run(TOKEN)

```
