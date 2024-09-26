import re
import requests
import os

# Extract URLs from a given text line
def extract_urls(text):
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, text)
    return urls

# Download image content from a given URL
def download_image(url, image_num):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        content_type = response.headers.get('Content-Type')

        # Check if its an actual image
        if content_type and content_type.startswith('image/'):
            # Extract the image extension
            extension = content_type.split('/')[-1]
            
            # Create a directory to save images
            if not os.path.exists('images'):
                os.makedirs('images')
            
            # Save image
            filename = f"images/image_{image_num}.{extension}"
            with open(filename, 'wb') as handler:
                for chunk in response.iter_content(1024):
                    handler.write(chunk)
            
            print(f"🖼️ Image downloaded and saved as {filename}")
        else:
            print(f"URL does not point to a valid image: {url}")
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")

# Function to search for 'dhd' in webpage content, extract URLs, and download images
def search_for_dhd_and_download_images(url):
    url_count = 0  # Initialize the URL counter
    
    try:
        # Fetch the content of the webpage
        response = requests.get(url)
        content = response.text
        
        # Split the content by lines and search for 'dhd'
        for line in content.splitlines():
            if 'dhd' in line:
                # Extract URLs if found in the same line
                urls = extract_urls(line)
                if urls:
                    for img_url in urls:
                        url_count += 1  # Increment counter for each URL found
                        download_image(img_url, url_count)
                else:
                    print("No URLs found in this line.")
                    
        print(f"\nTotal images downloaded: {url_count}")
                    
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")

# Example usage
webpage_url = 'https://storage.googleapis.com/panels-api/data/20240916/media-1a-i-p~s'  # Replace with the URL of the webpage you want to parse
search_for_dhd_and_download_images(webpage_url)
