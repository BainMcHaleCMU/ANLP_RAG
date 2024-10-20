import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

# Base URL
base_url = 'https://www.visitpittsburgh.com'

# List to store scraped data
scraped_data = []

# Function to scrape content from a single page
def scrape_page(url):
    try:
        print(f"Scraping {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title (h1 or h2)
            title = soup.find('h1') or soup.find('h2')  # Adjust based on page structure

            # Extract all text within the page (specifically in <main> if available)
            main_content = soup.find('main', class_='content--primary', id='main')
            if main_content:
                description = ' '.join(main_content.stripped_strings)  # Concatenate all text within <main>
            else:
                description = ' '.join(soup.stripped_strings)  # Fallback to extracting all text from the page

            return {
                'title': title.get_text(strip=True) if title else 'No Title',
                'description': description if description else 'No Description'
            }
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return None

# DFS-like function to recursively scrape links, with max depth limit and parent restriction
def dfs_scrape(url, visited, depth, max_depth):
    if depth > max_depth:
        return  # Stop the recursion if max depth is reached
    if url in visited:
        return  # Avoid revisiting the same page

    visited.add(url)

    # Scrape the current page
    page_data = scrape_page(url)
    if page_data:
        scraped_data.append(page_data)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the <main> section with the specific class and id
            main_content = soup.find('main', class_='content--primary', id='main')

            if main_content:
                # Find all links within the <main> section
                for link in main_content.find_all('a', href=True):
                    next_url = link['href']

                    # Ignore anchor links and invalid URLs
                    if next_url.startswith('#') or 'javascript:' in next_url:
                        continue

                    # Ensure all links are within the https://www.visitpittsburgh.com domain
                    if next_url.startswith('/'):
                        next_url = urljoin(base_url, next_url)
                    elif not next_url.startswith(base_url):
                        # Ignore external links
                        continue

                    print(f"Found link: {next_url}")
                    # Perform DFS on the next page with incremented depth
                    dfs_scrape(next_url, visited, depth + 1, max_depth)
                    time.sleep(1)  # Respectful scraping
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
    except Exception as e:
        print(f"Error while scraping links from {url}: {e}")

# Start the DFS scraping from the main page with max depth limit
start_url = 'https://www.visitpittsburgh.com/things-to-do/pittsburgh-sports-teams/'
visited = set()
max_depth = 1  # Set the maximum depth here

# Start scraping
dfs_scrape(start_url, visited, depth=0, max_depth=max_depth)

# Save the scraped data to a JSON file
with open('sports_general.json', 'w', encoding='utf-8') as json_file:
    json.dump(scraped_data, json_file, ensure_ascii=False, indent=2)

print(f"Scraped {len(scraped_data)} pages.")
