import os
import asyncio
import discord
from discord.ext import tasks
import requests
from datetime import datetime

# Load environment variables from .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, assume environment variables are set elsewhere

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Configuration from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID_STR = os.getenv('DISCORD_CHANNEL_ID')
DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID_STR) if DISCORD_CHANNEL_ID_STR else None
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID', 'UCYxRlFDqcWM4y7FfpiAN3KQ')  # White House channel ID
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHECK_INTERVAL = 5  # seconds

# Track if we've already notified about current live stream
last_live_video_id = None
is_currently_live = False


def check_youtube_live():
    """
    Check if the YouTube channel is currently live streaming.
    Returns: (is_live: bool, video_id: str or None, stream_title: str or None)
    """
    global last_live_video_id, is_currently_live
    
    try:
        # YouTube Data API v3 endpoint to search for live broadcasts
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'channelId': YOUTUBE_CHANNEL_ID,
            'eventType': 'live',
            'type': 'video',
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if there are any live videos
        if 'items' in data and len(data['items']) > 0:
            live_video = data['items'][0]
            video_id = live_video['id']['videoId']
            stream_title = live_video['snippet']['title']
            
            # Only notify if this is a new live stream (different video ID)
            if video_id != last_live_video_id:
                last_live_video_id = video_id
                is_currently_live = True
                return True, video_id, stream_title
            else:
                # Same stream still live
                is_currently_live = True
                return False, video_id, stream_title
        else:
            # No live streams found
            if is_currently_live:
                # Stream just ended
                is_currently_live = False
                last_live_video_id = None
            return False, None, None
            
    except Exception as e:
        print(f"Error checking YouTube live status: {e}")
        return False, None, None


@client.event
async def on_ready():
    """
    Called when the bot successfully connects to Discord.
    """
    print(f'{client.user} has connected to Discord!')
    print(f'Bot is in {len(client.guilds)} server(s)')
    
    # Start the monitoring task
    if not monitor_youtube.is_running():
        monitor_youtube.start()


@tasks.loop(seconds=CHECK_INTERVAL)
async def monitor_youtube():
    """
    Background task that checks YouTube channel every 5 seconds.
    """
    is_live, video_id, stream_title = check_youtube_live()
    
    if is_live and video_id:
        # Get the Discord channel
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            # Create embed message
            embed = discord.Embed(
                title="🔴 White House is LIVE!",
                description=f"**{stream_title}**",
                url=f"https://www.youtube.com/watch?v={video_id}",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Watch Now",
                value=f"[Click here to watch the stream](https://www.youtube.com/watch?v={video_id})",
                inline=False
            )
            embed.set_thumbnail(url="https://www.youtube.com/img/desktop/yt_1200.png")
            
            try:
                await channel.send("@everyone", embed=embed)
                print(f"Sent live notification for video: {video_id}")
            except Exception as e:
                print(f"Error sending Discord message: {e}")


@monitor_youtube.before_loop
async def before_monitor():
    """
    Wait until the bot is ready before starting the monitoring loop.
    """
    await client.wait_until_ready()


def main():
    """
    Main function to start the bot.
    """
    # Validate required environment variables
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN environment variable is required")
    if not DISCORD_CHANNEL_ID:
        raise ValueError("DISCORD_CHANNEL_ID environment variable is required")
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is required")
    
    print("Starting YouTube Live Monitor Bot...")
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()

