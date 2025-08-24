import discord
import random
import time
import os
import sys
import json
import asyncio
import base64
import discord.ui
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Sunucu üyelerini çekebilmek için intents'i aktif ettim

bot = commands.Bot(command_prefix="?", intents=intents)

yasaklilar = [
        "@everyone",
        "@here",
        "@newler",
        "/"
        ]

# Cooldown ve data için JSON dosyalarını yükleme/kaydetme fonksiyonları
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_json(filename, dicks):
    with open(filename, "w") as f:
        json.dump(dicks, f, indent=4)

if os.path.exists("starboard.json"):
    with open("starboard.json", "r") as f:
        starboard_messages = json.load(f)
else:
    starboard_messages = {}

cooldowns = load_json("cooldowns.json")
dicks = load_json("dicks.json")
lottery_data = load_json("lottery.json")
active_fights = set()

@bot.event
async def on_ready():
    print(f"Bot {bot.user} olarak giriş yaptı.")
    print("-----")

BLOCKED_USERS = {"1111276725473656852",
                 "1057696323391987782"}

@bot.check
async def globally_block_users(ctx):
    return str(ctx.author.id) not in BLOCKED_USERS

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

STAR_THRESHOLD = 3
STARBOARD_CHANNEL_ID = 1402040749750489198
starboard_messages = {}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name != "⭐":
        return

    guild = bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author.bot:
        return

    for reaction in message.reactions:
        if reaction.emoji == "⭐":
            if reaction.count >= STAR_THRESHOLD:
                starboard_channel = guild.get_channel(STARBOARD_CHANNEL_ID)

                embed = discord.Embed(
                    description=message.content or "*[bos msj]*",
                    color=discord.Color.gold(),
                    timestamp=message.created_at
                )
                embed.set_author(
                    name=message.author.name,
                    icon_url=message.author.display_avatar.url
                )
                embed.add_field(
                    name="Bağlantı",
                    value=f"[gtmek icn dıkla]({message.jump_url})",
                    inline=False
                )
                embed.set_footer(text=f"{reaction.count} ⭐")

                # Medya varsa ekle (resim ya da video bağlantısı olarak)
                if message.attachments:
                    for attachment in message.attachments:
                        if attachment.content_type.startswith("image"):
                            embed.set_image(url=attachment.url)
                            break
                        elif attachment.content_type.startswith("video"):
                            embed.add_field(name="Video", value=attachment.url, inline=False)
                            break

                # Daha önce eklenmiş mi kontrol et
                if message.id in starboard_messages:
                    try:
                        old_msg = await starboard_channel.fetch_message(starboard_messages[message.id])
                        await old_msg.edit(embed=embed)
                    except discord.NotFound:
                        sent = await starboard_channel.send(embed=embed)
                        starboard_messages[message.id] = sent.id
                else:
                    sent = await starboard_channel.send(embed=embed)
                    starboard_messages[message.id] = sent.id
            break


@bot.command()
@commands.is_owner()
async def reload(ctx):
    await ctx.send("🔁 Yeniden başlatılıyor...")
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, miktar: int):
    await ctx.channel.purge(limit=miktar)

@bot.command(aliases=["meth"])
async def math(ctx, ilk, islem, ikinci):
    ilk = float(ilk)
    ikinci = float(ikinci)

    toplama = ilk + ikinci
    cikartma = ilk-ikinci    
    carpma = ilk*ikinci
    bolme = ilk/ikinci

    if islem == "+":
        await ctx.send(f"sonuc = {toplama}")
    elif islem == "-":
        await ctx.send(f"sonuc = {cikartma}")
    elif islem == "*":
        await ctx.send(f"sonuc = {carpma}")
    elif islem == "/":
        await ctx.send(f"sonuc = {bolme}")

@bot.command()
async def gugul(ctx, *, aratilcak_sey):
    await ctx.send(f"[{aratilcak_sey}]"+"(https://letmegooglethat.com/?q="+aratilcak_sey.replace(" ", "+")+")")

@bot.command(aliases=["dakdakgo"])
async def ddg(ctx, *, aratilcak_sey):
    await ctx.send(f"[{aratilcak_sey}]"+f"(https://lmddgtfy.net/?q={aratilcak_sey.replace(' ', '%20')})")

