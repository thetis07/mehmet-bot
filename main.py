import discord
import random
import time
import os
import json
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

cooldowns = {}  # {user_id: last_buyult_time}


@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı.")


@bot.event
async def on_message(message):
    if message.content.lower().strip() == "slm":
        kullanici = message.author.name
        await message.channel.send(f"assalam {kullanici}!!11!")

    elif message.content.lower().strip() == "mrb":
        kullanici = message.author.name
        await message.channel.send(f"mrbbb {kullanici}!!11!")

    await bot.process_commands(message)


@bot.command()
async def purge(ctx, miktar):
    sil = await ctx.channel.purge(limit=int(miktar))
    await ctx.send(f"önceki {miktar} dene mesajlar silindi mehmet",
                   delete_after=3)


@bot.command()
async def yazitura(ctx, cevap: str):
    liste = ["yazı", "tura"]
    secilen = random.choice(liste)

    if cevap == secilen:
        await ctx.send(f"the cevap was {secilen}, kazandın helal lan türk")

    else:
        await ctx.send(f"the cevap was {secilen}, mal kürt kazanamadın")


@bot.command()
async def meme(ctx):
    memes = [
        "image1",
        "image2",
        "image3",
        "image4",
        "image5",
        "image6",
        "image7",
        "image8",
        "image9",
    ]
    secilen = random.choice(memes)
    with open(f"memes/{secilen}.png", "rb") as f:
        pic = discord.File(f)
        await ctx.send(file=pic)


@bot.command()
async def sik(ctx, option: str = None):
    user_id = str(ctx.author.id)

    # Dosyadan veriyi oku, yoksa boş dict yap
    if os.path.exists("dicks.json"):
        with open("dicks.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Eğer option parametresi yoksa uyar
    if option is None:
        await ctx.send("Lütfen bir seçenek gir: buyult / kaccm / top")
        return

    # cooldown sadece 'buyult' seçeneğinde geçerli
    if option == "buyult":
        now = time.time()
        cooldown_time = 7200  # 2 saat = 7200 saniye
        last_time = cooldowns.get(user_id, 0)

        if now - last_time < cooldown_time:
            kalan = int(cooldown_time - (now - last_time))
            await ctx.send(
                f"{ctx.author.mention}, bu komutu tekrar kullanmak için {kalan} saniye beklemelisin."
            )
            return
        else:
            cooldowns[user_id] = now

        buyume_rakamlari = list(range(1, 13))
        secilen_buyume = random.choice(buyume_rakamlari)
        boy = data.get(user_id, 0)
        boy += secilen_buyume
        data[user_id] = boy

        with open("dicks.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(
            f"{ctx.author.mention}, sikinin boyu {secilen_buyume} cm arttı! toplam boyun: {boy} cm 🍆"
        )
        return

    # cooldown yok, diğer seçenekler:
    if option == "kaccm":
        boy = data.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention}, sikiniz tam olarak {boy} cm!")
        return

    if option == "top":
        if not data:
            await ctx.send("Henüz hiç kimsenin büyü verisi yok.")
            return

        sirali = sorted(data.items(), key=lambda x: x[1], reverse=True)

        mesaj = "**Sunucu dick boy sıralaması:**\n"
        for i, (uid, boy) in enumerate(sirali, start=1):
            try:
                user = await ctx.guild.fetch_member(int(uid))
                isim = user.display_name if user else f"User ID: {uid}"
            except:
                isim = f"User ID: {uid}"

            mesaj += f"{i}. {isim} — {boy} cm\n"

            if len(mesaj) > 1900:
                mesaj += "\n...ve devamı var."
                break

        await ctx.send(mesaj)
        return

    # Bilinmeyen seçenek
    await ctx.send(
        "Geçersiz seçenek! buyult / kaccm / top seçeneklerini kullanabilirsin."
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention}, bu komutu tekrar kullanmak için {round(error.retry_after)} saniye beklemelisin."
        )
    else:
        raise error  # Diğer hataları normal şekilde göster


bot.run(
    "DISCORD_BOT_TOKEN")
