import os
import json

# Path to the directory containing your JSON files
channel_dir = "sample_youtube_statistics"
output_dir = "sample_youtube_statistics"

output_file_name = "combined_channel_data.json"
output_path = os.path.join(output_dir, output_file_name)

'''
Combine all channel data into 1 file
'''
combined_data = {}

for file in os.listdir(channel_dir):
    if file.endswith(".json"):
        file_path = os.path.join(channel_dir, file)
        print(f"Loading {file_path}...")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            combined_data.update(data)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save the combined data to the specified path
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=4)

print(f"Combined JSON saved to {output_path}.")