@bot.command()
async def yazitura(ctx, cevap: str):
    secilen = random.choice(["yazı", "tura"])
    if cevap.lower() == secilen:
        await ctx.send(f"Cevap **{secilen}** idi, kazandın helal lan türk")
    else:
        await ctx.send(f"Cevap **{secilen}** idi, mal kürt kazanamadın")

@bot.command()
async def secim(ctx, option1, option2):
    is_yasakli = False
    for kelime in yasaklilar:
        if kelime in option1 or kelime in option2:
            is_yasakli = True
            break

    if is_yasakli:
        await ctx.send("yarak yala")
    else:
        secilen = random.choice([option1, option2])
        await ctx.send(f"bu seciöm cıktıa : {secilen}")

@bot.command(aliases=["sole"])
async def say(ctx,soylenecek_sey):
    is_yasakli = False
    for i in yasaklilar:
        if i in soylenecek_sey:
            is_yasakli = True
            break
    
    if is_yasakli == True:
        await ctx.send("yarraaaaaaaamı yala laaa")
    elif is_yasakli == False:
        await ctx.message.delete()
        await ctx.send(soylenecek_sey)

@bot.command(aliases=["base64","beyz"])
async def base(ctx,option,*,mesaj):
    if option in ["encode","e"]:
        encoded = base64.b64encode(mesaj.encode()).decode()
        await ctx.send(f"{mesaj} --> {encoded}")
    elif option in ["decode","d"]:
        decoded = base64.b64decode(mesaj).decode()
        await ctx.send(f"{mesaj} --> {decoded}")
        

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


async def draw_lottery(ctx):
    """Loto çekilişini yapan ve kazananı anons eden fonksiyon."""
    global lottery_data, dicks
    participants = lottery_data.get("participants", {})
    if not participants:
        return

    winner_id = random.choice(list(participants.keys()))
    total_pot = sum(participants.values())

    try:
        winner_user = await bot.fetch_user(int(winner_id))
        mention = winner_user.mention
    except discord.NotFound:
        mention = f"Bilinmeyen Kullanıcı ({winner_id})"

    dicks[winner_id] = dicks.get(winner_id, 0) + total_pot
    save_json("dicks.json", dicks)

    await ctx.send(f"🎉 **allah yoksunu lodıri sona erdi** 🎉\n6 saat gecti aminyum ve kazanan: {mention}! helal olsun valla, lodirideki **{total_pot} cm**'i kazandın hll")

    lottery_data = {}
    save_json("lottery.json", lottery_data)

