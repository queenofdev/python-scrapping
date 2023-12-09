import json
import subprocess
import requests
import logging
import os

from bs4 import BeautifulSoup
from datetime import datetime

def convert_date_format(initial_date):
    # Split the string to separate the date part from the time part
    date_parts = initial_date.split(" at ")

    if len(date_parts) > 1:
        date_string = date_parts[0]  # Extract the date part
        time_string = date_parts[1]  # Extract the time part

        try:
            # Attempt to parse the initial date string with the first format
            parsed_date = datetime.strptime(date_string, '%b %d, %Y')
        except ValueError:
            try:
                # If the first format fails, try parsing with the second format
                parsed_date = datetime.strptime(date_string, '%b %d, %Y at %I:%M %p')
            except ValueError as e:
                # Handle the exception if both formats fail
                print(f"Error: {e}")
                return None

        # Format the parsed date with the time part and UTC timezone
        formatted_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return formatted_date
    else:
        try:
            # Attempt to parse the date without time information
            parsed_date = datetime.strptime(initial_date, '%b %d, %Y')
        except ValueError as e:
            print(f"Error: {e}")
            return None
        
        # Format the parsed date without time to the desired format
        formatted_date = parsed_date.strftime('%Y-%m-%dT00:00:00.000Z')
        return formatted_date


# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Assuming news headlines are in <h2> tags (this may vary based on the website structure)
    results = []
    index = 0
    for result in soup.find_all('a', class_='card-title-link'):  # Update class based on Google's structure
        title = result.find('h2')

        if title:
            sub_url = url + result['href']
            sub_response = requests.get(sub_url)
                    
            if sub_response.status_code != 200:
                logging.error(f"Failed to fetch news from {sub_url}. HTTP Status Code: {sub_response.status_code}")
                return []
            
            sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
            content = sub_soup.find('section', class_="at-body")
            if(sub_soup.find('div', class_="at-authors")):
                author = sub_soup.find('div', class_="at-authors").find('a').get_text()
            else:
                author = "None"
            date = sub_soup.find('span', class_="hcIsFR")
            if(sub_soup.find('div', class_='media')):
                imageUrl = sub_soup.find('div', class_='media').find('img').get("src")
            else:
                imageUrl = "None"

            # delete this when needed
            author = "Satoshi Nakamoto"
            if content:
                data = {
                    "author": author,
                    "content": content.get_text(),
                    "date": convert_date_format(date.get_text()),
                    "imageUrl": imageUrl,
                    "title": title.get_text(),
                }
                file_path = os.path.join(base_path, f"{index + 1}.json")
                with open(file_path, "w") as file:
                    json.dump(data, file)
                results.append(data)
                index += 1

    logging.info(f"Retrieved {len(results)} news headlines.")
    return results

if __name__ == "__main__":
    logging.info("Starting crypto news rephrasing.")
    news_url = "https://www.coindesk.com"

    folder_name = "raw_articles"
    sub_folder = datetime.now().strftime('%Y-%m-%d')

    latest_news = fetch_latest_news(news_url, folder_name, sub_folder)

    # Trigger the rephrase_and_save_news.py script
    subprocess.run(["python", "rephrase_and_save_news.py"])

    logging.info("Triggered rephrase_and_save_news.py.")
