import os
import time
import requests
from datetime import datetime

# Load environment variables from .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, assume environment variables are set elsewhere

# Configuration from environment variables
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
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


def send_discord_notification(video_id, stream_title):
    """
    Send a notification to Discord using webhook.
    """
    try:
        # Create embed message for Discord webhook
        embed = {
            "title": "🔴 White House is LIVE!",
            "description": f"**{stream_title}**",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "color": 15158332,  # Red color (decimal representation)
            "timestamp": datetime.utcnow().isoformat(),
            "fields": [
                {
                    "name": "Watch Now",
                    "value": f"[Click here to watch the stream](https://www.youtube.com/watch?v={video_id})",
                    "inline": False
                }
            ],
            "thumbnail": {
                "url": "https://www.youtube.com/img/desktop/yt_1200.png"
            }
        }
        
        # Webhook payload
        payload = {
            "content": "@everyone",
            "embeds": [embed]
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Sent live notification for video: {video_id}")
        return True
        
    except Exception as e:
        print(f"Error sending Discord message: {e}")
        return False


def main():
    """
    Main function to continuously monitor YouTube and send notifications.
    """
    # Validate required environment variables
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is required")
    
    print("Starting YouTube Live Monitor Bot...")
    print(f"Monitoring YouTube channel: {YOUTUBE_CHANNEL_ID}")
    print(f"Checking every {CHECK_INTERVAL} seconds...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            is_live, video_id, stream_title = check_youtube_live()
            
            if is_live and video_id:
                send_discord_notification(video_id, stream_title)
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()

