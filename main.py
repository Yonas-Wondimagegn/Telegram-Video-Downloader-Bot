import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import time
import threading

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = 'your_telegram_Token'  # Your Telegram token
PASSWORD = '123'  # Set your password here (optional)

async def start(update: Update, context: CallbackContext):
    user_info = update.message.from_user
    first_name = user_info.first_name
    await update.message.reply_text(f'''
Hello {first_name},

This bot is used to download videos from Instagram Reels and TikTok links and send them to you
Available commands:

/start
/help
/dev

To use simply send /download followed by an instagram reel or tikTok link and I'll send you the video file 😌
''')

async def dev(update: Update, context: CallbackContext):
    await update.message.reply_text('''
If you got an error or have any suggestions...feel free to reach out:
@A13X60 🤛🏽
''')

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('''
To use simply send /download followed by an instagram reel or tikTok link and I'll send you the video file.

Example:
/download https://www.instagram.com/reel/blablabla
or
/download https://www.tiktok.com/@user/video/blablabla
''')

def clear_download_folder():
    """Clears all downloaded files in the downloads folder."""
    downloads_folder = 'downloads'
    for file in os.listdir(downloads_folder):
        if file.endswith(('.mp4', '.mkv', '.webm')):
            file_path = os.path.join(downloads_folder, file)
            os.remove(file_path)
            logger.info(f'Deleted {file_path}')

async def download_and_upload(update: Update, context: CallbackContext) -> None:
    link = ' '.join(context.args)
    if not link:
        await update.message.reply_text('Please provide a link 👀')
        return

    await update.message.reply_text('Downloading video, please wait... ⏳')

    try:
        # Validate the link
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,  # Suppress console output
        }

        file_title = None

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(link, download=True)
                file_title = ydl.prepare_filename(info_dict)
            except yt_dlp.DownloadError as e:
                logger.error(f'Failed to download: {e}')
                await update.message.reply_text('Invalid link or download failed. Please check the URL and try again.')
                return

        # Check if the file exists and send it
        if file_title and os.path.exists(file_title):
            with open(file_title, 'rb') as video_file:
                await update.message.reply_video(video_file, filename=os.path.basename(file_title))
            await update.message.reply_text('Thanks for using my bot keshke🙇‍♂️🌚')
            logger.info(f'File {file_title} sent to user.')

            clear_download_folder()
            logger.info('Cleared downloads folder.')
        else:
            logger.error(f'File not found after download: {file_title}')
            await update.message.reply_text('An error occurred while processing the link you provided...\n\nSIKE...please wait a few seconds. If the issue persists contact me \n')

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        await update.message.reply_text('FOR NOW THE TIKTOK DOWNLOADER IS UNDER MAINTAINANCE UNTIL THEN YOU CAN USE INSTAGRAM REEL(THE BETTER ONE) THANKS \n @A13XBOTZ.\n\nJoin this channel to get update and also to make me smile:)')

async def delete_temp_files(update: Update, context: CallbackContext):
    password = ' '.join(context.args)
    if password == PASSWORD:
        clear_download_folder()
        await update.message.reply_text('All video files have been deleted from the download folder.')
        logger.info('All video files cleared from the downloads folder.')
    else:
        await update.message.reply_text('👀 Invalid password. Access denied.')

def monitor_download_folder():
    """Continuously monitors the download folder and clears video files every 5 minutes"""
    downloads_folder = 'downloads'
    while True:
        time.sleep(600)  # Wait for 5 minutes to delete
        clear_download_folder()
        logger.info('Cleared downloads folder.')

def start_monitoring():
    """Starts the download folder monitoring in a separate thread."""
    monitor_thread = threading.Thread(target=monitor_download_folder, daemon=True)
    monitor_thread.start()

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("download", download_and_upload))
    application.add_handler(CommandHandler("dev", dev))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("deletemp4", delete_temp_files))

    logger.info('Starting bot')

    # Start folder monitoring thread
    start_monitoring()

    application.run_polling()

if __name__ == '__main__':
    main()
