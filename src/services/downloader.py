"""
MEB-x Content Downloader Service

Handles downloading of books and videos from remote source using filename-based versioning.
"""

import os
import json
import requests


class ContentDownloader:
    """Handles content downloading from remote source."""

    def __init__(self, config):
        """
        Initialize the content downloader.

        Args:
            config (dict): Configuration dictionary from app_config.json
        """
        self.config = config

    def check_and_download_content(self):
        """Fetch content list and download new items."""
        try:
            # Fetch data from source URL
            response = requests.get(self.config['source_url'], timeout=10)
            response.raise_for_status()

            # Parse JSON array
            content_items = response.json()

            # Process each item
            for item in content_items:
                name = item.get('name')
                item_type = item.get('type')
                url = item.get('url')

                # Determine local directory
                if item_type == 'book':
                    local_dir = 'content/books/'
                elif item_type == 'video':
                    local_dir = 'content/videos/'
                else:
                    print(f"Warning: Unknown content type '{item_type}' for item '{name}'. Skipping.")
                    continue

                # Ensure directory exists
                os.makedirs(local_dir, exist_ok=True)

                # Construct full local path
                local_path = os.path.join(local_dir, name)

                # Check if file already exists
                if os.path.exists(local_path):
                    print(f"Content item '{name}' already exists. Skipping download.")
                    continue

                # Download the file
                print(f"Downloading new content item: '{name}'...")
                try:
                    file_response = requests.get(url, timeout=10, stream=True)
                    file_response.raise_for_status()

                    # Stream download to file
                    with open(local_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)

                except requests.RequestException as e:
                    print(f"Error downloading '{name}': {e}")
                    continue

            print("Content check finished.")

        except requests.RequestException as e:
            print(f"Network error fetching content list: {e}")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response: {e}")
        except Exception as e:
            print(f"Unexpected error in content downloader: {e}")
