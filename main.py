from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

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
    updater = Updater("TELETOKEN")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name_handler)],
            PRICE: [MessageHandler(Filters.text & ~Filters.command, price_handler)],
            LINK: [MessageHandler(Filters.text & ~Filters.command, link_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
