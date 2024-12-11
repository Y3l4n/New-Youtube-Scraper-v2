import json
import pandas as pd
import os

trending_file_path = 'sample_newest_trending_videos/24.11.12_US_trending_videos.json'

# Load the trending dataset
with open(trending_file_path, "r", encoding="utf-8") as f:
    trending_videos = json.load(f)

trending_df = pd.DataFrame.from_dict(trending_videos, orient="index")

# print(f"Number of videos in trending_videos: {trending_df.shape[0]}")

# view selected column from smallest to largest
def view_stats(column_name):
    list = sorted(trending_df[column_name].tolist())
    print(list)
    
# view_stats('viewCount')
# view_stats('likeCount')
# view_stats('commentCount')
trending_df['engagementRate'] = (trending_df['likeCount'] + trending_df['commentCount']) / trending_df['viewCount']
# view_stats('engagementRate')
# view_stats('avgDailyViews')

# Cut lower 20% of dataset based on these stats to further define trending videos
percentiles = trending_df[['viewCount', 'likeCount', 'commentCount', 'engagementRate', 'avgDailyViews']].quantile(0.2)
# print("20th percentiles:")
# print(percentiles)

trending_df = trending_df[
    (trending_df["viewCount"] >= 400000)
    & (trending_df['likeCount'] >= 10000)
    & (trending_df['commentCount'] >= 1000)
    & (trending_df['engagementRate'] >= 0.015)
    & (trending_df['avgDailyViews'] >= 100000)
]
# print(f"Number of trending videos after filtering: {trending_df.shape[0]}")

def view_lowest(column_name):
    lowest_view_count_row = trending_df.loc[trending_df[column_name].idxmin()]
    print(f"Title: {lowest_view_count_row['title']}")
    print(f'Published At: {lowest_view_count_row["publishedAt"]}')
    print(f"View Count: {lowest_view_count_row['viewCount']}")
    print(f"Like Count: {lowest_view_count_row['likeCount']}")
    print(f"Comment Count: {lowest_view_count_row['commentCount']}")
    print(f"Avg Daily Views: {lowest_view_count_row['avgDailyViews']}")
    print(f"Engagement Rate: {lowest_view_count_row['engagementRate']}")
    print(f"trendingPercentile: {lowest_view_count_row['trendingPercentile']}")

# view_lowest('viewCount')

# Assigning labels for trending dataset
trending_df['isTrending'] = 1
# Rank based on avgDailyViews and engagementRate
trending_df['trendingPercentile'] = trending_df[['avgDailyViews', 'viewCount', 'likeCount']].rank(pct=True).mean(axis=1)

trending_df['trendingPercentile'] = pd.cut(
    trending_df['trendingPercentile'], 
    10, 
    labels=[0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95], 
    include_lowest=True
)

# trending_df = trending_df.sort_values(by=['trendingPercentile', 'avgDailyViews', 'engagementRate'], ascending=[False, False, False])
print_df = trending_df[['channelTitle', 'viewCount', 'likeCount', 'commentCount', 'engagementRate', 'avgDailyViews', 'trendingPercentile']]
print_df = print_df.sort_values(by=['trendingPercentile', 'avgDailyViews'], ascending=False)
print(print_df.head(10))

# lowest_percentile_df = trending_df[trending_df['trendingPercentile'] == trending_df['trendingPercentile'].min()]
# df_2 = lowest_percentile_df[['viewCount', 'likeCount', 'commentCount', 'engagementRate', 'avgDailyViews', 'trendingPercentile']].quantile(0.1)
# print(df_2)


# print(trending_df.head())

# view_lowest('avgDailyViews')

# output_dir_1 = "yt_processed_datasets"
# trending_json = trending_df.to_json(orient="index", force_ascii=False, indent=4)
# with open(os.path.join(output_dir_1, "processed_US_trending_videos.json"), "w", encoding="utf-8") as f:
#     f.write(trending_json)

# print(f"Combined trending_videos JSON saved to {output_dir_1}.")