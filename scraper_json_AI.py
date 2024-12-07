import requests
import sys
import time
import os
import argparse
import json
from datetime import datetime, timezone


class YouTubeScraper:
    
    RECORDED_UTC_TIME = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
    def __init__(self, api_key, country_codes, output_dir="output/"):
        self.api_key = api_key
        self.country_codes = country_codes
        self.output_dir = output_dir

        self.snippet_features = ["title", "publishedAt", "channelTitle", "description"]

        self.CATEGORY_MAPPING = {
            "1": "Film & Animation",
            "2": "Autos & Vehicles",
            "10": "Music",
            "15": "Pets & Animals",
            "17": "Sports",
            "18": "Short Movies",
            "19": "Travel & Events",
            "20": "Gaming",
            "21": "Videoblogging",
            "22": "People & Blogs",
            "23": "Comedy",
            "24": "Entertainment",
            "25": "News & Politics",
            "26": "Howto & Style",
            "27": "Education",
            "28": "Science & Technology",
            "29": "Nonprofits & Activism",
            "30": "Movies",
            "31": "Anime/Animation",
            "32": "Action/Adventure",
            "33": "Classics",
            "34": "Comedy",
            "35": "Documentary",
            "36": "Drama",
            "37": "Family",
            "38": "Foreign",
            "39": "Horror",
            "40": "Sci-Fi/Fantasy",
            "41": "Thriller",
            "42": "Shorts",
            "43": "Shows",
            "44": "Trailers",
        }
        

    def api_request(self, page_token, country_code):
        request_url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=snippet,statistics,contentDetails,topicDetails&chart=mostPopular"
            f"&regionCode={country_code}&maxResults=50"
            f"&key={self.api_key}"
        )
        if page_token:
            request_url += f"&pageToken={page_token}"

        request = requests.get(request_url)

        if request.status_code == 429:
            print("Temp-banned due to excess requests, please wait and continue later")
            sys.exit()
        elif request.status_code != 200:
            print(f"Error: {request.status_code} - {request.text}")
            return {}

        return request.json()

    def parse_duration(self, duration_str):
        """Return duration in ISO 8601 format or a default value."""
        return duration_str if duration_str else "PT0S"

    
    def get_videos(self, items):
        
        videos = {}
        
        for video in items:
            if "statistics" not in video or "contentDetails" not in video or "snippet" not in video:
                continue

            video_id = video.get("id", "")
            snippet = video["snippet"]
            statistics = video["statistics"]
            content_details = video["contentDetails"]
            topic_details = video.get("topicDetails", {})

            category_id = snippet.get('categoryId', "N/A")
            category_name = self.CATEGORY_MAPPING.get(category_id, "Unknown")
            
            raw_topic_categories = topic_details.get('topicCategories', None)
            processed_topic_categories = self.process_topic_categories(raw_topic_categories)
            
            published_at = snippet.get('publishedAt', None)
            view_count = statistics.get('viewCount', 0)
            
            exact_elapsed_days = self.calculate_exact_elapsed_days(published_at)
            average_views_per_day = self.calculate_average_views_per_day(view_count, exact_elapsed_days)  
            
            # Construct video data
            video_data = {
                'fetchedDate': self.RECORDED_UTC_TIME,
                "publishedAt": published_at,
                'elapsedDays': round(float(exact_elapsed_days), 4),
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "channelTitle": snippet.get("channelTitle", ""),
                "channelId": snippet.get("channelId", ""),
                "tags": snippet.get("tags", None),
                "category": category_name,
                "duration": self.parse_duration(content_details.get("duration", "")),
                "licensedContent": content_details.get("licensedContent", False),
                "viewCount": int(view_count),
                'avgDailyViews': round(float(average_views_per_day), 2),
                "likeCount": int(statistics.get("likeCount", 0)),
                "commentCount": int(statistics.get("commentCount", 0)),
                "topicCategories": processed_topic_categories,
            }

            # Add video data to dictionary with video_id as key
            videos[video_id] = video_data

        return videos
    
    
    def process_topic_categories(self, topic_categories):

        if not topic_categories or not isinstance(topic_categories, list):
            return []

        processed_categories = []
        for url in topic_categories:
            try:
                # Extract the last part of the URL after the last "/"
                category_name = url.split("/")[-1]
                # Replace underscores with spaces to make it more readable
                category_name = category_name.replace("_", " ")
                processed_categories.append(category_name)
            except Exception as e:
                print(f"Error processing URL '{url}': {e}")
        
        return processed_categories

    def calculate_exact_elapsed_days(self, published_time):
            
        '''
        Calculate the exact elapsed days from the published time
        '''
        
        published_dt = datetime.strptime(published_time, "%Y-%m-%dT%H:%M:%SZ")
        elapsed = datetime.strptime(self.RECORDED_UTC_TIME, "%Y-%m-%dT%H:%M:%SZ") - published_dt
        elapsed_days = elapsed.total_seconds() / 60 / 60 / 24
        return f'{elapsed_days:.4f}'
    
    
    def calculate_average_views_per_day(self, view_count, exact_elapsed_days):
            
        '''
        Calculate the average views per day
        '''
        
        return f'{int(view_count) / float(exact_elapsed_days):.2f}'
    
    
    def get_pages(self, country_code):
        country_data = {}
        next_page_token = ""

        while next_page_token is not None:
            video_data_page = self.api_request(next_page_token, country_code)
            next_page_token = video_data_page.get("nextPageToken", None)

            items = video_data_page.get("items", [])
            country_data.update(self.get_videos(items))

        return country_data

    def write_to_file(self, country_code, country_data):
        print(f"Writing {country_code} data to file...")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        file_path = os.path.join(self.output_dir, f"{time.strftime('%y.%d.%m')}_{country_code}_trending_videos.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(country_data, file, ensure_ascii=False, indent=4)

        print(f"Data successfully written to {file_path}")

    def scrape_data(self):
        for country_code in self.country_codes:
            print(f"Scraping data for country: {country_code}")
            country_data = self.get_pages(country_code)
            self.write_to_file(country_code, country_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key_path", help="Path to the file containing the API key", default="api_key.txt")
    parser.add_argument("--country_code_path", help="Path to the file containing the list of country codes", default="country_codes.txt")
    parser.add_argument("--output_dir", help="Path to save the outputted files", default="sample_newest_trending_videos/")

    args = parser.parse_args()

    with open(args.key_path, "r") as file:
        api_key = file.readline().strip()

    with open(args.country_code_path, "r") as file:
        country_codes = [line.strip() for line in file]

    scraper = YouTubeScraper(api_key, country_codes, args.output_dir)
    scraper.scrape_data()