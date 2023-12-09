import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to find the first JSON file in the directory
def find_first_json(directory):
    for file in os.listdir(directory):
        if file.endswith(".json"):
            return os.path.join(directory, file)
    return None

# Function to extract headline from JSON file
def extract_headline(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data.get("headline", "")

# Function to create directory based on current date
def create_date_directory(base_directory):
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(base_directory, date_str)
    os.makedirs(path, exist_ok=True)
    return path

def search_google_and_save(headline, save_directory, num_results=15):
    query = headline.replace(" ", "+")
    results = []
    user_agent = {'User-agent': 'Mozilla/5.0'}

    for start in range(0, num_results, 10):
        url = f"https://www.google.com/search?q={query}&start={start}"
        response = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # More precise targeting of search results
        for result in soup.find_all('div', class_='kCrYT'):  # Update class based on Google's structure
            title = result.find('h3')
            if title:
                results.append(title.get_text())

            if len(results) >= num_results:
                break

        if len(results) >= num_results:
            break

    results = results[:num_results]  # Ensure only the desired number of results

    # Saving results to a file
    file_name = f"search_results_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    file_path = os.path.join(save_directory, file_name)
    
    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')



# Main execution
directory = os.getcwd() + '/Coindesk/2023-11-22'  # Change this to your folder path
results_directory = os.path.dirname(os.getcwd()) + '/test'  # Change this to your results folder path

json_file = find_first_json(directory)

if json_file:
    headline = extract_headline(json_file)
    if headline:
        date_directory = create_date_directory(results_directory)
        search_google_and_save(headline, date_directory)
    else:
        print("No headline found in JSON file.")
else:
    print("No JSON file fou3nd in the directory.")
