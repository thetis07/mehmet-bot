import discord
import random
import time
import os
import sys
import json
import subprocess
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

if os.path.exists("cooldowns.json"):
    with open("cooldowns.json", "r") as f:
        try:
            cooldowns = json.load(f)
        except json.JSONDecodeError:
            cooldowns = {}
else:
    cooldowns = {}


@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı.")

@bot.event
async def on_message(message):
    msg = message.content.lower().strip()
    kullanici = message.author.display_name

    if message.author.bot:  # Bu satır çok önemli
        return

    if msg in ["slm", "selam", "sa"]:
        await message.channel.send(f"assalam {kullanici}!!11!")

    elif msg in ["mrb", "mbr", "merhaba"]:
        await message.channel.send(f"mrbbb {kullanici}!!11!")

    elif msg in ["mehmet"]:
        mehmetler = ["mehmet", "Mehmet", "MEHMET"]
        secim = random.choice(mehmetler)
        await message.channel.send(secim)

    elif msg in ["ney"]:
        ney = "[ney](https://media.discordapp.net/stickers/1145389186510246040.png?size=160&name=ney)"
        await message.channel.send(ney)

    elif msg in ["direk"]:
        direk = "[direk](https://media.discordapp.net/stickers/1218860265274081344.png?size=160&name=direk)"
        await message.channel.send(direk)

    elif msg in ["zurna"]:
        zurna = "https://media.discordapp.net/attachments/1072612084690460763/1335950062798508156/ZURNA-KURSU-ESEV-scaled.png?ex=6888be73&is=68876cf3&hm=064acd205bcff14575f72a840cd3b1437854da21fa964b0afdf64fa1d59f0c11&format=webp&quality=lossless&width=988&height=659&"
        await message.channel.send(zurna)

    await bot.process_commands(message)

@bot.command()
@commands.is_owner()
async def reload(ctx):
    await ctx.send("🔁 Yeniden başlatılıyor...")
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, miktar):
    sil = await ctx.channel.purge(limit=int(miktar))

@bot.command(aliases=["sole"])
async def say(ctx, *, contentx):
    await ctx.message.delete()
    await ctx.send(contentx)

@bot.command()
async def gugul(ctx, *, aratilcak_sey):
    await ctx.send(f"[{aratilcak_sey}]"+"(https://letmegooglethat.com/?q="+aratilcak_sey.replace(" ", "+")+")")

@bot.command(aliases=["dakdakgo"])
async def ddg(ctx, *, aratilcak_sey):
    await ctx.send(f"[{aratilcak_sey}]"+f"(https://lmddgtfy.net/?q={aratilcak_sey.replace(" ", "%20")})")

@bot.command()
async def yazitura(ctx, cevap: str):
    liste = ["yazı", "tura"]
    secilen = random.choice(liste)

    if cevap == secilen:
        await ctx.send(f"the cevap was {secilen}, kazandın helal lan türk")

    else:
        await ctx.send(f"the cevap was {secilen}, mal kürt kazanamadın")

@bot.command()
async def secim(ctx, option1, option2):
    options = [option1, option2]
    secilen = random.choice(options)
    await ctx.send(f"cıkan secim : {secilen}")

@bot.command(aliases=["beyz","base"])
async def base64(ctx, option, *, mesaj):
    if option == "encode" or option == "e":
        result = subprocess.getoutput(f"echo '{mesaj}' | base64")
        await ctx.send(f"{mesaj} --> {result}")

    elif option == "decode" or option == "d":
        result = subprocess.getoutput(f"echo '{mesaj}' | base64 -d")
        await ctx.send(f"{mesaj} --> {result}")

    else:
        await ctx.send("duzgun secnek gir yarraaaam")

@bot.command()
async def meme(ctx):
    memes = [
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326969662410793/image1.png?ex=687a0b01&is=6878b981&hm=31012c814267081b54c9d60366544b936cab05e76563cfbca0769b5202496cf5&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326970056671242/image2.png?ex=687a0b01&is=6878b981&hm=0ab15f2b8e69c32ef15655c9c9c7b328bd1bd8d73f063b0533c408f00447703b&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326970547671140/image3.png?ex=687a0b01&is=6878b981&hm=a21b76d81eb7bbf86c9f3c770a934207a29fc2cc606d775f1a3c65b9f236e840&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326971012976720/image4.png?ex=687a0b01&is=6878b981&hm=73df1fde526b4bfffafeb17ec2b0c92f212c2278156f62479d4684f8dc866347&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326971528871957/image5.png?ex=687a0b01&is=6878b981&hm=1e60a0518695f5eaf279e21884f7975e5ad763dac4d6401d9c6ccf8ffda513d0&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326971931791471/image6.png?ex=687a0b02&is=6878b982&hm=7a27308c51a92df17a5650cfbeb2a6e9fdf04e78be5f4f6863b907119242d7b1&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326972355153990/image7.png?ex=687a0b02&is=6878b982&hm=0117ae4ca537eb79943dbc7744b9edfea7fd86e3cc93d692540712240692c223&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326972778774681/image8.png?ex=687a0b02&is=6878b982&hm=5c12e92cf96b32cbcb9db4d290b1633bf427f627f42147cc033d37e83cdcbb76&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395326974062497893/image9.png?ex=687a0b02&is=6878b982&hm=e0add52ef84503355ceefa516d0ecfffda96ded267a3447f2c6e17cbe7d92c54&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395328412071104523/kumar_oynarken_ben_1.png?ex=687a0c59&is=6878bad9&hm=1da2d366ce2e4ba49268ca0a9064a554ff1503c7ed2c411a289e1d1b53653c5a&",
        "https://cdn.discordapp.com/attachments/1395326899252625501/1395493324080812144/image.png?ex=687aa5ef&is=6879546f&hm=8ebabeac818ec3ced4a6aea29554d7bfbdd7c6d6528a72120008dedffea1774e&"
    ]
    secilen = random.choice(memes)
    await ctx.send(secilen)

