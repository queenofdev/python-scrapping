import json
import requests
import os
from bs4 import BeautifulSoup
import logging

def setup_directory(base_dir, sub_dir):
    path = os.path.join(base_dir, sub_dir)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def fetch_latest_news(url, folder_name, sub_folder):
    base_path = setup_directory(folder_name, sub_folder)

    logging.info(f"Fetching latest news from: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to fetch news from {url}. HTTP Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('h2')

    for i, headline in enumerate(headlines):
        if headline.text:
            file_path = os.path.join(base_path, f"{i+1}.json")
            with open(file_path, "w") as file:
                json.dump({"headline": headline.text}, file, indent=4, sort_keys=True)

    logging.info(f"Saved {len(headlines)} news headlines in separate files.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting crypto news fetching.")

    news_url = "https://www.coindesk.com/"
    folder_name = "Coindesk"
    sub_folder = "2023-11-22"

    fetch_latest_news(news_url, folder_name, sub_folder)
