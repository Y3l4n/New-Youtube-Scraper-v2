import json
import os

def extract_channel_ids_from_multiple_jsons(json_folder, output_file):
    '''
    Fetch all channel ids in the trending videos dataset, then write them to channel_ids.txt
    This can be used in YTStats to fetch the video info of all channel presented in the trending videos dataset
    '''

    all_channel_ids = set()  # Use a set to avoid duplicate channel IDs

    try:
        for file_name in os.listdir(json_folder):
            # Process only `.json` files
            if file_name.endswith('.json'):
                file_path = os.path.join(json_folder, file_name)
                print(f"Processing file: {file_path}")
                
                # Load the JSON data
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                channel_ids = [video_data["channelId"] for video_id, video_data in data.items()]
                all_channel_ids.update(channel_ids)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(all_channel_ids))
        
        print(f"Successfully extracted {len(all_channel_ids)} unique channel IDs to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

extract_channel_ids_from_multiple_jsons("newest_trending_videos", "channel_ids.txt")