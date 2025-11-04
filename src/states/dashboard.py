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

    def update(self, dt: float):
        pass  # No timer needed

    def handle_events(self, events: list):
        for event_type, key in events:
            if event_type == 'key_press':
                if key == '1':
                    self.should_transition = True
                    self.next_state = 'BOOKS_MENU'
                elif key == '2':
                    self.should_transition = True
                    self.next_state = 'VIDEOS_MENU'

    def render(self, screen, font):
        screen.blit(self.bg, (0, 0))

        books_text = font.render('Books', True, (255, 255, 255))
        videos_text = font.render('Videos', True, (255, 255, 255))

        screen.blit(books_text, (1280 // 2 - books_text.get_width() // 2, 720 // 3))
        screen.blit(videos_text, (1280 // 2 - videos_text.get_width() // 2, 720 * 2 // 3))
