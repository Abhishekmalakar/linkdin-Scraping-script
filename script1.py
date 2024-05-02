import requests
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import urllib.parse
import csv

# Set up logging
logging.basicConfig(filename='linkedin_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def linkedin_data(cookies_dict, first_name, last_name):
    try:
        # Initialize Chrome WebDriver
        driver = webdriver.Chrome()

        # Open LinkedIn homepage
        driver.get("https://www.linkedin.com")

        # Add cookies
        for name, value in cookies_dict.items():
            driver.add_cookie({'name': name, 'value': value})

        # Construct search URL with encoded search query
        search_query = urllib.parse.quote(f"{first_name} {last_name}")
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query}"
        
        # Navigate to the search page
        driver.get(search_url)

        # Wait for search results to load
        sleep(500)  # Adjust waiting time as needed

        # Get the updated page source after waiting
        html = driver.page_source

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract data
        results = []
        for person in soup.find_all("li", class_="reusable-search__result-container"):
            first_name = person.find("p", class_="name actor-name").text.strip()
            last_name = person.find("p", class_="name actor-name").text.strip()
            results.append({'First Name': first_name, 'Last Name': last_name})

        # Close WebDriver
        driver.quit()

        logging.info('LinkedIn data scraped successfully.')
        return results

    except Exception as e:
        logging.error(f'An error occurred while scraping LinkedIn data: {e}')
        return None

def save_to_csv(data):
    try:
        with open("linkedin_data.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ['First Name', 'Last Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        logging.info('Data saved to linkedin_data.csv')
    except Exception as e:
        logging.error(f'An error occurred while saving data to CSV: {e}')

if __name__ == "__main__":
    # Define the cookies_dict with session cookies
    cookies_dict = {
        '_guid': '7728a94f-edac-4971-80b9-ba6ee8147148',
        
    }
    first_name = input("Enter the first name to search: ")
    last_name = input("Enter the last name to search: ")

   
    data = linkedin_data(cookies_dict, first_name, last_name)

    if data:
     
        save_to_csv(data)
    else:
        print("Error occurred while scraping LinkedIn data.")
