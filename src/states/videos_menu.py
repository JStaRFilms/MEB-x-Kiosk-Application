"""
MEB-x Videos Menu State

Displays a list of available videos and handles selection.
"""

import os
import pygame
from src.states.base_state import BaseState


class VideosMenuState(BaseState):
    """State for browsing and selecting videos."""

    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(os.path.join('assets', 'fonts', 'default.ttf'), 30)
        self.load_videos()
        self.selected_index = 0

        # Navigation key mappings
        self.NAV_UP = '8'
        self.NAV_DOWN = '2'
        self.NAV_SELECT = '5'
        self.NAV_BACK = '*'

    def load_videos(self):
        """Scan the videos directory for available files."""
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
        except Exception as e:
            print(f"Error loading videos: {e}")
            self.videos = []

    def update(self, dt: float):
        pass  # No animation or timers needed

    def handle_events(self, events: list):
        for event_type, key in events:
            if event_type == 'key_press':
                if key == self.NAV_UP and self.selected_index > 0:
                    self.selected_index -= 1
                elif key == self.NAV_DOWN and self.selected_index < len(self.videos) - 1:
                    self.selected_index += 1
                elif key == self.NAV_SELECT and self.videos:
                    selected_video = self.videos[self.selected_index]
                    print(f"Selected video: {selected_video}")
                    # TODO: Future implementation - open video player
                elif key == self.NAV_BACK:
                    self.should_transition = True
                    self.next_state = 'DASHBOARD'

    def render(self, screen, ui_font):
        screen.fill((0, 0, 0))
        width, height = screen.get_size()

        # Title
        title = self.font.render("Available Videos", True, (255, 255, 255))
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        # Display videos list
        y_pos = 120
        line_height = 40

        if not self.videos:
            no_videos = self.font.render("No videos available", True, (128, 128, 128))
            screen.blit(no_videos, (width // 2 - no_videos.get_width() // 2,
                                    height // 2 - no_videos.get_height() // 2))

            # Show downloading status message
            downloading_msg = self.font.render("Content downloading in background...", True, (100, 100, 100))
            screen.blit(downloading_msg, (width // 2 - downloading_msg.get_width() // 2,
                                         height // 2 - downloading_msg.get_height() // 2 + 50))
            return

        # Calculate visible range (simple implementation, shows all for now)
        for i, video in enumerate(self.videos):
            color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)

            # Truncate long filenames for display
            display_name = video[:35] + '...' if len(video) > 35 else video
            text = self.font.render(display_name, True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, y_pos))
            y_pos += line_height

            # Stop if running off screen
            if y_pos > height - 100:
                break
