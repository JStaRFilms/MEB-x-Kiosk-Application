"""
MEB-x Content Downloader Service

Handles downloading of books and videos from remote source using filename-based versioning.
Supports direct downloads and YouTube videos.
"""

import os
import json
import requests
import yt_dlp
from .deleted_content_tracker import DeletedContentTracker


class ContentDownloader:
    """Handles content downloading from remote source."""

    def __init__(self, config, progress_callback=None):
        """
        Initialize the content downloader.

        Args:
            config (dict): Configuration dictionary from app_config.json
            progress_callback (callable): Optional callback for progress updates
                                         Signature: callback(filename, progress_float)
        """
        self.config = config
        self.progress_callback = progress_callback
        self.deleted_tracker = DeletedContentTracker()

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
                # Add options to avoid bot detection
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                    'Referer': 'https://www.youtube.com/',
                },
                # Add sleep interval to avoid rate limiting
                'sleep_interval': 1,
                'max_sleep_interval': 5,
                # Additional anti-bot measures
                'cookiesfrombrowser': None,  # Don't use browser cookies
                'ignoreerrors': True,
                'no_check_certificate': False,
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

                # Determine local directory and content type for tracker
                if item_type == 'book':
                    local_dir = 'content/books/'
                    tracker_type = 'book'
                elif item_type == 'video':
                    local_dir = 'content/videos/'
                    tracker_type = 'video'
                else:
                    print(f"Warning: Unknown content type '{item_type}' for item '{name}'. Skipping.")
                    continue

                # Check if this file was previously deleted by user
                if self.deleted_tracker.should_skip_download(tracker_type, name):
                    print(f"Content item '{name}' was previously deleted by user. Skipping download.")
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

                        # Get total file size for progress calculation
                        total_size = int(file_response.headers.get('content-length', 0))
                        downloaded_size = 0

                        # Stream download to file with progress updates
                        with open(local_path, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    downloaded_size += len(chunk)

                                    # Report progress if callback is available
                                    if self.progress_callback and total_size > 0:
                                        progress = downloaded_size / total_size
                                        self.progress_callback(name, min(progress, 1.0))

                        success = True

                        # Final progress update
                        if self.progress_callback:
                            self.progress_callback(name, 1.0)

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

    def check_for_updates(self):
        """Quick check for content updates without full logging."""
        try:
            # Fetch data from source URL
            response = requests.get(self.config['source_url'], timeout=5)
            response.raise_for_status()

            # Parse JSON array
            content_items = response.json()
            new_items_found = 0

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

                if not file_exists:
                    new_items_found += 1
                    # Download immediately
                    print(f"Menu-triggered download: '{name}'...")
                    success = False

                    if self._is_youtube_url(url):
                        print(f"Detected YouTube URL, using yt-dlp for '{name}'...")
                        base_path = os.path.splitext(local_path)[0]
                        success = self._download_youtube_video(url, base_path)
                    else:
                        try:
                            file_response = requests.get(url, timeout=10, stream=True)
                            file_response.raise_for_status()

                            with open(local_path, 'wb') as f:
                                for chunk in file_response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            success = True

                        except requests.RequestException as e:
                            print(f"Error downloading '{name}': {e}")
                            success = False

                    if success:
                        print(f"Successfully downloaded '{name}'")
                    else:
                        print(f"Failed to download '{name}'")

            if new_items_found == 0:
                print("Menu check: No new content available")
            else:
                print(f"Menu check: Downloaded {new_items_found} new items")

        except Exception as e:
            print(f"Menu update check failed: {e}")

    def redownload_deleted_content(self, content_type: str, filename: str, progress_callback=None) -> bool:
        """
        Manually redownload a previously deleted file.

        Args:
            content_type: 'book' or 'video'
            filename: Name of the file to redownload
            progress_callback: Optional callback for progress updates

        Returns:
            True if redownload was successful
        """
        try:
            # Fetch current content list to find the file
            response = requests.get(self.config['source_url'], timeout=10)
            response.raise_for_status()

            content_items = response.json()

            # Find the matching item
            target_item = None
            for item in content_items:
                if item.get('name') == filename and item.get('type') == content_type:
                    target_item = item
                    break

            if not target_item:
                print(f"File '{filename}' not found in remote content list")
                return False

            # Determine local directory
            if content_type == 'book':
                local_dir = 'content/books/'
            elif content_type == 'video':
                local_dir = 'content/videos/'
            else:
                print(f"Unknown content type: {content_type}")
                return False

            # Ensure directory exists
            os.makedirs(local_dir, exist_ok=True)

            url = target_item.get('url')
            local_path = os.path.join(local_dir, filename)

            print(f"Redownloading '{filename}'...")
            success = False

            if self._is_youtube_url(url):
                print(f"Detected YouTube URL, using yt-dlp for '{filename}'...")
                base_path = os.path.splitext(local_path)[0]
                success = self._download_youtube_video(url, base_path)
            else:
                try:
                    file_response = requests.get(url, timeout=10, stream=True)
                    file_response.raise_for_status()

                    total_size = int(file_response.headers.get('content-length', 0))
                    downloaded_size = 0

                    with open(local_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)

                                if progress_callback and total_size > 0:
                                    progress = downloaded_size / total_size
                                    progress_callback(filename, min(progress, 1.0))

                    success = True

                    if progress_callback:
                        progress_callback(filename, 1.0)

                except requests.RequestException as e:
                    print(f"Error redownloading '{filename}': {e}")
                    success = False

            if success:
                # Remove from deleted list since it's now restored
                self.deleted_tracker.mark_as_restored(content_type, filename)
                print(f"Successfully redownloaded '{filename}'")
                return True
            else:
                print(f"Failed to redownload '{filename}'")
                return False

        except Exception as e:
            print(f"Error in redownload: {e}")
            return False
