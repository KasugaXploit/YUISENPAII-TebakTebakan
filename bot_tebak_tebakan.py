import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Soal Tebak Tebakan minimal 50, aku buat contoh 10 dulu ya, nanti bisa kamu tambah sendiri
tebak_tebakan_list = [
    {"soal": "Saya punya kaki tapi tidak bisa berjalan. Saya adalah...", "jawaban": ["kursi"]},
    {"soal": "Buah apa yang selalu membuat orang ketawa?", "jawaban": ["pisang"]},
    {"soal": "Apa yang selalu datang tapi tidak pernah tiba?", "jawaban": ["besok", "esok"]},
    {"soal": "Saya bulat dan selalu mengikuti kamu, tapi kamu tidak bisa menangkap saya. Saya adalah...", "jawaban": ["bayangan"]},
    {"soal": "Apa yang punya tangan tapi tidak bisa bertepuk?", "jawaban": ["jam", "jam dinding"]},
    {"soal": "Apa yang bisa terbang tanpa sayap?", "jawaban": ["waktu"]},
    {"soal": "Apa yang selalu di depan mata tapi tidak terlihat?", "jawaban": ["masa depan"]},
    {"soal": "Saya selalu basah saat mengeringkan sesuatu. Saya adalah...", "jawaban": ["handuk"]},
    {"soal": "Apa yang bisa pecah tapi tidak pernah jatuh?", "jawaban": ["fajar"]},
    {"soal": "Apa yang punya leher tapi tidak punya kepala?", "jawaban": ["botol"]},
    # Tambahkan sampai 50 soal ya nanti
]

jawaban_benar = [
    "Yosh! Jawabanmu benar! 🎉",
    "Mantap! Kamu pinter banget! ✅",
    "Benar sekali! Lanjutkan! 💯",
    "Oke, itu jawaban yang tepat! 👍",
    "Sip! Kamu menang! 🏆",
]

jawaban_salah = [
    "Wah, salah deh coba lagi ya 😅",
    "Ups, itu belum tepat. Coba lagi dong!",
    "Hmm, jawabanmu kurang pas nih.",
    "Nggak bener, coba pikir lagi!",
    "Ayo semangat, jangan nyerah! 💪",
]

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hai! Aku YUI SENPAII.\n"
        "Kamu bisa main tebak-tebakan dengan perintah /tebak\n"
        "Ketik jawabanmu setelah soal muncul ya!"
    )

async def tebak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    soal = random.choice(tebak_tebakan_list)
    user_state[update.effective_user.id] = {
        "mode": "tebak",
        "jawaban": [j.lower() for j in soal["jawaban"]]
    }
    await update.message.reply_text(f"Tebak Tebakan:\n{soal['soal']}")

async def jawab_tebak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_state and user_state[user_id]["mode"] == "tebak":
        jawaban = user_state[user_id]["jawaban"]
        user_jawab = update.message.text.lower().strip()
        if user_jawab in jawaban:
            await update.message.reply_text(random.choice(jawaban_benar))
            del user_state[user_id]
        else:
            await update.message.reply_text(random.choice(jawaban_salah))
    else:
        await update.message.reply_text("Ketik /tebak dulu buat mulai tebak-tebakan!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tebak", tebak))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), jawab_tebak))

    print("Bot YUI SENPAII - Tebak Tebakan sedang berjalan...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
