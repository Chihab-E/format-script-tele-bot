import os
from dotenv import load_dotenv
import telebot

load_dotenv()  

bot_token = os.getenv('TELETOKEN')

bot = telebot.TeleBot(bot_token)

def create_promo_message():
    product_name = input("Enter the name of the product: ")
    price = input("Enter the price: ")
    link = input("Enter the link: ")

    message = f"""
🛍 تخفيـــض لـ : "{product_name}"

💵 السعر : "{price}"$ ☄️☄️⚡️

📍 رابط العملات: 💥💥
{link}
"""

    return message

@bot.message_handler(commands=['send'])
def send_promo(message):
    promo_message = create_promo_message()
    bot.send_message(message.chat.id, promo_message)

bot.infinity_polling()
