
# ===============================================
# Web Crawler for Search Engine Project
# Author: PARTHKUMAR PATEL
# Description:
# This script starts from a given URL (the seed) and downloads HTML pages.
# It follows links to other pages on the same site and saves up to 10 pages.
# These pages are stored in 'input_pages/' and used for the search engine.
# ===============================================

import requests  # To fetch web pages
from bs4 import BeautifulSoup  # To parse and extract links from HTML
from urllib.parse import urljoin, urlparse  # For handling and joining URLs
import os  # For file and folder operations

# === Configuration ===
SEED_URL = "https://en.wikipedia.org/"  # Starting URL for crawling (can be changed)
MAX_PAGES = 10  # Maximum number of pages to download
SAVE_DIR = "input_pages"  # Folder where pages will be saved

# Keep track of all the URLs we've already visited to avoid duplicates
visited = set()

# === Function: is_valid_link ===
# Checks if a URL points to the same domain or is a relative link
def is_valid_link(url, base_netloc):
    return urlparse(url).netloc == base_netloc or urlparse(url).netloc == ''

# === Function: crawl ===
# Downloads one page, saves it, then finds and follows links on that page
def crawl(url, base_url, count=0):
    # Stop if max limit is reached or we've already visited the URL
    if count >= MAX_PAGES or url in visited:
        return count

    try:
        # Try to fetch the web page
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch: {url} (status code {response.status_code})")
            return count
        html = response.text  # Get HTML content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return count

    # Mark the URL as visited
    visited.add(url)

    # Save the HTML content to a file (like page1.html, page2.html...)
    filename = os.path.join(SAVE_DIR, f"page{count+1}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Saved: {url} → {filename}")
    count += 1  # Increase the count

    # Parse the HTML and look for all the <a href="..."> links
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a", href=True):
        # Convert relative links to full URLs
        next_url = urljoin(base_url, link['href'])
        # Check if the new link is valid and hasn't been visited yet
        if next_url not in visited and is_valid_link(next_url, urlparse(base_url).netloc):
            count = crawl(next_url, base_url, count)  # Recursively crawl the next URL
            if count >= MAX_PAGES:
                break  # Stop crawling if we've saved enough pages

    return count  # Return the number of pages saved

# === Main Program Start ===
if __name__ == "__main__":
    # Make sure the folder for saving pages exists
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    print(f"🌐 Starting crawl from: {SEED_URL}")
    print(f"📥 Saving up to {MAX_PAGES} pages in: {SAVE_DIR}")

    # Start the crawling process
    crawl(SEED_URL, SEED_URL)

    print("✅ Crawling complete.")
