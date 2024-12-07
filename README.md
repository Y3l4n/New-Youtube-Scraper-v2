# New-Youtube-Scraper-v2
 Trending-Youtube-Scraper's better version

 With (a lot) of references from [Patrick Loeber's youtube-analyzer](https://github.com/patrickloeber/youtube-analyzer)

## This repository is for people in my DS project group. 

Please read everything here (all of it, lots of new stuff).

### Update 7/12

`YoutubeScraper` and `YTStatsProMax` got these additional updates, both scripts support batch processing. 

- Remove `defaultAudioLanguage` (since insignificant and a considerable number of videos don't have it)
- Remove `country` in `channel_statistics` (similar reason to `defaultAudioLanguage`)
- Add in `RECORDED_UTC_TIME` to record the fetching date (in UTC format to match that of YouTube)
- Add in `elapsedDays` to calculate time elapsed (in days) by taking `RECORDED_UTC_TIME` - `publishedAt`.
- Add in `avgDailyViews` to calculate average daily views by taking `viewCount` / `elapsedDays`.

See sample data for more details.

#### Helper functions

Inside `yt_helpers` are helpers function which supports some pre-processing after the data is collected. The `fetch_channel_ids.py` will collect all channel ids from trending videos, store them inside `channel_ids.txt` file. You can use that to batch fetching channel statistics via `YTStatsProMax` class. Will add more helpers but need suggestions.

### Update 4/12

The `scraper_json_AI.py` and `yt_stats_self_test_AI.py` are usable now, they will fetch same channel video_data (for `yt_stats_self_test_AI.py`) and trending video_data (for `scraper_json_AI.py`). See sample data in sample folder.

### New data file format

The `scraper_json.py` file is the OG `scraper_to_use.py` from [my Trending-Youtube-Scraper](https://github.com/Y3l4n/Trending-Youtube-Scraper), but now instead of returning csv rows it now returns json, each bracket is 1 row. See usage in the `scraper_json_imple.py`. See sample in sample_trending_data directory. You guys can suggest more properties here if you like, and I will see to it.

#### Why new data format
Easier to see and process.

### Youtube Channel Scraper 
The `yt_stats_self_test_AI.py` is the scraper class. Read it carefully (the scraper class has some helper method to fetch YT API, so read `yt_stats_self_test.py` will be more understandable, that's my experiment file). I've explained how each method works, and logic in both files. Of course you should watch [the tutorial i sent first](https://www.youtube.com/@patloeber/search?query=YouTube%20Data%20API%20Tutorial) to know how those URLs work. 

The original `yt_stats.py`, if run (use `yt_stats_imple.py`), it will return a json of what is fetchable from a channel. My modified script chooses the most analyze-able things (I think so).

`yt_stats_self_test_imple.py` is where I use the scraper class. It still works with the `api_key.txt`, but replace  `country_codes.txt` with `channel_id.txt`. The script is written to support processing multiple channels. See sample in sample_youtube_statistics directory. 

#### How to get channel IDs

After you watch those tutorials, you will know that there are channel IDs in YouTube Statistics. But now it's username policy, so here's how you can get the channel IDs.

Just use this website: https://ytlarge.com/youtube/channel-id-finder/ (much easier + there are some additional channel stats that we can add in our data)

### Further notification

All data files will be updated more in the future (but I myself am not positive that I will fix the scripts any further). 
