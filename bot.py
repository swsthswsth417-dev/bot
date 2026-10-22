import telebot, re, time, json, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
MAIN_ADMIN = 8836904278
MY_NUMBER = "01031949696"
CHANNEL = "@shmaopoj"
ESBAT_LINK = "https://t.me/shmaopoj"

bot = telebot.TeleBot(TOKEN, threaded=False)
banned = set()
ADMINS_FILE = "admins.json"

def load_admins():
    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, "r") as f:
                return set(json.load(f))
        except: pass
    return {MAIN_ADMIN}

def save_admins():
    with open(ADMINS_FILE, "w") as f:
        json.dump(list(ADMINS), f)

ADMINS = load_admins()
def is_admin(uid): return uid in ADMINS

def main_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📦 طلب الاشتراك", callback_data="order"),
        InlineKeyboardButton("📹 حجز فيديوكول مع مدام مريم", callback_data="video_call"),
        InlineKeyboardButton("✅ اثباتاتي", url=ESBAT_LINK)
    )
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    if is_admin(m.chat.id):
        bot.send_message(m.chat.id, f"وضع الادمن ✅\n/ban /unban /r /post /addadmin /deladmin /admins")
    else:
        if m.chat.id in banned: return
        bot.send_message(m.chat.id, "مرحب بيك ⭐\nاختار من تحت 👇", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def all_callbacks(c):
    name = c.from_user.first_name or "صديقي"
    user_display = f"@{c.from_user.username}" if c.from_user.username else f"{name} (معندوش يوزر)"
    if c.data == "order":
        bot.send_message(c.message.chat.id, f"تمام يا {name} حول 50 جنيه على {MY_NUMBER} وهات اسكرين ✅\nالرقم: {MY_NUMBER}")
        for aid in ADMINS: bot.send_message(aid, f"🔔 طلب اشتراك\nID: {c.from_user.id}\n{user_display}")
    elif c.data == "video_call":
        bot.send_message(c.message.chat.id, f"للحجز فيديو كول مع مدام مريم حول 10 جنيه رسوم الاشتراك على فودافون كاش {MY_NUMBER} وبعت اسكرين هنا ✅\nالرقم: {MY_NUMBER}")
        for aid in ADMINS: bot.send_message(aid, f"📹 حجز فيديوكول\nID: {c.from_user.id}\n{user_display}")
    bot.answer_callback_query(c.id)

@bot.message_handler(commands=['ban','unban','r','post','addadmin','deladmin','admins'])
def admin_cmds(m):
    if not is_admin(m.chat.id): return
    text = m.text.strip(); parts = text.split()
    if text.startswith("/ban"):
        banned.add(int(parts[1])); bot.send_message(m.chat.id, "حظرت ✅")
    elif text.startswith("/unban"):
        banned.discard(int(parts[1])); bot.send_message(m.chat.id, "فكيت ✅")
    elif text.startswith("/addadmin"):
        ADMINS.add(int(parts[1])); save_admins(); bot.send_message(m.chat.id, f"ضفت ادمن {parts[1]} ✅")
    elif text.startswith("/deladmin"):
        if int(parts[1]) == MAIN_ADMIN: return
        ADMINS.discard(int(parts[1])); save_admins(); bot.send_message(m.chat.id, "حذفت ✅")
    elif text.startswith("/admins"):
        bot.send_message(m.chat.id, "\n".join([str(x) for x in ADMINS]))
    elif text.startswith("/r"):
        uid = int(parts[1]); msg = text.split(maxsplit=2)[2]
        bot.send_message(uid, msg); bot.send_message(m.chat.id, "بعت ✅")
    elif text.startswith("/post"):
        bot.send_message(CHANNEL, text.replace("/post","").strip()); bot.send_message(m.chat.id, "نزل ✅")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    if is_admin(m.chat.id) and m.reply_to_message:
        s = re.search(r"ID: (\d+)", m.reply_to_message.text or "")
        if s: bot.send_message(int(s.group(1)), m.text); return
    if not is_admin(m.chat.id) and m.text:
        if m.chat.id in banned: return
        user_display = f"@{m.from_user.username}" if m.from_user.username else f"{m.from_user.first_name}"
        for aid in ADMINS: bot.send_message(aid, f"ID: {m.chat.id}\n{user_display}\n\n{m.text}")

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except: time.sleep(5)
