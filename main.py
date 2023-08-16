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

# Print or download resources based on --dry-run flag
if args.dry_run:
    print("Image URLs:")
    for img_url in image_urls:
        print(img_url)

    print("Zip file URLs:")
    for zip_url in zip_urls:
        print(zip_url)
else:
    # Create a directory to save the downloaded files
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Download images
    for img_url in image_urls:
        img_filename = os.path.join('downloads', os.path.basename(img_url))
        download_file(img_url, img_filename)
        print(f"Downloaded image: {img_url}")

    # Download zip files
    for zip_url in zip_urls:
        zip_filename = os.path.join('downloads', os.path.basename(zip_url))
        download_file(zip_url, zip_filename)
        print(f"Downloaded zip file: {zip_url}")

    # Extract zip files
    for zip_filename in os.listdir('downloads'):
        if zip_filename.lower().endswith('.zip'):
            with zipfile.ZipFile(os.path.join('downloads', zip_filename), 'r') as zip_ref:
                zip_ref.extractall('downloads')
                print(f"Extracted contents of {zip_filename}")

    print("Download and extraction completed.")
