import feedparser
import os
import requests
import logging
import time

# Configure logging
logging.basicConfig(filename='news_usa_rss.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Define the RSS feed URLs for each station (USA news)
rss_feed_urls = {
    "hits247": "https://www.spreaker.com/show/3371228/episodes/feed",
    "viralfm": "https://www.spreaker.com/show/3371228/episodes/feed",
    "ForeverworldFM": "https://www.spreaker.com/show/3371228/episodes/feed"
}

# Define the base directory for AzuraCast media
base_directory = "/mnt/smb_share/Azura_media"

# Define the directories for each radio station
station_directories = {
    "hits247": os.path.join(base_directory, "hits247", "News"),
    "viralfm": os.path.join(base_directory, "viralfm", "News"),
    "ForeverworldFM": os.path.join(base_directory, "ForeverworldFM", "News"),
    "rmf_fm": os.path.join(base_directory, "rmf_fm", "News")
}

# URL for the MP3 file provided by Sky News (UK news)
sky_news_mp3_url = "https://video.news.sky.com/snr/news/snrnews.mp3"

def download_and_distribute():
    # Download and distribute episodes for USA news stations
    for station, rss_feed_url in rss_feed_urls.items():
        # Parse the RSS feed
        feed = feedparser.parse(rss_feed_url)

        # Check if there are any entries in the feed
        if feed.entries:
            # Get the first entry (most recent episode)
            entry = feed.entries[0]
            
            # Extract episode title and MP3 URL
            episode_title = entry.title
            mp3_url = entry.enclosures[0].href

            # Download the MP3 file
            response = requests.get(mp3_url)
            if response.status_code == 200:
                print(f"Downloading episode for {station}: {episode_title}")
                logging.info(f"Downloading episode for {station}: {episode_title}")

                # Get the directory for the station
                directory = station_directories.get(station)

                if directory:
                    # Create the directory if it doesn't exist
                    os.makedirs(directory, exist_ok=True)

                    # Generate the file path
                    file_path = os.path.join(directory, "hourly_news.mp3")

                    # Save the MP3 file (overwrite existing file if it exists)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    print(f"Episode downloaded and distributed to {station} station.")
                    logging.info(f"Episode downloaded and distributed to {station} station.")
                else:
                    print(f"Directory not found for {station}.")
                    logging.error(f"Directory not found for {station}.")
            else:
                print(f"Failed to download the episode for {station}.")
                logging.error(f"Failed to download the episode for {station}.")
        else:
            print(f"No episodes found in the RSS feed for {station}.")
            logging.warning(f"No episodes found in the RSS feed for {station}.")

    # Download and distribute episode for the UK news station (rmf_fm)
    response = requests.get(sky_news_mp3_url)
    if response.status_code == 200:
        print("Downloading episode for rmf_fm: UK News")
        logging.info("Downloading episode for rmf_fm: UK News")

        # Get the directory for the station
        directory = station_directories.get("rmf_fm")

        if directory:
            # Create the directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)

            # Generate the file path
            file_path = os.path.join(directory, "hourly_news.mp3")

            # Save the MP3 file (overwrite existing file if it exists)
            with open(file_path, 'wb') as f:
                f.write(response.content)

            print("Episode downloaded and distributed to rmf_fm station.")
            logging.info("Episode downloaded and distributed to rmf_fm station.")
        else:
            print("Directory not found for rmf_fm.")
            logging.error("Directory not found for rmf_fm.")
    else:
        print("Failed to download the episode for rmf_fm.")
        logging.error("Failed to download the episode for rmf_fm.")

    print("Waiting for the next update...")
    logging.info("Waiting for the next update...")

# Run the script continuously
while True:
    download_and_distribute()
    # Wait for 30 minutes before checking for updates again
    time.sleep(30 * 60)  # 30 minutes in seconds
ending = input("press key to exit"