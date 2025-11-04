"""
MEB-x Videos Menu State

Displays a scrollable list of available videos with proper UI components.
"""

import os
import pygame
from src.states.base_state import BaseState
from src.states.viewer import ViewerState
from src.ui.renderer import UIRenderer
from src.ui.components import Text, ListItem, Scrollbar, DownloadProgress
from src.services.deleted_content_tracker import DeletedContentTracker


class VideosMenuState(BaseState):
    """State for browsing and selecting videos."""

    def __init__(self, downloader=None):
        super().__init__()
        self.renderer = UIRenderer()
        self.renderer.load_fonts(os.path.join('assets', 'fonts', 'default.ttf'))

        self.downloader = downloader
        self.selected_index = 0
        self.scroll_offset = 0
        self.content_check_started = False

        # Navigation key mappings
        self.NAV_UP = '8'
        self.NAV_DOWN = '2'
        self.NAV_SELECT = '5'
        self.NAV_BACK = '*'

        # UI layout constants
        self.item_height = 60
        self.visible_items = 8
        self.list_padding = self.renderer.get_spacing('lg')

        self.load_videos()  # Load existing videos without downloading
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        screen_width, screen_height = 1280, 720

        # Title
        self.title = Text(self.renderer, 0, self.renderer.get_spacing('xl'),
                         "Available Videos", '3xl', 'text_primary', 'center')
        self.title.rect.centerx = screen_width // 2

        # List container dimensions
        list_width = 800
        list_height = self.visible_items * self.item_height
        list_x = (screen_width - list_width) // 2
        list_y = self.title.rect.bottom + self.renderer.get_spacing('lg')

        self.list_x = list_x
        self.list_y = list_y
        self.list_width = list_width
        self.list_height = list_height

        # Scrollbar
        scrollbar_width = 12
        scrollbar_x = list_x + list_width + self.renderer.get_spacing('md')
        scrollbar_y = list_y
        scrollbar_height = list_height

        self.scrollbar = Scrollbar(self.renderer, scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height,
                                  len(self.videos), self.visible_items, self.scroll_offset)

        # Instructions
        self.instructions = Text(self.renderer, 0, screen_height - self.renderer.get_spacing('xl'),
                                "↑↓ Navigate • 5 Select • * Back", 'sm', 'text_muted', 'center')
        self.instructions.rect.centerx = screen_width // 2

        # Status message for empty list
        self.status_message = Text(self.renderer, 0, 0, "", 'lg', 'text_secondary', 'center')
        self.status_message.rect.center = (screen_width // 2, screen_height // 2)

        # Download progress indicator
        progress_width = 400
        progress_height = 60
        progress_x = (screen_width - progress_width) // 2
        progress_y = screen_height - self.renderer.get_spacing('3xl') - progress_height

        self.download_progress = DownloadProgress(self.renderer, progress_x, progress_y,
                                                progress_width, progress_height)
        self.download_progress.visible = False  # Hidden by default

        # Set up progress callback if downloader exists
        if self.downloader:
            self.downloader.progress_callback = self._on_download_progress

    def _on_download_progress(self, filename: str, progress: float):
        """Handle download progress updates."""
        self.download_progress.update_progress(filename, progress)
        self.download_progress.visible = True

        # Hide progress when download completes
        if progress >= 1.0:
            # Keep it visible for a moment, then hide
            pygame.time.set_timer(pygame.USEREVENT + 1, 2000)  # Hide after 2 seconds

    def load_videos(self):
        """Scan the videos directory for available files and include deleted videos for redownload."""
        try:
            videos_dir = os.path.join('content', 'videos')
            if not os.path.exists(videos_dir):
                os.makedirs(videos_dir)

            # Get all files, filter for common video formats
            all_files = os.listdir(videos_dir)
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            available_videos = [
                f for f in all_files
                if any(f.lower().endswith(ext) for ext in video_extensions)
            ]

            # Get deleted videos that can be redownloaded
            tracker = DeletedContentTracker()
            deleted_videos = tracker.get_deleted_files('video')

            # Combine available and deleted videos
            # Available videos come first, then deleted videos with [DELETED] prefix
            self.videos = available_videos.copy()
            self.deleted_videos = []  # Track which videos are deleted for redownload

            for deleted_video in deleted_videos:
                if deleted_video not in available_videos:  # Don't show if already available
                    self.videos.append(f"[DELETED] {deleted_video}")
                    self.deleted_videos.append(deleted_video)

            # Sort alphabetically
            self.videos.sort()
        except Exception as e:
            print(f"Error loading videos: {e}")
            self.videos = []
            self.deleted_videos = []

    def check_for_content_updates(self):
        """Check for content updates asynchronously."""
        if self.downloader and not self.content_check_started:
            self.content_check_started = True
            import threading
            def update_check():
                print("Videos menu: Checking for content updates...")
                self.downloader.check_for_updates()
                # Refresh the video list after updates
                self.load_videos()
                # Update scrollbar with new item count
                if hasattr(self, 'scrollbar'):
                    self.scrollbar.update_scroll(self.scroll_offset, len(self.videos), self.visible_items)

            thread = threading.Thread(target=update_check, daemon=True)
            thread.start()

    def update_scroll(self):
        """Update scroll position based on selected index."""
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.visible_items:
            self.scroll_offset = self.selected_index - self.visible_items + 1

        self.scrollbar.update_scroll(self.scroll_offset, len(self.videos), self.visible_items)

    def update(self, dt: float):
        # Start content update check on first update (after UI is initialized)
        if not self.content_check_started:
            self.check_for_content_updates()

    def handle_events(self, events: list):
        for event_type, key in events:
            if event_type == 'key_press':
                if key == self.NAV_UP and self.selected_index > 0:
                    self.selected_index -= 1
                    self.update_scroll()
                elif key == self.NAV_DOWN and self.selected_index < len(self.videos) - 1:
                    self.selected_index += 1
                    self.update_scroll()
                elif key == self.NAV_SELECT and self.videos:
                    selected_video = self.videos[self.selected_index]

                    # Check if this is a deleted video that needs redownloading
                    if selected_video.startswith("[DELETED] "):
                        actual_filename = selected_video[10:]  # Remove "[DELETED] " prefix
                        if self.downloader:
                            print(f"Redownloading deleted video: {actual_filename}")
                            success = self.downloader.redownload_deleted_content('video', actual_filename, self._on_download_progress)
                            if success:
                                # Refresh the video list to show the redownloaded video
                                self.load_videos()
                                # Update scrollbar
                                if hasattr(self, 'scrollbar'):
                                    self.scrollbar.update_scroll(self.scroll_offset, len(self.videos), self.visible_items)
                                print(f"Successfully redownloaded: {actual_filename}")
                            else:
                                print(f"Failed to redownload: {actual_filename}")
                        else:
                            print("No downloader available for redownload")
                    else:
                        # Normal video selection
                        video_path = os.path.join('content', 'videos', selected_video)
                        ViewerState.set_pending_content('video', video_path, selected_video)
                        self.should_transition = True
                        self.next_state = 'VIEWER'
                elif key == self.NAV_BACK:
                    self.should_transition = True
                    self.next_state = 'DASHBOARD'

    def render(self, screen, ui_font):
        # Clear screen with background
        screen.fill(self.renderer.get_color('background'))

        # Render title
        self.title.render(screen)

        if not self.videos:
            # Show status message
            self.status_message.set_text("No videos available")
            self.status_message.render(screen)

            # Show downloading status
            downloading_msg = Text(self.renderer, 0, self.status_message.rect.bottom + self.renderer.get_spacing('md'),
                                  "Content downloading in background...", 'base', 'text_muted', 'center')
            downloading_msg.rect.centerx = 1280 // 2
            downloading_msg.render(screen)
            return

        # Render visible list items
        start_idx = self.scroll_offset
        end_idx = min(start_idx + self.visible_items, len(self.videos))

        for i in range(start_idx, end_idx):
            item_idx = i - start_idx
            item_y = self.list_y + (item_idx * self.item_height)

            # Create list item component
            is_selected = (i == self.selected_index)
            item = ListItem(self.renderer, self.list_x, item_y, self.list_width, self.item_height,
                           self.videos[i][:50] + '...' if len(self.videos[i]) > 50 else self.videos[i],
                           is_selected)
            item.render(screen)

        # Render scrollbar
        self.scrollbar.render(screen)

        # Render instructions
        self.instructions.render(screen)

        # Render download progress if active
        self.download_progress.render(screen)
