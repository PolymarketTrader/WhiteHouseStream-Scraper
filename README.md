# YouTube Live Monitor Discord Bot

A Discord bot that continuously monitors the White House YouTube channel and sends notifications to your Discord server when they go live.

## Features

- 🔴 Monitors YouTube channel every 5 seconds
- 📢 Sends @everyone notifications when the channel goes live
- 🎨 Beautiful embed messages with stream links
- 🚀 Ready for Railway deployment

## Prerequisites

Before setting up this bot, you'll need:

1. **Discord Webhook URL** (Easy! No bot application needed)
   - Go to your Discord server
   - Right-click on the channel where you want notifications
   - Select "Edit Channel" → "Integrations" → "Webhooks"
   - Click "New Webhook" or "Create Webhook"
   - Copy the webhook URL (looks like: `https://discord.com/api/webhooks/...`)
   - You can customize the webhook name/avatar if you want

2. **YouTube Data API Key**
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
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url_here
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

5. **Run the bot:**
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
     - `DISCORD_WEBHOOK_URL` (your Discord webhook URL)
     - `YOUTUBE_API_KEY` (your YouTube API key)
     - `YOUTUBE_CHANNEL_ID` (optional, defaults to White House channel)

5. **Configure the service:**
   - Railway should auto-detect Python
   - If not, add a `Procfile` with: `worker: python bot.py`
   - Make sure the start command is set to: `python bot.py`

6. **Deploy:**
   - Railway will automatically deploy when you push to GitHub
   - Check the "Deployments" tab to see logs

## How It Works

1. The script runs continuously and checks the White House YouTube channel every 5 seconds using the YouTube Data API
2. When a live stream is detected (and it's a new stream), it sends a notification to your Discord channel using a webhook
3. The notification includes:
   - @everyone mention
   - Stream title
   - Direct link to watch the stream
   - Beautiful embed with thumbnail

## Customization

- **Change check interval:** Modify `CHECK_INTERVAL` in `bot.py` (currently 5 seconds)
- **Change YouTube channel:** Set `YOUTUBE_CHANNEL_ID` in your `.env` file or environment variables
- **Modify notification message:** Edit the embed in the `monitor_youtube()` function

## Troubleshooting

- **No notifications received:** 
  - Verify your Discord webhook URL is correct (should start with `https://discord.com/api/webhooks/`)
  - Make sure the webhook hasn't been deleted in Discord
  - Verify your YouTube API key is valid and has quota remaining
- **Railway deployment fails:** Check that all environment variables are set correctly
- **Webhook errors:** Make sure you copied the complete webhook URL from Discord

## License

This project is open source and available for personal use.

