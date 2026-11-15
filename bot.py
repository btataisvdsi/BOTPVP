import discord
from discord.ext import commands, tasks
import os
from gamedig import GameDig

# جلب المتغيرات من Railway
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 1571463916347727973))
SERVER_IP = os.environ.get("SERVER_IP", "51.68.107.75")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 18458)) # البورت اللي تأكدنا أنه مفتوح

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
        print(f"❌ لم يتم العثور على القناة بالمعرف: {CHANNEL_ID}")
        return

    print("🔍 جاري الاستعلام عن سيرفر MTA...")
    
    try:
        # استعمال gamedig للاستعلام عن سيرفر MTA
        server_info = GameDig.query(ip=SERVER_IP, port=SERVER_PORT, type='mtasa')
        
        embed = discord.Embed(
            title="🟢 حالة سيرفر MTA - Lemehost",
            color=discord.Color.green()
        )
        embed.add_field(name="الحالة", value="**ON** (يعمل)", inline=True)
        embed.add_field(name="اللاعبون", value=f"**{server_info.players} / {server_info.maxplayers}**", inline=True)
        print(f"✅ السيرفر يعمل! اللاعبون: {server_info.players}/{server_info.maxplayers}")
        
    except Exception as e:
        print(f"⚠️ السيرفر متوقف أو هناك مشكلة في الاتصال: {e}")
        embed = discord.Embed(
            title="🔴 حالة سيرفر MTA - Lemehost",
            color=discord.Color.red()
        )
        embed.add_field(name="الحالة", value="**OFF** (متوقف)", inline=True)
        embed.add_field(name="اللاعبون", value="**0 / 0**", inline=True)

    try:
        # البحث عن رسالة قديمة لتحديثها
        async for message in channel.history(limit=50):
            if message.author == bot.user and message.embeds:
                await message.edit(embed=embed)
                print("🔄 تم تحديث الرسالة القديمة.")
                return
                
        # إرسال رسالة جديدة
        await channel.send(embed=embed)
        print("📩 تم إرسال رسالة جديدة إلى القناة.")
    except Exception as e:
        print(f"❌ فشل في إرسال الرسالة: {e}")

bot.run(TOKEN)
