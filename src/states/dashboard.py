"""
MEB-x Dashboard State

Displays the main dashboard with Books and Videos options.
"""

import pygame
from src.states.base_state import BaseState


class DashboardState(BaseState):
    """State for the main dashboard UI."""

    def __init__(self):
        super().__init__()
        self.bg = pygame.image.load('assets/images/background.png')
        self.selected = 'books'  # 'books' or 'videos'

    def update(self, dt: float):
        pass  # No timer needed

    def handle_events(self, events: list):
        for event_type, key in events:
            if event_type == 'key_press':
                if key == '1':
                    self.selected = 'books'
                elif key == '2':
                    self.selected = 'videos'
                # For MUS, no further action

    def render(self, screen, font):
        screen.blit(self.bg, (0, 0))
        books_color = (255, 255, 255) if self.selected == 'books' else (128, 128, 128)
        videos_color = (255, 255, 255) if self.selected == 'videos' else (128, 128, 128)

        books_text = font.render('Books', True, books_color)
        videos_text = font.render('Videos', True, videos_color)

        screen.blit(books_text, (1280 // 2 - books_text.get_width() // 2, 720 // 3))
        screen.blit(videos_text, (1280 // 2 - videos_text.get_width() // 2, 720 * 2 // 3))
