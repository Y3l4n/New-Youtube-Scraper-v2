import yt_stats_self_test_AI
from yt_stats_self_test_AI import YTStatsProMax


output_directory = 'youtube_channel_data'
# Load API key from api_key.txt
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()

# Load channel IDs from channel_id.txt
with open('channel_id.txt', 'r') as f:
    channel_ids = [line.strip() for line in f.readlines()]

for channel_id in channel_ids:
    print(f"Processing channel: {channel_id}")
    yt = YTStatsProMax(api_key, channel_id)
    yt.extract_video_data(directory=output_directory)