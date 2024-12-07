import json
import os

def extract_channel_ids_from_multiple_jsons(json_folder, output_file):
    """
    Extracts all channel IDs from multiple JSON files in a directory and saves them into a single text file.
    (After fetching the trending videos, this will collect all channel ids into channel_ids.txt)
    (so that you could run the YTstats for each channel in the trending list)

    Parameters:
    json_folder (str): Path to the folder containing JSON files.
    output_file (str): Path to the text file where the channel IDs will be saved.
    """
    all_channel_ids = set()  # Use a set to avoid duplicate channel IDs

    try:
        # Iterate through all files in the folder
        for file_name in os.listdir(json_folder):
            # Process only `.json` files
            if file_name.endswith('.json'):
                file_path = os.path.join(json_folder, file_name)
                print(f"Processing file: {file_path}")
                
                # Load the JSON data
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Extract channel IDs and add them to the set
                channel_ids = [video_data["channelId"] for video_id, video_data in data.items()]
                all_channel_ids.update(channel_ids)
        
        # Save all unique channel IDs to the output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(all_channel_ids))
        
        print(f"Successfully extracted {len(all_channel_ids)} unique channel IDs to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# Provide the folder containing your JSON files and the output text file
extract_channel_ids_from_multiple_jsons("newest_trending_videos", "channel_ids.txt")