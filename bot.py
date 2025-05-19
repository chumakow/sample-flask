from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

tg_api = TGBOT_API_KEY

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

app = ApplicationBuilder().token(tg_api).build()

app.add_handler(CommandHandler("start", hello))

app.run_polling()
print("Our bot is running")