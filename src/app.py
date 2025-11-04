"""
MEB-x Main Application

State-machine driven kiosk application for Raspberry Pi.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame
from pygame.locals import *
import platform
import json
import threading
import time

from src.hardware.keypad import Keypad
from src.states.splash import SplashState
from src.states.dashboard import DashboardState
from src.states.books_menu import BooksMenuState
from src.states.videos_menu import VideosMenuState
from src.states.viewer import ViewerState
from src.services.downloader import ContentDownloader


def main():
    """Main application entry point."""
    # Set working directory to project root
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    pygame.init()

    # Load configuration
    config = {}
    try:
        with open(os.path.join('config', 'app_config.json'), 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")

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

    # Start content downloader if configured
    downloader = None
    if 'content' in config and config['content'].get('enabled', False):
        print("Starting background content downloader...")
        downloader = ContentDownloader(config['content'])

        def run_downloader_periodically():
            while True:
                downloader.check_and_download_content()
                time.sleep(config['content']['check_interval_hours'] * 3600)

        downloader_thread = threading.Thread(target=run_downloader_periodically, daemon=True)
        downloader_thread.start()

    # Initialize states
    states = {
        'SPLASH': SplashState(),
        'DASHBOARD': DashboardState(),
        'BOOKS_MENU': BooksMenuState(downloader),
        'VIDEOS_MENU': VideosMenuState(downloader)
    }

    # Set up progress callbacks for menu states (will be handled by individual states)
    # The progress callback is set up in each menu state's __init__ method

    current_state = states['SPLASH']
    current_state_id = 'SPLASH'

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # 60 FPS

        # Get all pygame events
        pygame_events = pygame.event.get()

        # Handle pygame events for system (QUIT, etc.)
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False

        # Poll keypad for key presses (pass events to keypad)
        key = keypad.get_key(pygame_events)
        events = []
        if key:
            events.append(('key_press', key))

        # Update current state
        current_state.handle_events(events)
        current_state.update(dt)

        # Check for state transition
        if current_state.should_transition:
            next_state_id = current_state.next_state

            # Handle dynamic VIEWER state creation
            if next_state_id == 'VIEWER':
                current_state = ViewerState()
                states['VIEWER'] = current_state  # Cache it for future use
            else:
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
