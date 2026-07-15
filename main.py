import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
RADIO_URL = "https://live.radio.si/Veseljak?t=1758375904462"  # Radio stream

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        # Avtomatska sinhronizacija slash ukazov ob zagonu bota
        synced = await bot.tree.sync()
        print(f"🔄 Uspešno sinhroniziral {len(synced)} slash ukazov!")
    except Exception as e:
        print(f"❌ Napaka pri sinhronizaciji ukazov: {e}")


@bot.tree.command(name="radio", description="Zaženi radio Veseljak!")
async def radio(interaction: discord.Interaction):
    # Pri slash ukazih uporabljamo interaction.user namesto ctx.author
    if not interaction.user.voice:
        return await interaction.response.send_message(
            "❌ Bejži v vc če me hočš čut gustek en!", 
            ephemeral=True  # Ukaz vidi samo tisti, ki ga je poslal
        )

    channel = interaction.user.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    # Najprej pošljemo odgovor Discordu, da ne poteče čas (timeout)
    await interaction.response.send_message("📻 Zej ga pam, uživaj!")

    if not voice:
        voice = await channel.connect()

    if voice.is_playing():
        voice.stop()

    # Stream radio using ffmpeg
    voice.play(
        discord.FFmpegPCMAudio(RADIO_URL),
        after=lambda e: print("Radio stream ended:", e),
    )


@bot.tree.command(name="stop", description="Ugasni radio in me vrzi ven")
async def stop(interaction: discord.Interaction):
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    
    if voice and voice.is_connected():
        await voice.disconnect()
        await interaction.response.send_message("⏹️ Ugasnil sem radio, adijo!")
    else:
        await interaction.response.send_message(
            "⚠️ Gustek... nisem v vc.", 
            ephemeral=True
        )


bot.run(TOKEN)