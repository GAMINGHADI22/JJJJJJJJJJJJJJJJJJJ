import os, time
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8566117526:AAHgkoF74JChfn9LFYiwd32LZrhKPD9OW3Q", "8566117526:AAHgkoF74JChfn9LFYiwd32LZrhKPD9OW3Q")
ADMIN = "@ABDUR9X"

premium_users = {}  # user_id : expiry_timestamp

# 🕒 CHECK PREMIUM
def is_premium(user_id):
    if user_id in premium_users:
        if time.time() < premium_users[user_id]:
            return True
        else:
            del premium_users[user_id]
    return False

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💜⚡ ADMIN RAHMAN 𝗕𝗢𝗧 ⚡💜\n\n"
        "🎬 Downloader Bot\n"
        "👉 Premium: /premium\n"
        "📎 Send link"
    )

# 👑 PREMIUM INFO
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(
        "👑 PREMIUM PLAN\n\n"
        "💎 1080p + 720p Unlock\n"
        "⚡ Fast Download\n\n"
        "💰 Price: 100৳ / 30 Days\n\n"
        "📱 Payment:\n"
        "bKash/Nagad: 01XXXXXXXXX\n\n"
        f"🆔 ID: {uid}\n\n"
        "📸 Payment screenshot পাঠাও\n"
        "Admin: @ABDUR9X"
    )

# 🆔 MY ID
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 {update.effective_user.id}")

# 👑 ADD PREMIUM (30 days)
async def addpremium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN:
        return

    try:
        uid = int(context.args[0])
        premium_users[uid] = time.time() + (30 * 24 * 60 * 60)
        await update.message.reply_text("✅ Premium added (30 days)")
    except:
        await update.message.reply_text("❌ Error")

# ❌ REMOVE
async def removepremium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN:
        return

    try:
        uid = int(context.args[0])
        premium_users.pop(uid, None)
        await update.message.reply_text("❌ Removed")
    except:
        pass

# 🔍 LINK
async def link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    context.user_data["url"] = url

    buttons = [
        [InlineKeyboardButton("💜 1080p", callback_data="1080")],
        [InlineKeyboardButton("⚡ 720p", callback_data="720")],
        [InlineKeyboardButton("📱 360p", callback_data="360")],
        [InlineKeyboardButton("🎧 MP3", callback_data="mp3")]
    ]

    await update.message.reply_text(
        "💜 Select quality",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ⚙️ DOWNLOAD
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    choice = q.data
    url = context.user_data.get("url")

    # 🔒 PREMIUM LOCK
    if choice in ["1080","720"] and not is_premium(uid):
        await q.message.reply_text(
            "👑 Premium Required\nUse /premium"
        )
        return

    msg = await q.message.reply_text("⏳ Downloading...")

    try:
        ydl_opts = {"format": "best"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(data)

        with open(file, "rb") as f:
            if choice == "mp3":
                await q.message.reply_audio(f)
            else:
                await q.message.reply_video(f)

        os.remove(file)
        await msg.delete()

    except:
        await msg.edit_text("❌ Failed")

# 🚀 RUN
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("addpremium", addpremium))
    app.add_handler(CommandHandler("removepremium", removepremium))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
