"""
MEB-x Content Downloader Service

Handles downloading of books and videos from remote source using filename-based versioning.
Supports direct downloads and YouTube videos.
"""

import os
import json
import requests
import yt_dlp


class ContentDownloader:
    """Handles content downloading from remote source."""

    def __init__(self, config):
        """
        Initialize the content downloader.

        Args:
            config (dict): Configuration dictionary from app_config.json
        """
        self.config = config

    def _is_youtube_url(self, url):
        """Check if URL is from YouTube or YouTube-like platforms."""
        youtube_domains = [
            'youtube.com', 'youtu.be', 'youtube-nocookie.com',
            'm.youtube.com', 'music.youtube.com'
        ]
        return any(domain in url.lower() for domain in youtube_domains)

    def _download_youtube_video(self, url, output_path):
        """Download YouTube video using yt-dlp."""
        try:
            ydl_opts = {
                'outtmpl': output_path,
                'format': 'best[height<=720]',  # Limit to 720p for kiosk
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"YouTube download error: {e}")
            return False

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

                # Check if file already exists (handle YouTube extensions)
                file_exists = False
                if self._is_youtube_url(url):
                    # For YouTube, check if any file with the base name exists
                    base_name = os.path.splitext(name)[0]
                    for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
                        if os.path.exists(os.path.join(local_dir, base_name + ext)):
                            file_exists = True
                            break
                else:
                    file_exists = os.path.exists(local_path)

                if file_exists:
                    print(f"Content item '{name}' already exists. Skipping download.")
                    continue

                # Download the file
                print(f"Downloading new content item: '{name}'...")
                success = False

                if self._is_youtube_url(url):
                    # Use yt-dlp for YouTube videos
                    print(f"Detected YouTube URL, using yt-dlp for '{name}'...")
                    # yt-dlp will automatically add extension, so we need to handle the filename
                    base_path = os.path.splitext(local_path)[0]  # Remove extension if present
                    success = self._download_youtube_video(url, base_path)
                else:
                    # Use regular HTTP download for other URLs
                    try:
                        file_response = requests.get(url, timeout=10, stream=True)
                        file_response.raise_for_status()

                        # Stream download to file
                        with open(local_path, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        success = True

                    except requests.RequestException as e:
                        print(f"Error downloading '{name}': {e}")
                        success = False

                if not success:
                    print(f"Failed to download '{name}', skipping...")
                    continue

            print("Content check finished.")

        except requests.RequestException as e:
            print(f"Network error fetching content list: {e}")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response: {e}")
        except Exception as e:
            print(f"Unexpected error in content downloader: {e}")
