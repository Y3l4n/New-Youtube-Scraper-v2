import requests
import sys
import time
import os
import argparse
import isodate
import json
from datetime import timedelta


class YouTubeScraper:
    def __init__(self, api_key, country_codes, output_dir="output/"):
        self.api_key = api_key
        self.country_codes = country_codes
        self.output_dir = output_dir

        self.snippet_features = ["title", "publishedAt", "channelTitle", "description"]

        self.category_mapping = {
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
        
        self.default_audio_language = {
            "zxx": "Not applicable",
            "ab": "Abkhazian",
            "aa": "Afar",
            "af": "Afrikaans",
            "sq": "Albanian",
            "ase": "American Sign Language",
            "am": "Amharic",
            "ar": "Arabic",
            "arc": "Aramaic",
            "hy": "Armenian",
            "as": "Assamese",
            "ay": "Aymara",
            "az": "Azerbaijani",
            "bn": "Bangla",
            "ba": "Bashkir",
            "eu": "Basque",
            "be": "Belarusian",
            "bh": "Bihari",
            "bi": "Bislama",
            "bs": "Bosnian",
            "br": "Breton",
            "bg": "Bulgarian",
            "yue": "Cantonese",
            "yue-HK": "Cantonese (Hong Kong)",
            "ca": "Catalan",
            "chr": "Cherokee",
            "zh": "Chinese",
            "zh-CN": "Chinese (China)",
            "zh-HK": "Chinese (Hong Kong)",
            "zh-Hans": "Chinese (Simplified)",
            "zh-SG": "Chinese (Singapore)",
            "zh-TW": "Chinese (Taiwan)",
            "zh-Hant": "Chinese (Traditional)",
            "cho": "Choctaw",
            "co": "Corsican",
            "hr": "Croatian",
            "cs": "Czech",
            "da": "Danish",
            "nl": "Dutch",
            "nl-BE": "Dutch (Belgium)",
            "nl-NL": "Dutch (Netherlands)",
            "dz": "Dzongkha",
            "en": "English",
            "en-CA": "English (Canada)",
            "en-IE": "English (Ireland)",
            "en-GB": "English (United Kingdom)",
            "en-US": "English (United States)",
            "eo": "Esperanto",
            "et": "Estonian",
            "fo": "Faroese",
            "fj": "Fijian",
            "fil": "Filipino",
            "fi": "Finnish",
            "fr": "French",
            "fr-BE": "French (Belgium)",
            "fr-CA": "French (Canada)",
            "fr-FR": "French (France)",
            "fr-CH": "French (Switzerland)",
            "gl": "Galician",
            "ka": "Georgian",
            "de": "German",
            "de-AT": "German (Austria)",
            "de-DE": "German (Germany)",
            "de-CH": "German (Switzerland)",
            "el": "Greek",
            "kl": "Greenlandic (Kalaallisut)",
            "gn": "Guarani",
            "gu": "Gujarati",
            "hak": "Hakka Chinese",
            "hak-TW": "Hakka Chinese (Taiwan)",
            "ha": "Hausa",
            "iw": "Hebrew",
            "hi": "Hindi",
            "hi-Latn": "Hindi (Phonetic)",
            "hu": "Hungarian",
            "is": "Icelandic",
            "ig": "Igbo",
            "id": "Indonesian",
            "ia": "Interlingua",
            "ie": "Interlingue",
            "iu": "Inuktitut",
            "ik": "Inupiaq",
            "ga": "Irish",
            "it": "Italian",
            "ja": "Japanese",
            "jv": "Javanese",
            "kn": "Kannada",
            "ks": "Kashmiri",
            "kk": "Kazakh",
            "km": "Khmer",
            "rw": "Kinyarwanda",
            "tlh": "Klingon",
            "ko": "Korean",
            "ku": "Kurdish",
            "ky": "Kyrgyz",
            "lo": "Lao",
            "la": "Latin",
            "lv": "Latvian",
            "ln": "Lingala",
            "lt": "Lithuanian",
            "lb": "Luxembourgish",
            "mk": "Macedonian",
            "mg": "Malagasy",
            "ms": "Malay",
            "ml": "Malayalam",
            "mt": "Maltese",
            "mi": "Maori",
            "mr": "Marathi",
            "mas": "Masai",
            "nan": "Min Nan Chinese",
            "nan-TW": "Min Nan Chinese (Taiwan)",
            "mo": "Moldavian",
            "mn": "Mongolian",
            "my": "Myanmar (Burmese)",
            "na": "Nauru",
            "nv": "Navajo",
            "ne": "Nepali",
            "no": "Norwegian",
            "oc": "Occitan",
            "or": "Odia",
            "om": "Oromo",
            "ps": "Pashto",
            "fa": "Persian",
            "fa-AF": "Persian (Afghanistan)",
            "fa-IR": "Persian (Iran)",
            "pl": "Polish",
            "pt": "Portuguese",
            "pt-BR": "Portuguese (Brazil)",
            "pt-PT": "Portuguese (Portugal)",
            "pa": "Punjabi",
            "qu": "Quechua",
            "ro": "Romanian",
            "rm": "Romansh",
            "rn": "Rundi",
            "ru": "Russian",
            "ru-Latn": "Russian (Phonetic)",
            "sm": "Samoan",
            "sg": "Sango",
            "sa": "Sanskrit",
            "gd": "Scottish Gaelic",
            "sr": "Serbian",
            "sr-Cyrl": "Serbian (Cyrillic)",
            "sr-Latn": "Serbian (Latin)",
            "sh": "Serbo-Croatian",
            "sdp": "Sherdukpen",
            "sn": "Shona",
            "sd": "Sindhi",
            "si": "Sinhala",
            "sk": "Slovak",
            "sl": "Slovenian",
            "so": "Somali",
            "st": "Southern Sotho",
            "es": "Spanish",
            "es-419": "Spanish (Latin America)",
            "es-MX": "Spanish (Mexico)",
            "es-ES": "Spanish (Spain)",
            "su": "Sundanese",
            "sw": "Swahili",
            "ss": "Swati",
            "sv": "Swedish",
            "tl": "Tagalog",
            "tg": "Tajik",
            "ta": "Tamil",
            "tt": "Tatar",
            "te": "Telugu",
            "th": "Thai",
            "bo": "Tibetan",
            "ti": "Tigrinya",
            "to": "Tongan",
            "ts": "Tsonga",
            "tn": "Tswana",
            "tr": "Turkish",
            "tk": "Turkmen",
            "tw": "Twi",
            "uk": "Ukrainian",
            "ur": "Urdu",
            "uz": "Uzbek",
            "vi": "Vietnamese",
            "vo": "Volapük",
            "cy": "Welsh",
            "fy": "Western Frisian",
            "wo": "Wolof",
            "xh": "Xhosa",
            "yi": "Yiddish",
            "yo": "Yoruba",
            "zu": "Zulu",
            "und": "Other",
        }
    
    #Parse default audio language
    def get_audio_language(self, language_code):
        return self.default_audio_language.get(language_code, 'Unknown')

    def api_request(self, page_token, country_code):
        request_url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=snippet,statistics,contentDetails&chart=mostPopular"
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

    def get_channel_stats(self, channel_id):
        url = (
            f"https://www.googleapis.com/youtube/v3/channels"
            f"?part=snippet,statistics&id={channel_id}&key={self.api_key}"
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            stats = data['items'][0]['statistics']
            snippet = data['items'][0]['snippet']
            subscriber_count = stats.get('subscriberCount', 0)
            total_view_count = stats.get('viewCount', 0)
            channel_country = snippet.get('country', 'Unknown')
            return int(subscriber_count), int(total_view_count), channel_country
        else:
            print(f"Error fetching channel stats: {response.status_code}")
            return 0, 0, 'Unknown'

    def parse_duration(self, duration_str):
        if not duration_str:
            return 0.0
        try:
            duration = isodate.parse_duration(duration_str)
            if isinstance(duration, timedelta):
                total_minutes = duration.total_seconds() / 60
                return round(total_minutes, 2)
            else:
                return 0.0
        except isodate.ISO8601Error:
            return 0.0

    def get_videos(self, items):
        video_list = []
        for video in items:
            if "statistics" not in video or "contentDetails" not in video:
                continue

            snippet = video['snippet']
            statistics = video['statistics']
            content_details = video['contentDetails']

            video_data = {feature: snippet.get(feature, "") for feature in self.snippet_features}

            category_id = snippet.get("categoryId", "")
            video_data["category"] = self.category_mapping.get(category_id, "Unknown")

            video_data["tags"] = snippet.get("tags", ["[none]"])

            duration_iso = content_details.get('duration', 'PT0S')
            video_data["duration"] = self.parse_duration(duration_iso)

            video_data["live_content"] = content_details.get('liveBroadcastContent', 'none')

            video_data["view_count"] = int(statistics.get("viewCount", 0))
            video_data["likes"] = int(statistics.get('likeCount', 0))
            video_data["comment_count"] = int(statistics.get('commentCount', 0))

            channel_id = snippet.get("channelId", "")
            subscriber_count, total_view_count, channel_country = self.get_channel_stats(channel_id)
            video_data["subscriber_count"] = subscriber_count
            video_data["total_view_count"] = total_view_count
            video_data["channel_country"] = channel_country

            video_data["engagement_rate"] = (
                (video_data["likes"] + video_data["comment_count"]) / video_data["view_count"]
                if video_data["view_count"] else 0
            )

            video_list.append(video_data)
        return video_list

    def get_pages(self, country_code):
        country_data = []
        next_page_token = ""

        while next_page_token is not None:
            video_data_page = self.api_request(next_page_token, country_code)
            next_page_token = video_data_page.get("nextPageToken", None)

            items = video_data_page.get('items', [])
            country_data += self.get_videos(items)

        return country_data

    def write_to_file(self, country_code, country_data):
        print(f"Writing {country_code} data to file...")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        file_path = os.path.join(self.output_dir, f"{time.strftime('%y.%d.%m')}_{country_code}_videos.json")
        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(country_data, file, ensure_ascii=False, indent=4)  # Unicode decoding enabled

    def scrape_data(self):
        for country_code in self.country_codes:
            country_data = self.get_pages(country_code)
            self.write_to_file(country_code, country_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', help='Path to the file containing the API key', default='api_key.txt')
    parser.add_argument('--country_code_path', help='Path to the file containing the list of country codes', default='country_codes.txt')
    parser.add_argument('--output_dir', help='Path to save the outputted files', default='output/')

    args = parser.parse_args()

    with open(args.key_path, 'r') as file:
        api_key = file.readline().strip()

    with open(args.country_code_path, 'r') as file:
        country_codes = [line.strip() for line in file]

    scraper = YouTubeScraper(api_key, country_codes, args.output_dir)
    scraper.scrape_data()