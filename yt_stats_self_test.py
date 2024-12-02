import requests
import json
import re
from collections import Counter

class YTStatsProMax:
    
    #Category mapping for YouTube standard categories
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
        
    
    # Get channel statistics from the url
    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={self.channel_id}&key={self.api_key}'
        # print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        # print(data)
        try:
            overall_channel_data = data['items'][0]['statistics']
            additional_channel_data = data['items'][0]['snippet']
            
            self.channel_statistics = {
                'channelTitle': additional_channel_data['title'],
                'viewCount': int(overall_channel_data.get('viewCount', 0)),
                'subscriberCount': int(overall_channel_data.get('subscriberCount', 0)),
                'videoCount': int(overall_channel_data.get('videoCount', 0)),
                'country': additional_channel_data.get('country', None),
                'channelCategory': self.get_channel_category()
            }
            
        except (KeyError, IndexError) as e:
            print(f'Error! Could not get channel statistics for channel ID {self.channel_id}: \n{data}')
            self.channel_statistics = {}
        return self.channel_statistics
    
    
    '''
    Get channelCategory logic: count all category id in all videos of channel
    Return the most frequent category
    If category not found, return "Unknown"
    '''
    def get_channel_category(self):
        if not self.video_data:
            self.get_channel_video_data()
            
        categories = [video['categoryId'] for video in self.video_data.values()]
        if not categories:
            return "Unknown"
        
        category_count = Counter(categories)
        most_common_category = category_count.most_common(1)
        
        category_id = most_common_category[0][0]
        
        return self.CATEGORY_MAPPING.get(category_id, "Unknown")
    
    
    # Get video data from the url
    def get_channel_video_data(self):
        # 1. Get video id
        channel_videos = self._get_channel_videos(limit=50) #max num of videos to get on 1 page
        # print(channel_videos) #get all video ids
        # print(len(channel_videos)) #how many videos
        
        # 2. Get video statistics
        for video_id in channel_videos.keys():
            video_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,topicDetails&id={video_id}&key={self.api_key}'
            json_url = requests.get(video_url)
            data = json.loads(json_url.text)
            
            try:
                video_data = data['items'][0]
                snippet = video_data['snippet']
                content_details = video_data['contentDetails']
                statistics = video_data['statistics']
                topic_details = video_data.get('topicDetails', {})
                
                #Category mapping
                category_id = snippet.get('categoryId', "N/A")
                category_name = self.CATEGORY_MAPPING.get(category_id, "N/A")

                self.video_data[video_id] = {
                    'publishedAt': snippet['publishedAt'],
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'channelTitle': snippet['channelTitle'],
                    'tags': snippet.get('tags', None),
                    'category': category_name,
                    'defaultAudioLanguage': snippet.get('defaultAudioLanguage', None),
                    'duration': content_details['duration'],
                    'licensedContent': content_details['licensedContent'],
                    'viewCount': int(statistics.get('viewCount', 0)),
                    'likeCount': int(statistics.get('likeCount', 0)),
                    'commentCount': int(statistics.get('commentCount', 0)),
                    'topicCategories': topic_details.get('topicCategories', None)
                }
            except (KeyError, IndexError):
                print(f'Error! Could not get video data for video ID {video_id}: \n{data}')
            
        return self.video_data
    
    
    def _get_channel_videos(self, limit=None): #flip through each page for channel videos
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit is not None and isinstance(limit, int): #Check limit not none / is integer
            url += "&maxResults=" + str(limit)
        # print(url)
        
        vid, next_page_token = self._get_channel_videos_per_page(url)
        index = 0
        while(next_page_token is not None and index < 10): #limit to 10 pages (50 videos each)
            next_url = url + "&pageToken=" + next_page_token
            next_vid, next_page_token = self._get_channel_videos_per_page(next_url)
            vid.update(next_vid) #update next video dictionary
            index += 1
            
        return vid
    
    
    def _get_channel_videos_per_page(self, url): #helper method to get video on each page
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        
        channel_videos = dict()
        if 'items' not in data: #check the 'items' key in data
            print('Error! Could not get correct channel data!\n', data)
            return channel_videos, None
        
        item_data = data['items']
        nextPageToken = data.get("nextPageToken", None) #get next page token to go to next page
        
        for item in item_data:
            try:
                kind = item['id']['kind'] #get kind in id 
                if kind == 'youtube#video': #get video type only
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = {}
            except KeyError as e:
                print('Error! Could not extract video ID from item:\n', item)
            
        return channel_videos, nextPageToken
        
    
    #Dump channel statistics
    def dump_channel_statistics(self):
        if self.channel_statistics is None:
            print("No channel statistics to dump.")
            return
        
        channel_title = re.sub(r'[\\/*?:"<>|]', '_', self.channel_statistics['channelTitle']).replace(" ", "_").lower()
        filename = f"{channel_title}_channel_statistics.json"

        # Write the channel statistics to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.channel_statistics, f, indent=4, ensure_ascii=False)

        print(f'Channel statistics dumped to {filename}')
            
    
    #Dump video data
    def dump_video_data(self):
        """Dumps video data into a JSON file"""
        if self.video_data is None:
            print('Video data is missing!')
            return
        if not self.channel_statistics:
            print('Getting channel statistics for filename...')
            self.get_channel_statistics()
            
        # Replace invalid characters in the file name
        channel_title = re.sub(r'[\\/*?:"<>|]', '_', self.channel_statistics['channelTitle']).replace(" ", "_").lower()
        filename = f"{channel_title}_video_data.json"

        # Write the video data to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.video_data, f, indent=4, ensure_ascii=False)

        print(f'Video data dumped to {filename}')