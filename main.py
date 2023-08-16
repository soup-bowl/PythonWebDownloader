import os
import argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

# Function to download a file
def download_file(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Download images and zip files from a website.")
parser.add_argument("url", help="URL of the website to scrape")
parser.add_argument("--dry-run", action="store_true", help="Print URLs instead of downloading")
args = parser.parse_args()

# Send a GET request to the webpage
response = requests.get(args.url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all image and zip file URLs on the page
image_urls = []
zip_urls = []

for img_tag in soup.find_all('img'):
    img_url = urljoin(args.url, img_tag['src'])
    image_urls.append(img_url)

for link_tag in soup.find_all('a'):
    href = link_tag.get('href')
    if href.lower().endswith('.zip'):
        zip_url = urljoin(args.url, href)
        zip_urls.append(zip_url)

# Create a directory to save the downloaded files
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Check for existing files before downloading
downloaded_files = os.listdir('downloads')
existing_filenames = set([filename.lower() for filename in downloaded_files])

# Download images
for img_url in image_urls:
    img_filename = os.path.basename(img_url)
    if img_filename.lower() not in existing_filenames:
        if args.dry_run:
            print(f"Image would be downloaded: {img_url}")
        else:
            img_save_path = os.path.join('downloads', img_filename)
            download_file(img_url, img_save_path)
            print(f"Downloaded image: {img_url}")

# Download zip files
for zip_url in zip_urls:
    zip_filename = os.path.basename(zip_url)
    if zip_filename.lower() not in existing_filenames:
        if args.dry_run:
            print(f"Zip file would be downloaded: {zip_url}")
        else:
            zip_save_path = os.path.join('downloads', zip_filename)
            download_file(zip_url, zip_save_path)
            print(f"Downloaded zip file: {zip_url}")

print("Download and extraction completed.")
