# telegram bot: admin panel, kino qo'shish, majburiy obuna boshqaruv

import telebot
from telebot import types

BOT_TOKEN = '7808954491:AAE7vqeM4esMKv2S6SLhdsDyG-i-20FOMjQ'
bot = telebot.TeleBot(BOT_TOKEN)

admin_ids = [1225264753]  # bu yerga adminlar ID sini yozing
channels = ['@MuXa_pro_uzakaunt']  # majburiy obuna kanallar ro'yxati
kino_dict = {}  # kinolar ro'yxati {"1": "file_id", ...}

# === Obuna tekshiruv ===
def check_sub(user_id):
    for ch in channels:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status == 'left':
                return False
        except:
            return False
    return True

# === START ===
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not check_sub(user_id):
        markup = types.InlineKeyboardMarkup()
        for ch in channels:
            markup.add(types.InlineKeyboardButton(f"Obuna bo'lish: {ch}", url=f"https://t.me/{ch[1:]}") )
        markup.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check"))
        bot.send_message(user_id, "📌 Iltimos, quyidagi kanallarga obuna bo'ling va tekshiring.", reply_markup=markup)
    else:
        bot.send_message(user_id, "✅ Xush kelibsiz! Kino raqamini yuboring.")

@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id
    if check_sub(user_id):
        bot.send_message(user_id, "✅ Obuna tasdiqlandi! Kino raqamini yuboring.")
    else:
        bot.send_message(user_id, "❌ Siz hali ham obuna bo‘lmagansiz!")

# === Kino yuborish ===
@bot.message_handler(func=lambda message: message.text.isdigit())
def yubor_kino(message):
    kod = message.text.strip()
    if kod in kino_dict:
        file_id = kino_dict[kod]
        try:
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.send_video(message.chat.id, file_id)
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Fayl yuborishda xatolik: {str(e)}")
    else:
        bot.send_message(message.chat.id, "❌ Bunday kino mavjud emas. To‘g‘ri raqam yuboring (masalan: 1 yoki 2)")

# === Raqam emas kiritilsa ===
@bot.message_handler(func=lambda message: not message.text.isdigit())
def notogri_kiritish(message):
    bot.send_message(message.chat.id, "📌 Iltimos, faqat kino raqamini kiriting (masalan: 1 yoki 2)")

# === Admin kino qo‘shishi ===
@bot.message_handler(content_types=['video'])
def qoshish_video(message):
    if message.from_user.id in admin_ids:
        bot.send_message(message.chat.id, "✅ Video qabul qilindi. Endi unga raqam belgilang (masalan: 4)")
        bot.register_next_step_handler(message, lambda msg: saqlash_video(msg, message.video.file_id))
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")

def saqlash_video(message, file_id):
    kod = message.text.strip()
    if kod.isdigit():
        kino_dict[kod] = file_id
        bot.send_message(message.chat.id, f"✅ Kino {kod}-raqam bilan saqlandi.")
    else:
        bot.send_message(message.chat.id, "❌ Iltimos, faqat raqam kiriting.")

bot.infinity_polling()
