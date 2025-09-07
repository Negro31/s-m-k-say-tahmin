from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot çalışıyor!")

def main():
    app = Application.builder().token("8443063681:AAEMtw5dAb-EvgpZaBQYppN1Y2v9Co1qZLM").build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()  # v21'de de aynı

if __name__ == "__main__":
    main()
