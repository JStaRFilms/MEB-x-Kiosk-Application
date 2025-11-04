"""
MEB-x Dashboard State

Displays the main dashboard with Books and Videos cards.
"""

import pygame
import os
from src.states.base_state import BaseState
from src.ui.renderer import UIRenderer
from src.ui.components import Card, Text


class DashboardState(BaseState):
    """State for the main dashboard UI."""

    def __init__(self):
        super().__init__()
        self.renderer = UIRenderer()
        self.renderer.load_fonts(os.path.join('assets', 'fonts', 'default.ttf'))

        # Focus state (0 = Books, 1 = Videos)
        self.focused_index = 0

        # Initialize UI components
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        screen_width, screen_height = 1280, 720

        # Title
        self.title = Text(self.renderer, 0, self.renderer.get_spacing('3xl'),
                         "MEB-x Educational Content", '4xl', 'text_primary', 'center')
        self.title.rect.centerx = screen_width // 2

        # Card dimensions and spacing
        card_width = 400
        card_height = 200
        card_spacing = self.renderer.get_spacing('xl')
        total_width = (card_width * 2) + card_spacing
        start_x = (screen_width - total_width) // 2
        card_y = screen_height // 2 - card_height // 2

        # Books card
        self.books_card = Card(self.renderer, start_x, card_y, card_width, card_height,
                              'surface', 'border', 'lg', True)
        self.books_title = Text(self.renderer, 0, 0, "Books", '2xl', 'text_primary', 'center')
        self.books_title.rect.center = self.books_card.rect.center
        self.books_subtitle = Text(self.renderer, 0, 0, "Educational Materials",
                                  'base', 'text_secondary', 'center')
        self.books_subtitle.rect.centerx = self.books_card.rect.centerx
        self.books_subtitle.rect.top = self.books_title.rect.bottom + self.renderer.get_spacing('sm')

        # Videos card
        videos_x = start_x + card_width + card_spacing
        self.videos_card = Card(self.renderer, videos_x, card_y, card_width, card_height,
                               'surface', 'border', 'lg', True)
        self.videos_title = Text(self.renderer, 0, 0, "Videos", '2xl', 'text_primary', 'center')
        self.videos_title.rect.center = self.videos_card.rect.center
        self.videos_subtitle = Text(self.renderer, 0, 0, "Multimedia Content",
                                   'base', 'text_secondary', 'center')
        self.videos_subtitle.rect.centerx = self.videos_card.rect.centerx
        self.videos_subtitle.rect.top = self.videos_title.rect.bottom + self.renderer.get_spacing('sm')

        # Instructions
        self.instructions = Text(self.renderer, 0, screen_height - self.renderer.get_spacing('3xl'),
                                "Use 1/2 to select • Press 5 to confirm", 'sm', 'text_muted', 'center')
        self.instructions.rect.centerx = screen_width // 2

    def update(self, dt: float):
        pass  # No animation or timers needed

    def handle_events(self, events: list):
        for event_type, key in events:
            if event_type == 'key_press':
                if key == '1':
                    self.focused_index = 0  # Focus Books
                elif key == '2':
                    self.focused_index = 1  # Focus Videos
                elif key == '5':  # Select/Confirm
                    if self.focused_index == 0:
                        self.should_transition = True
                        self.next_state = 'BOOKS_MENU'
                    elif self.focused_index == 1:
                        self.should_transition = True
                        self.next_state = 'VIDEOS_MENU'

    def render(self, screen, font):
        # Clear screen with background
        screen.fill(self.renderer.get_color('background'))

        # Update card borders based on focus
        books_border = 'border_focus' if self.focused_index == 0 else 'border'
        videos_border = 'border_focus' if self.focused_index == 1 else 'border'

        self.books_card.border_color = books_border
        self.videos_card.border_color = videos_border

        # Render components
        self.title.render(screen)
        self.books_card.render(screen)
        self.videos_card.render(screen)
        self.books_title.render(screen)
        self.books_subtitle.render(screen)
        self.videos_title.render(screen)
        self.videos_subtitle.render(screen)
        self.instructions.render(screen)
