import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Kullanıcıların oyun verilerini saklamak için dict
games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Sayı Tahmin Oyununa Hoş Geldin!\n"
        "Ben 1 ile 100 arasında bir sayı tuttum.\n"
        "Tahmin etmek için: /guess <sayı>\n"
        "Yeni oyun başlatmak için: /newgame"
    )
    await newgame(update, context)

async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    games[user_id] = random.randint(1, 100)
    await update.message.reply_text("✅ Yeni oyun başladı! 1 ile 100 arasında bir sayı tuttum, tahmin et!")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in games:
        await update.message.reply_text("Önce /newgame yazarak oyun başlatmalısın 🎮")
        return

    if not context.args:
        await update.message.reply_text("Kullanım: /guess <sayı>")
        return

    try:
        tahmin = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Lütfen bir sayı gir.")
        return

    hedef = games[user_id]

    if tahmin < hedef:
        await update.message.reply_text("🔻 Daha büyük bir sayı dene!")
    elif tahmin > hedef:
        await update.message.reply_text("🔺 Daha küçük bir sayı dene!")
    else:
        await update.message.reply_text("🎉 Tebrikler! Doğru bildin 🎉\nYeni oyun için: /newgame")
        del games[user_id]

def main():
    # Buraya BotFather’dan aldığın bot tokenini gir
    app = Application.builder().token("BOT_TOKENIN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newgame", newgame))
    app.add_handler(CommandHandler("guess", guess))

    app.run_polling()

if __name__ == "__main__":
    main()
