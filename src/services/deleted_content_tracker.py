"""
MEB-x Deleted Content Tracker Service

Tracks files that users have deleted to prevent automatic redownload while allowing manual redownload.
"""

import os
import json
from typing import Dict, List, Set


class DeletedContentTracker:
    """Manages tracking of deleted content files."""

    def __init__(self, tracker_file: str = 'config/deleted_content.json'):
        """
        Initialize the deleted content tracker.

        Args:
            tracker_file: Path to the JSON file storing deleted content info
        """
        self.tracker_file = tracker_file
        self.deleted_content: Dict[str, List[str]] = {}  # content_type -> list of filenames

        # Ensure config directory exists
        os.makedirs(os.path.dirname(tracker_file), exist_ok=True)

        # Load existing deleted content
        self._load_deleted_content()

    def _load_deleted_content(self):
        """Load deleted content from the tracker file."""
        try:
            if os.path.exists(self.tracker_file):
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    self.deleted_content = json.load(f)
            else:
                # Initialize with empty structure
                self.deleted_content = {'book': [], 'video': []}
                self._save_deleted_content()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading deleted content tracker: {e}")
            # Initialize with empty structure on error
            self.deleted_content = {'book': [], 'video': []}

    def _save_deleted_content(self):
        """Save deleted content to the tracker file."""
        try:
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                json.dump(self.deleted_content, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving deleted content tracker: {e}")

    def mark_as_deleted(self, content_type: str, filename: str):
        """
        Mark a file as deleted.

        Args:
            content_type: 'book' or 'video'
            filename: Name of the deleted file
        """
        if content_type not in self.deleted_content:
            self.deleted_content[content_type] = []

        if filename not in self.deleted_content[content_type]:
            self.deleted_content[content_type].append(filename)
            self._save_deleted_content()
            print(f"Marked {filename} as deleted")

    def mark_as_restored(self, content_type: str, filename: str):
        """
        Remove a file from the deleted list (when redownloaded).

        Args:
            content_type: 'book' or 'video'
            filename: Name of the restored file
        """
        if content_type in self.deleted_content and filename in self.deleted_content[content_type]:
            self.deleted_content[content_type].remove(filename)
            self._save_deleted_content()
            print(f"Removed {filename} from deleted list")

    def is_deleted(self, content_type: str, filename: str) -> bool:
        """
        Check if a file is marked as deleted.

        Args:
            content_type: 'book' or 'video'
            filename: Name of the file to check

        Returns:
            True if the file is marked as deleted
        """
        return (content_type in self.deleted_content and
                filename in self.deleted_content[content_type])

    def get_deleted_files(self, content_type: str) -> List[str]:
        """
        Get list of deleted files for a content type.

        Args:
            content_type: 'book' or 'video'

        Returns:
            List of deleted filenames
        """
        return self.deleted_content.get(content_type, [])

    def get_all_deleted_files(self) -> Dict[str, List[str]]:
        """
        Get all deleted files organized by content type.

        Returns:
            Dictionary with content types as keys and lists of filenames as values
        """
        return self.deleted_content.copy()

    def should_skip_download(self, content_type: str, filename: str) -> bool:
        """
        Check if a file should be skipped during download.

        Args:
            content_type: 'book' or 'video'
            filename: Name of the file to check

        Returns:
            True if the file should be skipped (marked as deleted)
        """
        return self.is_deleted(content_type, filename)
