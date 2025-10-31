"""
MEB-x Books Menu State

Displays a list of available books and handles selection.
"""

import os
import pygame
from src.states.base_state import BaseState


class BooksMenuState(BaseState):
    """State for browsing and selecting books."""

    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(os.path.join('assets', 'fonts', 'default.ttf'), 30)
        self.load_books()
        self.selected_index = 0

        # Navigation key mappings
        self.NAV_UP = '8'
        self.NAV_DOWN = '2'
        self.NAV_SELECT = '5'
        self.NAV_BACK = '*'

    def load_books(self):
        """Scan the books directory for available files."""
        books_dir = os.path.join('content', 'books')
        if not os.path.exists(books_dir):
            os.makedirs(books_dir)
            self.books = []
            return

        # Get all files, filter for common book formats
        all_files = os.listdir(books_dir)
        book_extensions = ['.txt', '.pdf', '.epub', '.docx']
        self.books = [
            f for f in all_files
            if any(f.lower().endswith(ext) for ext in book_extensions)
        ]

    def update(self, dt: float):
        pass  # No animation or timers needed

    def handle_events(self, events: list):
        for event_type, key in events:
            if event_type == 'key_press':
                if key == self.NAV_UP and self.selected_index > 0:
                    self.selected_index -= 1
                elif key == self.NAV_DOWN and self.selected_index < len(self.books) - 1:
                    self.selected_index += 1
                elif key == self.NAV_SELECT and self.books:
                    selected_book = self.books[self.selected_index]
                    print(f"Selected book: {selected_book}")
                    # TODO: Future implementation - open book viewer
                elif key == self.NAV_BACK:
                    self.should_transition = True
                    self.next_state = 'DASHBOARD'

    def render(self, screen, ui_font):
        screen.fill((0, 0, 0))
        width, height = screen.get_size()

        # Title
        title = self.font.render("Available Books", True, (255, 255, 255))
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        # Display books list
        y_pos = 120
        line_height = 40

        if not self.books:
            no_books = self.font.render("No books available", True, (128, 128, 128))
            screen.blit(no_books, (width // 2 - no_books.get_width() // 2,
                                   height // 2 - no_books.get_height() // 2))
            return

        # Calculate visible range (simple implementation, shows all for now)
        for i, book in enumerate(self.books):
            color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)

            # Truncate long filenames for display
            display_name = book[:35] + '...' if len(book) > 35 else book
            text = self.font.render(display_name, True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, y_pos))
            y_pos += line_height

            # Stop if running off screen
            if y_pos > height - 100:
                break
