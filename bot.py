import telebot
import os
from telebot import types

# O'zingizning BOT TOKENingizni shu yerga yozing:
BOT_TOKEN = '7808954491:AAE7vqeM4esMKv2S6SLhdsDyG-i-20FOMjQ'
bot = telebot.TeleBot(BOT_TOKEN)

# Tekshiriladigan Telegram kanal
channels = ['@MuXa_pro_uzakaunt']

def check_sub(user_id):
    for ch in channels:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status == 'left':
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not check_sub(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Telegram kanalga a'zo bo'lish (1)", url="https://t.me/MuXa_pro_uzakaunt"))
        markup.add(types.InlineKeyboardButton("Instagram kanalga a'zo bo'lish (1)", url="https://www.instagram.com/tarjima_kinolar02"))
        markup.add(types.InlineKeyboardButton("Instagram kanalga a'zo bo'lish (1)", url="https://www.instagram.com/1slomov_030"))
        markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check"))
        
        text = (
            "❌ Botdan foydalanish uchun quyidagi Telegram kanalga a'zo bo'lishingiz shart:\n\n"
            "🔗 @MuXa_pro_uzakaunt\n\n"
            "📢 Instagram sahifalarimizga ham obuna bo‘ling (ixtiyoriy):\n"
            "1. https://www.instagram.com/tarjima_kinolar02\n"
            "2. https://www.instagram.com/1slomov_030"
        )
        bot.send_message(user_id, text, reply_markup=markup)
    else:
        bot.send_message(user_id, "✅ Xush kelibsiz! Siz botdan foydalanishingiz mumkin.")

@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id
    if check_sub(user_id):
        bot.send_message(user_id, "✅ Rahmat! Endi botdan foydalanishingiz mumkin.")
    else:
        bot.send_message(user_id, "❗ Siz hali ham Telegram kanalga a'zo bo‘lmagansiz.")



# 🔢 Kod va fayl nomlari lug‘ati
kino_dict = {
    "1": "kino1.mp4",
    "2": "kino2.mp4",
    "3": "kino3.mp4"
}

# 📩 Foydalanuvchi xabar yuborganda
@bot.message_handler(func=lambda message: message.text.isdigit())
def yubor_kino(message):
    kod = message.text.strip()
    
    if kod in kino_dict:
        fayl_nomi = kino_dict[kod]
        if os.path.exists(fayl_nomi):
            try:
                with open(fayl_nomi, 'rb') as video:
                    bot.send_chat_action(message.chat.id, 'upload_video')
                    bot.send_video(message.chat.id, video)
            except Exception as e:
                bot.send_message(message.chat.id, f"⚠️ Fayl yuborishda xatolik: {str(e)}")
        else:
            bot.send_message(message.chat.id, f"❌ Fayl topilmadi: {fayl_nomi}")
    else:
        bot.send_message(message.chat.id, "❌ Bunday kino mavjud emas. To‘g‘ri raqam yuboring (masalan: 1 yoki 2)")

# 📩 Agar foydalanuvchi raqam emas narsa yuborsa
@bot.message_handler(func=lambda message: not message.text.isdigit())
def notogri_kiritish(message):
    bot.send_message(message.chat.id, "📌 Iltimos, faqat kino raqamini kiriting (masalan: 1 yoki 2)")

 bot.infinity_polling()