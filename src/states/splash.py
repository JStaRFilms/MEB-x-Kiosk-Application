"""
MEB-x Splash State

Displays the EU logo during startup.
"""

import pygame
from src.states.base_state import BaseState


class SplashState(BaseState):
    """State for showing the splash screen."""

    def __init__(self):
        super().__init__()
        self.timer = 3.0  # 3 seconds
        self.logo = pygame.image.load('assets/images/eu_logo.png')

    def update(self, dt: float):
        self.timer -= dt
        if self.timer <= 0:
            self.should_transition = True
            self.next_state = 'DASHBOARD'

    def handle_events(self, events: list):
        # Splash screen doesn't respond to events
        pass

    def render(self, screen, font):
        screen.fill((0, 0, 0))
        screen.blit(self.logo, (1280 // 2 - 400 // 2, 720 // 2 - 400 // 2))
