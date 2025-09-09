# Python Libraries Assignment
import requests
import os
from urllib.parse import urlparse

def is_image_url(url):
    # Check if the URL points to a common image type.Returns True if URL ends with an image extension.

    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg")
    return url.lower().endswith(image_extensions)

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Ask the user for directory name
    dir_name = input("Please enter a directory name to save images (default: Fetched_Images): ").strip()
    if not dir_name:
        dir_name = "Fetched_Images"
    
    # Create directory if it doesn't exist
    os.makedirs(dir_name, exist_ok=True)
    
    # Get multiple URLs from user
    urls = input("Please enter one or more image URLs, separated by spaces: ").split()

    success_count = 0
    failure_count = 0
    
    # Loop through each URL in the list
    for url in urls:
        # Skip non-image URLs
        if not is_image_url(url):
            print(f"✗ Skipping non-image URL: {url}")
            failure_count += 1
            continue
        try:
            # Add headers to mimic a browser
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

            # Fetch the image
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes

            # Check Content-Type header to ensure it's an actual image
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"⚠ Skipped: {url} does not contain an image (Content-Type: {content_type})")
                failure_count += 1
                continue
            
            # Extract filename from URL or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "downloaded_image.jpg"
            
            # Check if file exists and rename if necessary
            filepath = os.path.join(dir_name, filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filename = f"{base}_{counter}{ext}"
                filepath = os.path.join(dir_name, filename)
                counter += 1
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")
            print("\nConnection strengthened. Community enriched.")
            success_count += 1
        
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error for {url}: {e}")
            failure_count += 1
        except Exception as e:
            print(f"✗ An error occurred for {url}: {e}")
            failure_count += 1
    
    # Summary
    print("\nSummary:")
    print(f"✓ Images downloaded successfully: {success_count}")
    print(f"✗ Images failed to download: {failure_count}")

if __name__ == "__main__":
    main()
