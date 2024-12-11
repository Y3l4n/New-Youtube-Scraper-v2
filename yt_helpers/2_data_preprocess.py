import json
import pandas as pd
import os

trending_file_path = 'sample_newest_trending_videos/24.11.12_US_trending_videos.json'
combined_channel_data_file_path = 'sample_youtube_statistics/combined_channel_data.json'

# Load the trending dataset
with open(trending_file_path, "r", encoding="utf-8") as f:
    trending_videos = json.load(f)

# Load the combined channel dataset
with open(combined_channel_data_file_path, "r", encoding="utf-8") as f:
    combined_channel_data = json.load(f)

# Convert both datasets to pandas DataFrames
trending_df = pd.DataFrame.from_dict(trending_videos, orient="index")
combined_df = pd.DataFrame.from_dict(combined_channel_data, orient="index")

trending_df = trending_df[trending_df["viewCount"] >= 100000]
combined_df = combined_df[combined_df["viewCount"] >= 1000]
print(f"Number of videos with at least 100,000 views in trending_videos: {trending_df.shape[0]}")
print(f"Number of videos with at least 1,000 views in channel_data: {combined_df.shape[0]}")

# Drop trending videos that have either zero likes or zero comments (further processing)
trending_df = trending_df[(trending_df["likeCount"] > 0) & (trending_df["commentCount"] > 0)]
print(f"Number of trending videos after dropping rows with zero likes or comments: {trending_df.shape[0]}")

output_dir_1 = "sample_newest_trending_videos"
output_dir_2 = "sample_youtube_statistics"
# Convert the DataFrame to a JSON object
trending_json = trending_df.to_json(orient="index", force_ascii=False, indent=4)
combined_json = combined_df.to_json(orient="index", force_ascii=False, indent=4)

with open(os.path.join(output_dir_2, "processed_channel_data.json"), "w", encoding="utf-8") as f:
    f.write(combined_json)
# Save the JSON object to a file
with open(os.path.join(output_dir_1, "processed_trending_videos.json"), "w", encoding="utf-8") as f:
    f.write(trending_json)

print(f"Combined trending_videos JSON saved to {output_dir_1}.")
print(f"Combined channel_data JSON saved to {output_dir_2}.")