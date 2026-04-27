import os
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "╔═══════◇◆◇═══════╗\n"
        "   💜 ADMIN RAHMAN BOT\n"
        "╚═══════◇◆◇═══════╝\n\n"
        "🎬 YouTube + TikTok Downloader\n"
        "🎧 MP3 Audio Supported\n"
        "🚀 Fast Download Enabled\n\n"
        "📎 Send your video link 👇"
    )

async def link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not ("youtube.com" in url or "youtu.be" in url or "tiktok.com" in url):
        await update.message.reply_text("❌ YouTube/TikTok link পাঠাও")
        return

    context.user_data["url"] = url

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

    await update.message.reply_text(
        "╭━━━━━━━◇◆◇━━━━━━━╮\n"
        "   🎬 DOWNLOAD READY\n"
        "╰━━━━━━━◇◆◇━━━━━━━╯\n\n"
        "💜 Choose your format below 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    url = context.user_data.get("url")
    choice = q.data

    msg = await q.message.reply_text(
        "╭──────────────╮\n"
        "   🚀 DOWNLOADING\n"
        "╰──────────────╯\n\n"
        "📊 Please wait..."
    )

    try:
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

        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(data)

        await msg.edit_text(
            "╭──────────────╮\n"
            "   📤 SENDING\n"
            "╰──────────────╯\n\n"
            "✅ Almost done..."
        )

        if choice == "mp3":
            file_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")
            with open(file_path, "rb") as audio:
                await q.message.reply_audio(audio=audio, caption="🎧 MP3 Ready")
        else:
            with open(file_path, "rb") as video:
                await q.message.reply_video(video=video, caption="✅ Download Complete")

        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ Download failed\n\n" + str(e)[:200])

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, link_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🔥 Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
