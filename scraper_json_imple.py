import scraper_json
from scraper_json import YouTubeScraper

with open('api_key.txt', 'r') as file:
    api_key = file.readline().strip()

with open('country_codes.txt', 'r') as file:
    country_codes = [line.strip() for line in file]

# Create an instance of the YouTubeScraper class
scraper = YouTubeScraper(api_key=api_key, country_codes=country_codes, output_dir="trending_data_output")

# Run the scraper
scraper.scrape_data()

print("Scraping complete! JSON files have been saved in the output directory.")