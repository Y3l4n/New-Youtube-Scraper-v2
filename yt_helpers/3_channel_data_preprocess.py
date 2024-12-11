import json
import pandas as pd
import os

combined_channel_data_file_path = 'yt_processed_datasets/combined_channel_data.json'

# Load the combined channel dataset
with open(combined_channel_data_file_path, "r", encoding="utf-8") as f:
    combined_channel_data = json.load(f)

# Convert both datasets to pandas DataFrames
combined_df = pd.DataFrame.from_dict(combined_channel_data, orient="index")

print(f"Number of videos in channel_data: {combined_df.shape[0]}")

# Cut lower 10% of dataset (these stats) to eliminate data with missing values
percentiles = combined_df[['viewCount', 'likeCount', 'commentCount', 'avgDailyViews', 'engagementRate']].quantile(0.1)
# print("10th percentiles:")
# print(percentiles)

combined_df = combined_df[
    (combined_df["viewCount"] >= 92000)
    & (combined_df['likeCount'] >= 2000)
    & (combined_df['commentCount'] >= 70)
    & (combined_df['engagementRate'] >= 0.001) # Set to 0.001 because of the low engagement rate (ex: music videos)
    & (combined_df['avgDailyViews'] >= 170)
]
print(f"Number of trending videos after filtering: {combined_df.shape[0]}")





output_dir_2 = "yt_processed_datasets"
combined_json = combined_df.to_json(orient="index", force_ascii=False, indent=4)
with open(os.path.join(output_dir_2, "processed_channel_data.json"), "w", encoding="utf-8") as f:
    f.write(combined_json)    
print(f"Combined channel_data JSON saved to {output_dir_2}.")