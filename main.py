import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Kullanıcıların oyun durumlarını saklamak için dictionary
games = {}

# Tahmin edilecek kelimeler listesi
WORDS = ["python", "telegram", "bilgisayar", "programlama", "kodlama", "yazilim", "robot"]

MAX_TRIES = 6  # Hakkı

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Kelime Bilmece Oyununa Hoş Geldin!\n"
        "Oyun başlatmak için: /oyun\n"
        "Tahmin yapmak için artık komut gerekmez, doğrudan harf veya kelime yazabilirsin."
    )

async def oyun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    word = random.choice(WORDS)
    display = ["_"] * len(word)
    
    games[user_id] = {
        "word": word,
        "display": display,
        "tries": MAX_TRIES,
        "guessed": []
    }
    
    await update.message.reply_text(
        f"✅ Yeni oyun başladı!\nKelime: {' '.join(display)}\nKalan hakkın: {MAX_TRIES}"
    )

async def tahmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    if user_id not in games:
        return  # Oyun başlamadıysa mesajı yok say

    game = games[user_id]

    # Kullanıcı kelimeyi tahmin ediyorsa
    if len(text) > 1:
        if text == game["word"]:
            await update.message.reply_text(f"🎉 Tebrikler! Kelimeyi doğru bildin: {game['word']}")
            del games[user_id]
        else:
            game["tries"] -= 1
            if game["tries"] <= 0:
                await update.message.reply_text(f"❌ Hakkın bitti! Kelime: {game['word']}")
                del games[user_id]
            else:
                await update.message.reply_text(f"Yanlış tahmin! Kalan hakkın: {game['tries']}")
        return

    # Kullanıcı harf tahmini yapıyorsa
    letter = text
    if letter in game["guessed"]:
        await update.message.reply_text("Bu harfi zaten tahmin ettin!")
        return

    game["guessed"].append(letter)

    if letter in game["word"]:
        for i, ch in enumerate(game["word"]):
            if ch == letter:
                game["display"][i] = letter
        if "_" not in game["display"]:
            await update.message.reply_text(f"🎉 Tebrikler! Kelimeyi tamamladın: {game['word']}")
            del games[user_id]
            return
        else:
            await update.message.reply_text(f"✅ Doğru harf! {' '.join(game['display'])}\nKalan hakkın: {game['tries']}")
    else:
        game["tries"] -= 1
        if game["tries"] <= 0:
            await update.message.reply_text(f"❌ Hakkın bitti! Kelime: {game['word']}")
            del games[user_id]
        else:
            await update.message.reply_text(f"Yanlış harf! {' '.join(game['display'])}\nKalan hakkın: {game['tries']}")

def main():
    app = Application.builder().token("8395382669:AAEOvfoHSrfrNC2nSBvofn6_UcS0LLeZdes").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oyun", oyun))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), tahmin))

    app.run_polling()

if __name__ == "__main__":
    main()
