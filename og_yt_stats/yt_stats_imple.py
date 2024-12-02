import yt_stats
from yt_stats import YTstats

with open('api_key.txt', 'r') as file:
    api_key = file.readline().strip()

with open('channel_id.txt', 'r') as file:
    channel_id = [line.strip() for line in file]
    
yt = YTstats(api_key, channel_id)

yt.extract_all()

yt.dump()

print("Channel Statistics:")

print(yt.channel_statistics)