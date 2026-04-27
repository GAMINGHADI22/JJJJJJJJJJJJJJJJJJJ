import os
import asyncio
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8566117526:AAHgkoF74JChfn9LFYiwd32LZrhKPD9OW3Q", "8566117526:AAHgkoF74JChfn9LFYiwd32LZrhKPD9OW3Q")

FAST_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "concurrent_fragment_downloads": 16,
    "retries": 10,
    "fragment_retries": 10,
    "socket_timeout": 20,
}

# 💜 START WITH ANIMATION
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⚡ Initializing bot...")

    texts = [
        "⚡ Initializing bot.",
        "⚡ Initializing bot..",
        "⚡ Initializing bot...",
        "💜 Loading interface...",
        "💜 Almost ready..."
    ]

    for t in texts:
        await asyncio.sleep(0.5)
        await msg.edit_text(t)

    await asyncio.sleep(0.5)
    await msg.edit_text(
        "╔══════════════════════════════╗\n"
        "║ 💜✨⚡ 𝗔𝗗𝗠𝗜𝗡 𝗥𝗔𝗛𝗠𝗔𝗡 𝗕𝗢𝗧 ⚡✨💜 ║\n"
        "╠══════════════════════════════╣\n"
        "║ 🌌 𝗡𝗘𝗢𝗡 𝗩𝗜𝗗𝗘𝗢 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗘𝗥      ║\n"
        "║ 🎬 YouTube • TikTok Supported ║\n"
        "║ 🎧 MP3 Audio • HD Quality     ║\n"
        "║ 🚀 Ultra Fast Engine Active   ║\n"
        "║ 🔮 Status: ONLINE • READY     ║\n"
        "╚══════════════════════════════╝\n\n"
        "💎 Smart Bot Ready!\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📎 Send your video link now 👇"
    )

# 🔍 LINK HANDLER (WITH PREVIEW)
async def link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not ("youtube.com" in url or "youtu.be" in url or "tiktok.com" in url):
        await update.message.reply_text("❌ Valid YouTube/TikTok link পাঠাও")
        return

    context.user_data["url"] = url

    loading = await update.message.reply_text("🔍 Scanning link...")
    await loading.edit_text("🔍 Scanning link.")
    await loading.edit_text("🔍 Scanning link..")
    await loading.edit_text("🔍 Scanning link...")

    try:
        with yt_dlp.YoutubeDL(FAST_OPTS) as ydl:
            data = ydl.extract_info(url, download=False)

        title = data.get("title", "Unknown Title")
        duration = data.get("duration", 0)
        thumbnail = data.get("thumbnail")

        minutes = duration // 60
        seconds = duration % 60

        buttons = [
            [
                InlineKeyboardButton("💎 1080p", callback_data="1080"),
                InlineKeyboardButton("⚡ 720p", callback_data="720")
            ],
            [
                InlineKeyboardButton("📱 360p", callback_data="360"),
                InlineKeyboardButton("🎧 MP3", callback_data="mp3")
            ]
        ]

        caption = (
            "╭━━━〔 💜 VIDEO PREVIEW 💜 〕━━━╮\n"
            f"🎬 {title[:40]}\n"
            f"⏱ {minutes}:{seconds:02d}\n\n"
            "⚡ Choose your format 👇"
        )

        await loading.delete()

        if thumbnail:
            await update.message.reply_photo(
                photo=thumbnail,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await update.message.reply_text(
                caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    except Exception as e:
        await loading.edit_text("❌ Preview load failed")

# ⚙️ DOWNLOAD HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    url = context.user_data.get("url")
    choice = q.data

    msg = await q.message.reply_text(
        "🚀 Processing...\n⏳ Please wait..."
    )

    try:
        os.makedirs("downloads", exist_ok=True)

        base_opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "noplaylist": True,
            **FAST_OPTS
        }

        if choice == "mp3":
            ydl_opts = {
                **base_opts,
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }],
            }
        elif choice == "1080":
            ydl_opts = {**base_opts, "format": "bestvideo[height<=1080]+bestaudio/best"}
        elif choice == "720":
            ydl_opts = {**base_opts, "format": "bestvideo[height<=720]+bestaudio/best"}
        else:
            ydl_opts = {**base_opts, "format": "bestvideo[height<=360]+bestaudio/best"}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(data)

        await msg.edit_text("📤 Sending file...")

        if choice == "mp3":
            file_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")
            with open(file_path, "rb") as f:
                await q.message.reply_audio(audio=f)
        else:
            with open(file_path, "rb") as f:
                await q.message.reply_video(video=f)

        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ Download failed")

# 🚀 RUN
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
