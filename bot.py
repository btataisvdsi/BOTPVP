import discord
from discord.ext import commands, tasks
import mtasanpystatus
import os

# جلب المتغيرات من Railway
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 1571463916347727973))
SERVER_IP = os.environ.get("SERVER_IP", "51.68.107.75")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 13458)) # البورت الصحيح

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول كـ {bot.user}")
    update_status_panel.start()

@tasks.loop(minutes=5)
async def update_status_panel():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"❌ ما لقيتش الروم بالـ ID: {CHANNEL_ID}")
        return

    print("🔍 كنشيك على سيرفر MTA...")
    
    try:
        # محاولة الاتصال بالسيرفر
        server = mtasanpystatus(ip=SERVER_IP, port=SERVER_PORT)
        
        embed = discord.Embed(
            title="🟢 حالة سيرفر MTA - Lemehost",
            color=discord.Color.green()
        )
        embed.add_field(name="الحالة", value="**ON** (يعمل)", inline=True)
        embed.add_field(name="اللاعبون", value=f"**{server.players} / {server.maxplayers}**", inline=True)
        print("✅ السيرفر شاعل!")
        
    except Exception as e:
        print(f"⚠️ السيرفر طافي أو كاين مشكل فـ الاتصال: {e}")
        embed = discord.Embed(
            title="🔴 حالة سيرفر MTA - Lemehost",
            color=discord.Color.red()
        )
        embed.add_field(name="الحالة", value="**OFF** (متوقف)", inline=True)
        embed.add_field(name="اللاعبون", value="**0 / 0**", inline=True)

    try:
        async for message in channel.history(limit=50):
            if message.author == bot.user and message.embeds:
                await message.edit(embed=embed)
                print("🔄 تم تحديث الرسالة القديمة.")
                return
                
        await channel.send(embed=embed)
        print("📩 تم إرسال رسالة جديدة للروم.")
    except Exception as e:
        print(f"❌ ما قدرتش نصيفط الرسالة. تأكد من صلاحيات البوت: {e}")

bot.run(TOKEN)
