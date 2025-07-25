import os
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)
from aliexpress_api import AliexpressApi, models

load_dotenv()

API_KEY = os.getenv("ALIEXPRESS_API_KEY")
API_SECRET = os.getenv("ALIEXPRESS_API_SECRET")
TRACKING_ID = os.getenv("ALIEXPRESS_TRACKING_ID", "default")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

aliexpress = AliexpressApi(API_KEY, API_SECRET, models.Language.EN, models.Currency.USD, TRACKING_ID)

def extract_product_id(text):
    m = re.search(r'/item/(\d+)\.html', text)
    return m.group(1) if m else None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if not text:
        await update.message.reply_text("Please send a valid AliExpress product URL or ID")
        return
    
    try:
        res = aliexpress.get_affiliate_links(text)
        if res and len(res) > 0:
            link = res[0].promotion_link
            await update.message.reply_text(f"🔗 Here's your affiliate link:\n{link}")
        else:
            await update.message.reply_text("❌ No affiliate link was generated")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
