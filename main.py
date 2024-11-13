import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

NAME, PRICE, LINK = range(3)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Welcome! Please enter the name of the product:")
    return NAME

def name_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['product_name'] = update.message.text
    update.message.reply_text("Got it! Now, enter the price:")
    return PRICE

def price_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['price'] = update.message.text
    update.message.reply_text("Thanks! Finally, enter the link:")
    return LINK

def link_handler(update: Update, context: CallbackContext) -> int:
    product_name = context.user_data['product_name']
    price = context.user_data['price']
    link = update.message.text
    
    message = f"""
🛍 تخفيـــض لـ : "{product_name}"

💵 السعر : "{price}"$ ☄️☄️⚡️

📍 رابط العملات: 💥💥
{link}
"""
    update.message.reply_text(message)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Canceled.")
    return ConversationHandler.END

def main():
    token = os.getenv("TELETOKEN")
    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_handler)],
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == '__main__':
    main()
