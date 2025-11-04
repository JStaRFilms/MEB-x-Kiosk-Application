"""
MEB-x Splash State

Displays the EU logo during startup with styled background.
"""

import pygame
import os
from src.states.base_state import BaseState
from src.ui.renderer import UIRenderer


class SplashState(BaseState):
    """State for showing the splash screen."""

    def __init__(self):
        super().__init__()
        self.timer = 3.0  # 3 seconds
        self.renderer = UIRenderer()
        self.renderer.load_fonts(os.path.join('assets', 'fonts', 'default.ttf'))

        # Load logo
        try:
            self.logo = pygame.image.load('assets/images/eu_logo.png')
            # Scale logo to appropriate size (300x300 for better proportion)
            self.logo = pygame.transform.smoothscale(self.logo, (300, 300))
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Create fallback logo
            self.logo = pygame.Surface((300, 300))
            self.logo.fill(self.renderer.get_color('primary'))

    def update(self, dt: float):
        self.timer -= dt
        if self.timer <= 0:
            self.should_transition = True
            self.next_state = 'DASHBOARD'

    def handle_events(self, events: list):
        # Splash screen doesn't respond to events
        pass

    def render(self, screen, font):
        # Clear screen with styled background
        screen.fill(self.renderer.get_color('background'))

        # Center the logo
        screen_width, screen_height = screen.get_size()
        logo_x = screen_width // 2 - self.logo.get_width() // 2
        logo_y = screen_height // 2 - self.logo.get_height() // 2

        screen.blit(self.logo, (logo_x, logo_y))

        # Optional: Add app title below logo
        title_text = "MEB-x Educational Kiosk"
        title_y = logo_y + self.logo.get_height() + self.renderer.get_spacing('lg')
        self.renderer.draw_text(screen, title_text, (screen_width // 2, title_y),
                               'lg', 'text_secondary', 'center')
