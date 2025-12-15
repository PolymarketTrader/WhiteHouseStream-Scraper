# YouTube Live Monitor Discord Bot

A Discord bot that continuously monitors the White House YouTube channel and sends notifications to your Discord server when they go live.

## Features

- 🔴 Monitors YouTube channel every 5 seconds
- 📢 Sends @everyone notifications when the channel goes live
- 🎨 Beautiful embed messages with stream links
- 🚀 Ready for Railway deployment

## Prerequisites

Before setting up this bot, you'll need:

1. **Discord Bot Token**
   - Go to https://discord.com/developers/applications
   - Create a new application
   - Go to "Bot" section and create a bot
   - Copy the bot token
   - Enable "Message Content Intent" under Privileged Gateway Intents

2. **Discord Channel ID**
   - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
   - Right-click on your channel → Copy ID

3. **YouTube Data API Key**
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing one
   - Enable "YouTube Data API v3"
   - Create credentials (API Key)
   - Copy the API key

## Setup Instructions

### Local Development

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   On Windows PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```

4. **Edit `.env` and add your credentials:**
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_CHANNEL_ID=your_discord_channel_id_here
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

5. **Invite your bot to your Discord server:**
   - Go to https://discord.com/developers/applications
   - Select your application
   - Go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`
   - Select bot permissions: `Send Messages`, `Embed Links`, `Mention Everyone`
   - Copy the generated URL and open it in your browser to invite the bot

6. **Run the bot:**
   ```bash
   python bot.py
   ```

### Deploying to Railway

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-github-repo-url
   git push -u origin main
   ```

2. **Create a Railway account:**
   - Go to https://railway.app/
   - Sign up/login with GitHub

3. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

4. **Configure environment variables:**
   - In your Railway project, go to "Variables" tab
   - Add all variables from `.env.example`:
     - `DISCORD_TOKEN`
     - `DISCORD_CHANNEL_ID`
     - `YOUTUBE_API_KEY`
     - `YOUTUBE_CHANNEL_ID` (optional, defaults to White House channel)

5. **Configure the service:**
   - Railway should auto-detect Python
   - If not, add a `Procfile` with: `worker: python bot.py`
   - Make sure the start command is set to: `python bot.py`

6. **Deploy:**
   - Railway will automatically deploy when you push to GitHub
   - Check the "Deployments" tab to see logs

## How It Works

1. The bot connects to Discord using your bot token
2. Every 5 seconds, it checks the White House YouTube channel for live streams using the YouTube Data API
3. When a live stream is detected (and it's a new stream), it sends a notification to your Discord channel
4. The notification includes:
   - @everyone mention
   - Stream title
   - Direct link to watch the stream
   - Beautiful embed with thumbnail

## Customization

- **Change check interval:** Modify `CHECK_INTERVAL` in `bot.py` (currently 5 seconds)
- **Change YouTube channel:** Set `YOUTUBE_CHANNEL_ID` in your `.env` file or environment variables
- **Modify notification message:** Edit the embed in the `monitor_youtube()` function

## Troubleshooting

- **Bot doesn't respond:** Make sure the bot has permission to send messages in your channel
- **No notifications:** Verify your YouTube API key is valid and has quota remaining
- **Railway deployment fails:** Check that all environment variables are set correctly

## License

This project is open source and available for personal use.

