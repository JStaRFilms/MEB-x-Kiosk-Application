"""
MEB-x Main Application

State-machine driven kiosk application for Raspberry Pi.
"""

import pygame
from pygame.locals import *
import platform
import os

from src.hardware.keypad import Keypad
from src.states.splash import SplashState
from src.states.dashboard import DashboardState


def main():
    """Main application entry point."""
    pygame.init()

    # Constants
    WIDTH = 1280
    HEIGHT = 720

    # Detect if running on Raspberry Pi
    is_rpi = 'raspberrypi' in platform.platform().lower()

    # Set display mode: fullscreen on Pi, windowed elsewhere
    flags = pygame.FULLSCREEN if is_rpi else 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("MEB-x Kiosk" if not is_rpi else "")

    # Load font
    font = pygame.font.Font(os.path.join('assets', 'fonts', 'default.ttf'), 50)

    # Initialize keypad
    keypad = Keypad()

    # Initialize states
    states = {
        'SPLASH': SplashState(),
        'DASHBOARD': DashboardState()
    }

    current_state = states['SPLASH']
    current_state_id = 'SPLASH'

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # 60 FPS

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Poll keypad for key presses
        key = keypad.get_key()
        events = []
        if key:
            events.append(('key_press', key))

        # Update current state
        current_state.handle_events(events)
        current_state.update(dt)

        # Check for state transition
        if current_state.should_transition:
            next_state_id = current_state.next_state
            current_state = states[next_state_id]
            current_state_id = next_state_id
            # Reset transition flag
            current_state.should_transition = False

        # Render current state
        current_state.render(screen, font)

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
