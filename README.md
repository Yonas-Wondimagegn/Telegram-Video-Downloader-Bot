# Telegram Video Downloader Bot

This is a Telegram bot that downloads videos from Instagram Reels and TikTok links and sends them to users.

## Features

- **Download videos from Instagram Reels and TikTok**: Send a link and get the video file.
- **Automatic cleanup**: Deletes all downloaded video files in the `downloads` folder every 10 minutes.
- **Manual cleanup**: Deletes all downloaded video files in the `downloads` folder using the `/deletemp4` command with a password.
- **Password protection**: Use a password to clear the download folder manually through the Telegram bot.

## Commands

- `/start` - Start the bot and get a welcome message.
- `/download <link>` - Download video from a provided Instagram Reel or TikTok link.
- `/help` - Show help message with usage instructions.
- `/dev` - Contact the developer.
- `/deletemp4 <password>` - Clear all video files in the `downloads` folder (you can set password so only the admin will clear the download folder)

## Prerequisites

- Python 3.7 or later
- `python-telegram-bot` library
- `yt-dlp` library

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/telegram-video-downloader-bot.git
   cd telegram-video-downloader-bot
