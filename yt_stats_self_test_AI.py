import requests
import json
import re
from collections import Counter
import os

class YTStatsProMax:
    
    # Category mapping for YouTube standard categories
    CATEGORY_MAPPING = {
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
        "44": "Trailers"
    }

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = {}

    # Helper function to make a request to the YouTube API (This is AI generated so I don't know shit)
    def _make_request(self, url):
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Received status code {response.status_code} from YouTube API.")
                print(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}")
        return None

    # Get channel statistics from the URL
    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={self.channel_id}&key={self.api_key}'
        data = self._make_request(url)
        if not data:
            print("Error: Failed to fetch channel statistics.")
            return {}

        try:
            items = data.get('items', [])
            if not items:
                print("Error: No items found in channel statistics response.")
                return {}

            overall_channel_data = items[0]['statistics']
            additional_channel_data = items[0]['snippet']

            self.channel_statistics = {
                'channelTitle': additional_channel_data['title'],
                'viewCount': int(overall_channel_data.get('viewCount', 0)),
                'subscriberCount': int(overall_channel_data.get('subscriberCount', 0)),
                'videoCount': int(overall_channel_data.get('videoCount', 0)),
                'country': additional_channel_data.get('country', None),
                'channelCategory': self.get_channel_category()
            }
        except (KeyError, IndexError) as e:
            print(f"Error processing channel statistics: {e}")
            self.channel_statistics = {}
        return self.channel_statistics

    # Get channelCategory logic: count all category id in all videos of channel, return the most frequent category
    def get_channel_category(self):
        if not self.video_data:
            self.get_channel_video_data()

        categories = [video['category'] for video in self.video_data.values()]
        if not categories:
            return "Unknown"

        category_count = Counter(categories)
        most_common_category = category_count.most_common(1)

        return most_common_category[0][0] if most_common_category else "Unknown"

    # Get video data from the URL
    def get_channel_video_data(self):
        channel_videos = self._get_channel_videos(limit=50)
        if not channel_videos:
            print("Error: No videos found for this channel.")
            return {}

        for video_id in channel_videos.keys():
            video_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,topicDetails&id={video_id}&key={self.api_key}'
            data = self._make_request(video_url)
            if not data:
                print(f"Error: Failed to fetch data for video ID {video_id}.")
                continue

            try:
                items = data.get('items', [])
                if not items:
                    print(f"Error: No items found for video ID {video_id}.")
                    continue

                video_data = items[0]
                snippet = video_data['snippet']
                content_details = video_data['contentDetails']
                statistics = video_data['statistics']
                topic_details = video_data.get('topicDetails', {})

                category_id = snippet.get('categoryId', "N/A")
                category_name = self.CATEGORY_MAPPING.get(category_id, "Unknown")

                raw_topic_categories = topic_details.get('topicCategories', None)
                processed_topic_categories = self.process_topic_categories(raw_topic_categories)
                
                
                self.video_data[video_id] = {
                    'publishedAt': snippet.get('publishedAt', "N/A"),
                    'title': snippet.get('title', "No Title"),
                    'description': snippet.get('description', "No Description"),
                    'channelTitle': snippet.get('channelTitle', "Unknown"),
                    'tags': snippet.get('tags', None),
                    'category': category_name,
                    'defaultAudioLanguage': snippet.get('defaultAudioLanguage', None),
                    'duration': content_details.get('duration', "N/A"),
                    'licensedContent': content_details.get('licensedContent', False),
                    'viewCount': int(statistics.get('viewCount', 0)),
                    'likeCount': int(statistics.get('likeCount', 0)),
                    'commentCount': int(statistics.get('commentCount', 0)),
                    'topicCategories': processed_topic_categories
                }
            except (KeyError, IndexError) as e:
                print(f"Error processing video data for video ID {video_id}: {e}")
        return self.video_data
    

    
    """
    Process the list of topicCategories URLs into a simplified format.
    Args:
        topic_categories (list): A list of URLs pointing to Wikipedia topic categories.
        it is a list contains these links, the normal form is
        ["https://en.wikipedia.org/wiki/the_topic_categories_1"
        "https://en.wikipedia.org/wiki/the_topic_categories_2"]
        
    Returns:
        list: after process, it will become this
        [the topic categories 1,
        the topic categories 2]
    """
    
    def process_topic_categories(self, topic_categories):

        if not topic_categories or not isinstance(topic_categories, list):
            print("Invalid topic categories provided. Returning an empty list.")
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
    
    ##flip through each page for channel videos
    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit:
            url += f"&maxResults={limit}"

        videos = {}
        next_page_token = None
        for _ in range(10):  # Limit to 10 pages (50 videos per page)
            if next_page_token:
                url += f"&pageToken={next_page_token}"

            data = self._make_request(url)
            if not data:
                print("Error: Failed to fetch channel videos.")
                break

            items = data.get('items', [])
            for item in items:
                try:
                    if item['id']['kind'] == "youtube#video":
                        video_id = item['id']['videoId']
                        videos[video_id] = {}
                except KeyError as e:
                    print(f"Error extracting video ID: {e}")

            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break
        return videos

    #Dump channel statistics to json file. Json file will be stored in specified directory
    def dump_channel_statistics(self, directory=None):
        """Dump channel statistics to a JSON file."""
        if not self.channel_statistics:
            print("Error: No channel statistics to dump.")
            return

        #Safe filename
        channel_title = re.sub(r'[\\/*?:"<>|]', '_', self.channel_statistics['channelTitle']).replace(" ", "_").lower()
        filename = f"{channel_title}_channel_statistics.json"
        
        if directory:
            os.makedirs(directory, exist_ok=True)
            filepath = os.path.join(directory, filename)
        else:
            filepath = filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.channel_statistics, f, indent=4, ensure_ascii=False)
        print(f"Channel statistics dumped to {filepath}.")


    #Dump video data to json file. Json file will be stored in specified directory
    def dump_video_data(self, directory=None):

        if not self.video_data:
            print("Error: No video data to dump.")
            return
        if not self.channel_statistics:
            print('Getting channel statistics for filename')
            self.get_channel_statistics()

        #Safe filename
        channel_title = re.sub(r'[\\/*?:"<>|]', '_', self.channel_statistics['channelTitle']).replace(" ", "_").lower()
        filename = f"{channel_title}_video_data.json"

        if directory:
            os.makedirs(directory, exist_ok=True)
            filepath = os.path.join(directory, filename)
        else:
            filepath = filename
        
        # Write the data to a JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.video_data, f, indent=4, ensure_ascii=False)
        print(f"Video data dumped to {filepath}.")
        
        
    #I'm too lazy to add in more methods in dump
    def extract_video_data(self,directory=None):
        self.get_channel_video_data()
        self.dump_video_data(directory=directory)
    
    def extract_channel_statistics(self,directory=None):
        self.get_channel_statistics()
        self.dump_channel_statistics(directory=directory)
    
    def extract_all(self,directory=None):
        self.get_channel_statistics()
        self.get_channel_video_data()
        self.dump_channel_statistics(directory=directory)
        self.dump_video_data(directory=directory)