@bot.command(aliases=["pipi", "Pipi", "PİPİ", "Sik", "SİK", "cuk", "Cuk", "CUK"])
async def sik(ctx, *args):
    import os, json, random, time
    global dicks, cooldowns, lottery_data

    user_id = str(ctx.author.id)

    if not args:
        await ctx.send("https://tenor.com/view/rock-one-eyebrow-raised-rock-staring-the-rock-gif-22113367")
        return

    option = args[0].lower()
    amount = args[1] if len(args) > 1 else None

    # LOTO zaman kontrolü
    if "end_time" in lottery_data and time.time() > lottery_data["end_time"]:
        print("[DEBUG] Loto süresi doldu, çekiliş yapılıyor.")
        await draw_lottery(ctx)
        return

    # GIVE KOMUTU
    if option == "give":
        if not ctx.message.mentions or amount is None:
            await ctx.send("kime ne kadar vercen amk düzgün yaz: `!sik give <miktar> @kullanıcı`")
            return

        try:
            miktar = int(amount)
            if miktar <= 0:
                await ctx.send("0 veya negatif veremezsin be kürd")
                return
        except ValueError:
            await ctx.send("sayı giricen kanka `!sik give <miktar> @kullanıcı` örnek.")
            return

        hedef_kisi = ctx.message.mentions[0]
        hedef_id = str(hedef_kisi.id)
        veren_id = user_id

        veren_cm = dicks.get(veren_id, 0)
        if veren_cm < miktar:
            await ctx.send(f"{ctx.author.mention}, o kadar sikin yok mk! sende sadece {veren_cm} cm var.")
            return

        dicks[veren_id] = veren_cm - miktar
        dicks[hedef_id] = dicks.get(hedef_id, 0) + miktar

        with open("dicks.json", "w") as f:
            json.dump(dicks, f, indent=4)

        await ctx.send(f"{ctx.author.mention}, {hedef_kisi.mention} kişisine **{miktar} cm** verdi. hll lan sana mal kopek")
        return

    if option == "fight":
        if not ctx.message.mentions or amount is None:
            await ctx.send("kime meydan okuduğunu ve ne kadar cm bahis koyduğunu yaz: `!sik fight @kullanici <miktar>`")
            return

        try:
            miktar = int(amount)
            if miktar <= 0:
                await ctx.send("bahis negatif olamaz aq")
                return
        except ValueError:
            await ctx.send("bahis miktarına sayı gir gral")
            return

        hedef = ctx.message.mentions[0]
        hedef_id = str(hedef.id)
        user_id = str(ctx.author.id)

        if user_id == hedef_id:
            await ctx.send("kendi sikinle savaşamazsın koçum")
            return

        # 🔒 aynı anda iki dövüşe girmeyi engelle
        if user_id in active_fights or hedef_id in active_fights:
            await ctx.send("Sen veya rakibin zaten başka bir dövüşte. Önce o bitsin.")
            return

        user_cm = dicks.get(user_id, 0)
        hedef_cm = dicks.get(hedef_id, 0)

        if user_cm < miktar or hedef_cm < miktar:
            await ctx.send(f"her iki tarafın da en az {miktar} cm sik olması lazım. {ctx.author.mention}: {user_cm} cm, {hedef.mention}: {hedef_cm} cm")
            return

        class FightButtons(discord.ui.View):
            def __init__(self, timeout=60):
                super().__init__(timeout=timeout)
                self.response = None

            @discord.ui.button(label="Kabul Et", style=discord.ButtonStyle.green)
            async def kabul(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != hedef.id:
                    await interaction.response.send_message("Sen karışma amk", ephemeral=True)
                    return
                self.response = "kabul"
                await interaction.response.edit_message(content=f"{hedef.mention} dövüşü kabul etti! Savaş başlıyor...", view=None)
                self.stop()

            @discord.ui.button(label="Reddet", style=discord.ButtonStyle.red)
            async def reddet(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != hedef.id:
                    await interaction.response.send_message("Sen karışma amk", ephemeral=True)
                    return
                self.response = "reddet"
                await interaction.response.edit_message(content=f"{hedef.mention} dövüşü reddetti. korkak", view=None)
                self.stop()

        # 🔒 Dövüşe ekle
        active_fights.add(user_id)
        active_fights.add(hedef_id)

        try:
            view = FightButtons()
            await ctx.send(f"🥊 {ctx.author.mention}, {hedef.mention} kişisine **{miktar} cm** bahisle dövüş teklif etti.", view=view)
            await view.wait()

            if view.response != "kabul":
                return  # Dövüş iptal edildi

            # %50-%50 adil savaş
            kazanan_id = random.choice([user_id, hedef_id])
            kaybeden_id = hedef_id if kazanan_id == user_id else user_id

            kazanan_user = ctx.author if kazanan_id == user_id else hedef
            kaybeden_user = hedef if kazanan_id == user_id else ctx.author

            dicks[kazanan_id] = dicks.get(kazanan_id, 0) + miktar
            dicks[kaybeden_id] = max(0, dicks.get(kaybeden_id, 0) - miktar)

            save_json("dicks.json", dicks)

            await ctx.send(f"💥 **SİK DÖVÜŞÜ!** 💥\n"
                        f"{ctx.author.mention} vs {hedef.mention} – bahis: **{miktar} cm**\n\n"
                        f"🏆 **Kazanan:** {kazanan_user.mention} (+{miktar} cm)\n"
                        f"💀 **Kaybeden:** {kaybeden_user.mention} (-{miktar} cm)")

        finally:
            # 🔓 Dövüş bitince temizle
            active_fights.discard(user_id)
            active_fights.discard(hedef_id)

        return

    if not args:
        await ctx.send("https://tenor.com/view/rock-one-eyebrow-raised-rock-staring-the-rock-gif-22113367")
        return

    option = args[0].lower()

    # LOTO zaman kontrolü
    if "end_time" in lottery_data and time.time() > lottery_data["end_time"]:
        print("[DEBUG] Loto süresi doldu, çekiliş yapılıyor.")
        await draw_lottery(ctx)
        # Bu return önemli, yoksa loto bittikten sonra komut devam etmeye çalışır
        if option == "lottery": return

    # LOTTERY
    if option in ["lottery", "lodıri"]:
        participants = lottery_data.get("participants", {})

        if amount is not None:
            try:
                amount_int = int(amount)
                if amount_int <= 0:
                    await ctx.send("mal kürd en az 20cm ile katılabiliyon")
                    return
            except ValueError:
                await ctx.send("sayı gir amk cahili sana integer ile stringi ayrıstırmayı ogretmedilermi")
                return

            if user_id in participants:
                await ctx.send("zaten katıldın beklicen")
                return

            user_cm = dicks.get(user_id, 0)
            if amount_int < 20:
                await ctx.send(f"{ctx.author.mention}, katılmak icin 20cm girmne lazım en az allahın malı. sende sadece {user_cm}cm var.")
                return

            if user_cm < amount_int:
                await ctx.send(f"{ctx.author.mention}, o kadar cmin yok puhaha allan arabı sende sadece {user_cm}cm var")
                return

            if not participants:
                lottery_data["end_time"] = time.time() + (6 * 60 * 60)
                lottery_data["participants"] = {}
                await ctx.send("🎉 **lodıri basladı genclerr** 6 saatte bidcek")

            dicks[user_id] -= amount_int
            lottery_data["participants"][user_id] = lottery_data["participants"].get(user_id, 0) + amount_int
            save_json("dicks.json", dicks)
            save_json("lottery.json", lottery_data)

            time_left = lottery_data["end_time"] - time.time()
            hours, rem = divmod(time_left, 3600)
            minutes, _ = divmod(rem, 60)
            await ctx.send(f"{ctx.author.mention}, **{amount_int} cm** ile lodıriye gatıldın, gud lak amınogli! 🍀\n bitmesine **{int(hours)} saat {int(minutes)} dakika** var.")
        else:
            if not participants:
                await ctx.send("**lodıri!!11!**\n> suan lodırı yok\n> `!sik lottery <miktar>` yaz baslat gral.")
                return

            total_pot = sum(participants.values())
            time_left = lottery_data["end_time"] - time.time()
            hours, rem = divmod(time_left, 3600)
            minutes, _ = divmod(rem, 60)
            await ctx.send(f"**lodıri!!11!**\n> lodiride **{len(participants)}** kişi var.\n> doplam ödül: **{total_pot} cm** 💰\n> bitmesine: **~{int(hours)} saat {int(minutes)} dakika**.")
        return

    if option in ["buyult", "kaldir", "kaldır"]:
        now = time.time()
        cooldown_time = 7200
        last_time = cooldowns.get(user_id, 0)

        if now - last_time < cooldown_time:
            kalan = int(cooldown_time - (now - last_time))
            saat = int(kalan / 3600)
            dakika = int((kalan % 3600) / 60)
            user = ctx.author.mention

            if saat >= 1:
                await ctx.send(f"{user}, sikini {saat} saat {dakika} dakika sonra buyultebilcen gral.")
            else:
                await ctx.send(f"{user}, sikini {dakika} dakika sonra buyultebilcen gral.")
            return

        cooldowns[user_id] = now
        with open("cooldowns.json", "w") as f:
            json.dump(cooldowns, f, indent=4)

        secilen_buyume = random.randint(1, 12)
        boy = dicks.get(user_id, 0) + secilen_buyume
        dicks[user_id] = boy

        with open("dicks.json", "w") as f:
            json.dump(dicks, f, indent=4)

        await ctx.send(f"{ctx.author.mention}, sikinin boyu {secilen_buyume} cm arttı! toplam boyun: {boy} cm 🍆")
        return

    if option == "kaccm":
        boy = dicks.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention}, sikiniz tam olarak {boy} cm!")
        return

    if option == "top":
        if not dicks:
            await ctx.send("kimsenin siki yok yani siksiz world")
            return

        sirali = sorted(dicks.items(), key=lambda x: x[1], reverse=True)

        mesaj = ""
        for i, (uid, boy) in enumerate(sirali, start=1):
            uid = int(uid)
            user = ctx.guild.get_member(uid)
            if not user:
                try:
                    user = await ctx.guild.fetch_member(uid)
                except:
                    user = None

            isim = user.display_name if user else f"User ID: {uid}"
            mesaj += f"{i}. **{isim} – {boy} cm**\n"

            if len(mesaj) > 1900:
                mesaj += "\n...ve devamı var."
                break

        embed = discord.Embed(
            title="> **sarvarun en büyük siklileri:** 🍆",
            description=mesaj,
            color=discord.Color.dark_gold()
        )

        await ctx.send(embed=embed)
        return

    if option == "daily":
        now = time.time()
        cooldown_time = 86400
        last_time = cooldowns.get(user_id + "_daily", 0)

        if now - last_time < cooldown_time:
            kalan = int(cooldown_time - (now - last_time))
            saat = kalan // 3600
            dakika = (kalan % 3600) // 60
            await ctx.send(f"{ctx.author.mention}, daily için {saat} saat {dakika} dakika beklicen gral.")
            return

        cooldowns[user_id + "_daily"] = now
        with open("cooldowns.json", "w") as f:
            json.dump(cooldowns, f, indent=4)

        buyume = random.randint(20, 40)
        boy = dicks.get(user_id, 0) + buyume
        dicks[user_id] = boy

        with open("dicks.json", "w") as f:
            json.dump(dicks, f, indent=4)

        await ctx.send(f"{ctx.author.mention}, sikin artık daha buyuk! today **+{buyume} cm** buyudu hll. toplam: **{boy} cm** 🍆")
        return

    if option in ["superbuyult", "superkaldir", "superkaldır"]:
        now = time.time()
        cooldown_time = 3600
        last_time = cooldowns.get(user_id + "_super", 0)

        if now - last_time < cooldown_time:
            kalan = int(cooldown_time - (now - last_time))
            dakika = int((kalan % 3600) / 60)
            saniye = int(kalan % 60)
            await ctx.send(f"{ctx.author.mention}, süper büyütme için {dakika} dakika {saniye} saniye daha bekle gral.")
            return

        cooldowns[user_id + "_super"] = now
        with open("cooldowns.json", "w") as f:
            json.dump(cooldowns, f, indent=4)

        secilen_bk = random.randint(20, 40)
        sans = random.random()

        boy = dicks.get(user_id, 0)
        if sans <= 0.5:
            boy += secilen_bk
            sonuc = f"sanslı orospu cocu! 🍆\nsikin {secilen_bk} cm uzadı. toplam: {boy} cm!"
        else:
            boy -= secilen_bk
            boy = max(boy, 0)
            sonuc = f"allaaan malı haha! 😆\nsikin {secilen_bk} cm kısaldı. yeni boy: {boy} cm."

        dicks[user_id] = boy
        with open("dicks.json", "w") as f:
            json.dump(dicks, f, indent=4)

        await ctx.send(f"{ctx.author.mention}, {sonuc}")
        return

    # Geçersiz option kontrolü
    if option not in ["buyult", "superbuyult", "daily", "lottery", "kaccm", "top", "give"]:
        await ctx.send("seçenekler bunlar sadece: buyult / superbuyult / daily / lottery / kaccm / top / give")
        return

@bot.check
async def dm_check(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("AHHHH YARRAAAAAAAKKKKKKKKKKKK")
        return False  # Komut çalıştırılmaz
    return True  # Komut çalıştırılabilir

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention}, bu komutu tekrar kullanmak için {error.retry_after:.1f} saniye beklemelisin."
        )
    else:
        print(f"Bir hata oluştu: {error}")

if not os.path.exists("lottery.json"):
    with open("lottery.json", "w") as f: json.dump({}, f)
if not os.path.exists("dicks.json"):
    with open("dicks.json", "w") as f: json.dump({}, f)
if not os.path.exists("cooldowns.json"):
    with open("cooldowns.json", "w") as f: json.dump({}, f)

# Lütfen bot token'ını buraya kendin ekle
bot.run("yaraghımı yala")
