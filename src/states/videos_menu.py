"""
MEB-x Videos Menu State

Displays a scrollable list of available videos with proper UI components.
"""

import os
import pygame
from src.states.base_state import BaseState
from src.ui.renderer import UIRenderer
from src.ui.components import Text, ListItem, Scrollbar


class VideosMenuState(BaseState):
    """State for browsing and selecting videos."""

    def __init__(self, downloader=None):
        super().__init__()
        self.renderer = UIRenderer()
        self.renderer.load_fonts(os.path.join('assets', 'fonts', 'default.ttf'))

        self.downloader = downloader
        self.selected_index = 0
        self.scroll_offset = 0

        # Navigation key mappings
        self.NAV_UP = '8'
        self.NAV_DOWN = '2'
        self.NAV_SELECT = '5'
        self.NAV_BACK = '*'

        # UI layout constants
        self.item_height = 60
        self.visible_items = 8
        self.list_padding = self.renderer.get_spacing('lg')

        self.load_videos()
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

    def load_videos(self):
        """Scan the videos directory for available files."""
        # Check for content updates when entering the menu
        if self.downloader:
            print("Videos menu: Checking for content updates...")
            self.downloader.check_for_updates()

        try:
            videos_dir = os.path.join('content', 'videos')
            if not os.path.exists(videos_dir):
                os.makedirs(videos_dir)
                self.videos = []
                return

            # Get all files, filter for common video formats
            all_files = os.listdir(videos_dir)
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            self.videos = [
                f for f in all_files
                if any(f.lower().endswith(ext) for ext in video_extensions)
            ]
            # Sort alphabetically
            self.videos.sort()
        except Exception as e:
            print(f"Error loading videos: {e}")
            self.videos = []

    def update_scroll(self):
        """Update scroll position based on selected index."""
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.visible_items:
            self.scroll_offset = self.selected_index - self.visible_items + 1

        self.scrollbar.update_scroll(self.scroll_offset, len(self.videos), self.visible_items)

    def update(self, dt: float):
        pass  # No animation or timers needed

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
                    print(f"Selected video: {selected_video}")
                    # TODO: Future implementation - open video player
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
