"""
MEB-x Content Downloader

Handles automatic downloading of books and videos from configured source.
"""

import json
import hashlib
import os
import threading
import time
import requests
from datetime import datetime


class ContentDownloader:
    """Handles periodic content downloading from remote source."""

    def __init__(self, config):
        """
        Initialize the content downloader.

        Args:
            config (dict): Content configuration from app_config.json
        """
        self.config = config
        os.makedirs(os.path.join('content', 'books'), exist_ok=True)
        os.makedirs(os.path.join('content', 'videos'), exist_ok=True)

    def _log(self, message):
        """Simple logging to console with timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Content Downloader: {message}")

    def check_connectivity(self):
        """
        Check for internet connectivity.

        Returns:
            bool: True if connected, False otherwise
        """
        try:
            # Test DNS resolution and connectivity to Google DNS
            response = requests.head('https://dns.google', timeout=10, allow_redirects=True)
            return response.status_code == 200
        except Exception as e:
            self._log(f"Connectivity check failed: {e}")
            return False

    def download_content(self):
        """Download new or updated content if configured and online."""
        if not self.config.get('enabled', False):
            return

        if not self.check_connectivity():
            self._log("No internet connection, skipping download")
            return

        metadata_file = os.path.join('content', 'local_metadata.json')

        # Load local metadata
        local_metadata = {}
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r') as f:
                    local_metadata = json.load(f)
            except Exception as e:
                self._log(f"Error loading metadata: {e}")

        self._log("Checking for content updates...")

        try:
            # Fetch content list from API
            response = requests.get(
                self.config['source_url'],
                timeout=self.config.get('timeout_seconds', 60)
            )
            response.raise_for_status()

            # Assume the API returns a list of content items
            # Each item should have: name, type ('book' or 'video'), url, hash
            remote_files = response.json()

            downloaded_count = 0

            for file_info in remote_files:
                try:
                    fname = file_info['name']
                    ftype = file_info['type']  # 'book' or 'video'
                    furl = file_info['url']
                    fhash = file_info['hash']

                    # Determine local directory
                    local_dir = os.path.join('content', ftype + 's')
                    local_path = os.path.join(local_dir, fname)

                    # Check if file already exists and is up-to-date
                    needs_download = True
                    if os.path.exists(local_path):
                        with open(local_path, 'rb') as f:
                            existing_hash = hashlib.md5(f.read()).hexdigest()
                        if existing_hash == fhash:
                            needs_download = False

                    if needs_download:
                        # Download the file
                        file_response = requests.get(
                            furl,
                            timeout=self.config.get('timeout_seconds', 60)
                        )
                        file_response.raise_for_status()

                        # Save the file
                        with open(local_path, 'wb') as f:
                            f.write(file_response.content)

                        # Update metadata
                        local_metadata[fname] = fhash
                        downloaded_count += 1
                        self._log(f"Downloaded {fname} to {ftype}s")

                except Exception as e:
                    self._log(f"Error downloading {fname}: {e}")
                    continue

            if downloaded_count > 0:
                # Save updated metadata
                with open(metadata_file, 'w') as f:
                    json.dump(local_metadata, f, indent=2)
                self._log(f"Download complete, {downloaded_count} files updated")
            else:
                self._log("No new content to download")

        except requests.RequestException as e:
            self._log(f"Network error during content check: {e}")
        except json.JSONDecodeError as e:
            self._log(f"Invalid JSON response from server: {e}")
        except Exception as e:
            self._log(f"Unexpected error: {e}")

    def background_loop(self):
        """Infinite loop for periodic content checking."""
        while True:
            try:
                self.download_content()
            except Exception as e:
                self._log(f"Error in background loop: {e}")

            # Sleep for configured interval
            interval_seconds = self.config.get('check_interval_hours', 24) * 3600
            time.sleep(interval_seconds)


def start_background_downloader(config):
    """
    Start the background content downloader thread.

    Args:
        config (dict): Content configuration
    """
    downloader = ContentDownloader(config)

    # Check immediately once
    downloader.download_content()

    # Then start background thread
    thread = threading.Thread(target=downloader.background_loop, daemon=True)
    thread.start()
    print("Background content downloader started")
