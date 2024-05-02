import requests
from bs4 import BeautifulSoup
import csv
import logging

# Set up logging
logging.basicConfig(filename='linkedin_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_linkedin_data_with_api(first_name, last_name):
    try:
        # Define headers with LinkedIn API token
        headers = {
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        # Send a GET request to LinkedIn API
        response = requests.get(f"https://api.linkedin.com/v2/people/?firstName={first_name}&lastName={last_name}", headers=headers)
        response.raise_for_status()  # Raise exception for any HTTP error

        # Extract data from JSON response
        data = response.json()
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')

        # Write data to CSV
        with open('linkedin_data_api.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['FirstName', 'LastName']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'FirstName': first_name, 'LastName': last_name})

        logging.info('LinkedIn data scraped successfully using API.')
    except Exception as e:
        logging.error(f'Error occurred while scraping LinkedIn data using API: {e}')

def scrape_linkedin_data_with_browser(first_name, last_name):
    try:
        # Send a GET request to LinkedIn search page
        response = requests.get(f"https://www.linkedin.com/search/results/people/?keywords={first_name}%20{last_name}")
        response.raise_for_status()  # Raise exception for any HTTP error

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate search results
        search_results = soup.find_all("li", class_="search-result search-result__occluded-item ember-view")

        # Open CSV file for writing
        with open('linkedin_data_browser.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['FirstName', 'LastName']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Iterate over search results
            for result in search_results[:10]:
                first_name = result.find("span", class_="name actor-name").text.strip()
                last_name = result.find("span", class_="name actor-name").text.strip()
                writer.writerow({'FirstName': first_name, 'LastName': last_name})

        logging.info('LinkedIn data scraped successfully using browser.')
    except Exception as e:
        logging.error(f'Error occurred while scraping LinkedIn data using browser: {e}')

if __name__ == "__main__":
    # Example usage with API
    scrape_linkedin_data_with_api("John", "Doe")

    # Example usage with browser scraping
    scrape_linkedin_data_with_browser("John", "Doe")
