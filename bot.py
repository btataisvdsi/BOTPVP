import discord
from discord.ext import commands, tasks
import mtasanpystatus
import os
import asyncio
import time

# جلب التوكن من إعدادات GitHub (Secrets)
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = 1571463916347727973
SERVER_IP = "51.68.107.75"
SERVER_PORT = 13335  # البورت اللي كيبان فالتصويرة

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول كـ {bot.user}")
    update_status_panel.start()

@tasks.loop(minutes=5) # التحديث كل 5 دقايق
async def update_status_panel():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    try:
        # محاولة جلب حالة السيرفر
        server = mtasanpystatus(ip=SERVER_IP, port=SERVER_PORT)
        
        embed = discord.Embed(
            title="🟢 حالة سيرفر MTA - Lemehost",
            color=discord.Color.green()
        )
        embed.add_field(name="الحالة", value="**ON** (يعمل)", inline=True)
        embed.add_field(name="اللاعبون", value=f"**{server.players} / {server.maxplayers}**", inline=True)
        
    except Exception as e:
        embed = discord.Embed(
            title="🔴 حالة سيرفر MTA - Lemehost",
            color=discord.Color.red()
        )
        embed.add_field(name="الحالة", value="**OFF** (متوقف)", inline=True)
        embed.add_field(name="اللاعبون", value="**0 / 0**", inline=True)

    # البحث على رسالة قديمة ديال البوت باش نعدلوها (باش ما نعمروش الروم بالرسائل)
    async for message in channel.history(limit=50):
        if message.author == bot.user and message.embeds:
            await message.edit(embed=embed)
            return
            
    # إلا ما لقيناش رسالة، كنصيفطو واحدة جديدة
    await channel.send(embed=embed)

# هاد الدالة كتخلي البوت يخدم لمدة 3.5 سوايع ومن بعد كيطفى باش GitHub Actions يبدل العملية بجديدة
async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    # كنديرو وقت محدد باش البوت ما يتقتلش من طرف GitHub
    time.sleep(3.5 * 60 * 60) # كيخدم 3 سوايع و 30 دقيقة