@bot.command()
async def ping(ctx):
    '''
    This text will be shown in the help command
    '''

    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(f"pinpon oc {latency}ms")


@bot.command(aliases=["pipi", "Pipi", "PİPİ", "Sik", "SİK", "cuk", "Cuk", "CUK"])
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
        await ctx.send("https://tenor.com/view/rock-one-eyebrow-raised-rock-staring-the-rock-gif-22113367")
        return

    # cooldown sadece 'buyut' seçeneğinde geçerli
    if option == "buyult" or option == "kaldir" or option == "kaldır":
        now = time.time()
        cooldown_time = 7200  # 2 saat = 7200 saniye
        last_time = cooldowns.get(user_id, 0)

        if now - last_time < cooldown_time:
            kalan = int(cooldown_time - (now - last_time))
            saat = int(kalan/3600)
            dakika = int((kalan%3600) / 60)
            user = ctx.author.mention
            
            if saat >= 1:
                await ctx.send(f"{user}, sikini {saat} saat {dakika} dakika sonra buyultebilcen gral.")
                return

            if saat == 0:
                await ctx.send(f"{user}, sikini {dakika} dakika sonra buyultebilcen gral.")
                return

        else:
            cooldowns[user_id] = now
            with open("cooldowns.json", "w") as f:
                json.dump(cooldowns, f, indent=4)


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
            await ctx.send("kimsenin siki yok yani siksiz world")
            return

        sirali = sorted(data.items(), key=lambda x: x[1], reverse=True)

        mesaj = "> **sarvarın en buyuk siklileri:**\n"
        for i, (uid, boy) in enumerate(sirali, start=1):
            try:
                user = await ctx.guild.fetch_member(int(uid))
                isim = user.display_name if user else f"> User ID: {uid}"
            except:
                isim = f"User ID: {uid}"

            mesaj += f"> {i}. {isim} — {boy} cm\n"

            if len(mesaj) > 1900:
                mesaj += "\n...ve devamı var."
                break

        await ctx.send(mesaj)
        return

    if option == "superbuyult" or option == "superkaldir" or option == "superkaldır":
        now = time.time()
        cooldown_time = 3600  # 1 saat = 3600 saniye
        last_time = cooldowns.get(user_id + "_super", 0)

        if now - last_time < cooldown_time:
            kalan = int(cooldown_time - (now - last_time))
            dakika = int((kalan % 3600) / 60)
            saniye = int(kalan % 60)
            await ctx.send(f"{ctx.author.mention}, süper büyütme için {dakika} dakika {saniye} saniye daha bekle gral.")
            return

        # Cooldown'u kaydet
        cooldowns[user_id + "_super"] = now
        with open("cooldowns.json", "w") as f:
            json.dump(cooldowns, f, indent=4)

        secilen_bk = random.randint(20, 40)
        sans = random.random()  # 0 ile 1 arasında sayı

        boy = data.get(user_id, 0)

        if sans <= 0.5:
            # Büyütme
            boy += secilen_bk
            sonuc = f"sanslı orospu cocu! 🍆\nsikin {secilen_bk} cm uzadı. toplam: {boy} cm!"
        else:
            # Küçültme (negatif olmaması için kontrol)
            boy -= secilen_bk
            if boy < 0:
                boy = 0
            sonuc = f"allaaan malı haha! 😆\nsikin {secilen_bk} cm kısaldı. yeni boy: {boy} cm."

        data[user_id] = boy

        with open("dicks.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"{ctx.author.mention}, {sonuc}")
        return

    # Bilinmeyen seçenek
    await ctx.send(
        "allahsız kürt seçenekler bunlar sadece: buyult / superbuyult / kaccm / top"
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention}, bu komutu tekrar kullanmak çin {round(error.retry_after)/60} saat beklemelisin."
        )
    else:
        raise error  # Diğer hataları normal şekilde göster

bot.run("MTM5NDYzNTc0NTMwMTM2NDgzNg.G2YQaP.5a0M4AukYXr-H07Nq1QpC9oZSyO9JyJ8dm9rF0")
