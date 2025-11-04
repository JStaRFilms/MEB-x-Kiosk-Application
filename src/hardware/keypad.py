"""
MEB-x Keypad Handler

Provides interface for the 3x4 matrix keypad.

This module supports dual-mode functionality:
- On Linux (Raspberry Pi): Uses hardware keypad via gpiozero library with GPIO pins.
- On other systems (e.g., Windows for development): Uses a mock keypad via pygame to simulate keyboard input.
  Keyboard mappings for mock keypad:
  Primary (Numpad keys - recommended):
  - NumPad 1,2,3 → '1','2','3'
  - NumPad 4,5,6 → '4','5','6'
  - NumPad 7,8,9 → '7','8','9'
  - NumPad 0 → '0'
  - NumPad * → '*'
  - NumPad / → '#'
  - NumPad Enter → '5' (select)
  Fallback (Alternative keys):
  - Top-row 1,2,3,4,5,6,7,8,9,0 → same numbers
  - Main keyboard * → '*'
  - Main keyboard / → '#'
  - Enter/Return → '5' (select)
  - Spacebar → '5' (select)
  - Escape → '*' (back)
"""

import platform
import time

try:
    import pygame
    pygame_available = True
except ImportError:
    pygame_available = False

if platform.system() == 'Linux':
    from gpiozero import Button, OutputDevice


class MockKeypad:
    """
    Mock keypad implementation using pygame for keyboard input simulation.
    Used on non-Linux systems (e.g., Windows) for development and testing.
    """

    def __init__(self):
        if not pygame_available:
            raise ImportError("pygame is required for mock keypad on non-Linux systems. Please install: pip install pygame")
        pygame.init()
        # Key mappings: pygame key constants to keypad characters
        # Primary mappings: numpad keys (preferred)
        self.key_mappings = {
            pygame.K_KP1: '1',
            pygame.K_KP2: '2',
            pygame.K_KP3: '3',
            pygame.K_KP4: '4',
            pygame.K_KP5: '5',
            pygame.K_KP6: '6',
            pygame.K_KP7: '7',
            pygame.K_KP8: '8',
            pygame.K_KP9: '9',
            pygame.K_KP0: '0',
            pygame.K_KP_MULTIPLY: '*',
            pygame.K_KP_DIVIDE: '#',  # Using divide as # since numpad doesn't have #
            pygame.K_KP_ENTER: '5',   # Enter key as alternative select
        }

        # Fallback mappings: top-row number keys and common alternatives
        self.fallback_mappings = {
            pygame.K_1: '1',
            pygame.K_2: '2',
            pygame.K_3: '3',
            pygame.K_4: '4',
            pygame.K_5: '5',
            pygame.K_6: '6',
            pygame.K_7: '7',
            pygame.K_8: '8',
            pygame.K_9: '9',
            pygame.K_0: '0',
            # Special keys - using common keyboard alternatives
            pygame.K_ASTERISK: '*',  # * key on main keyboard
            pygame.K_HASH: '#',      # # key if available
            pygame.K_BACKSLASH: '*', # \ key as alternative *
            pygame.K_SLASH: '#',     # / key as alternative #
            pygame.K_RETURN: '5',    # Enter key as select
            pygame.K_SPACE: '5',     # Spacebar as select
            pygame.K_ESCAPE: '*',    # Escape as back
        }

    def get_key(self, pygame_events=None):
        """
        Poll pygame events and return keypad character or None.

        Args:
            pygame_events: List of pygame events to check (optional, for compatibility)

        Returns:
            str or None: Keypad character if a mapped key is pressed, else None.
        """
        events_to_check = pygame_events if pygame_events is not None else pygame.event.get()
        for event in events_to_check:
            if event.type == pygame.KEYDOWN:
                # Check primary mappings first (numpad keys)
                if event.key in self.key_mappings:
                    return self.key_mappings[event.key]
                # Check fallback mappings (top-row number keys)
                elif event.key in self.fallback_mappings:
                    return self.fallback_mappings[event.key]
        return None


class Keypad:
    def __init__(self):
        if platform.system() == 'Linux':
            # Raspberry Pi with hardware keypad
            self.hardware = True
            self.row_pins = [18, 19, 20]  # GPIO input pins for rows
            self.col_pins = [12, 13, 16, 26]  # GPIO output pins for columns

            # Keypad mapping (3 rows x 4 columns)
            self.key_map = [
                ['1', '2', '3', 'A'],
                ['4', '5', '6', 'B'],
                ['7', '8', '9', 'C']
            ]

            # Setup rows as buttons with pull-up
            self.rows = [Button(pin, pull_up=True) for pin in self.row_pins]
            # Setup columns as outputs
            self.cols = [OutputDevice(pin) for pin in self.col_pins]

            # Set all columns high initially
            for col in self.cols:
                col.on()
        else:
            # Development machine with mock keypad
            self.hardware = False
            self.mock = MockKeypad()

    def get_key(self, pygame_events=None):
        """
        Scan the keypad and return the pressed key character or None.

        On Linux: Scans hardware keypad matrix.
        On other systems: Polls pygame events for keyboard input.

        Args:
            pygame_events: List of pygame events to check (optional, passed from main loop)

        Returns:
            str or None: The key character pressed or None if no key is pressed.
        """
        if self.hardware:
            # Hardware keypad scanning logic
            for col_idx, col in enumerate(self.cols):
                # Set other columns high
                for other_col in self.cols:
                    if other_col != col:
                        other_col.on()
                # Set current column low
                col.off()
                time.sleep(0.01)  # Small delay for settling
                # Check each row
                for row_idx, row in enumerate(self.rows):
                    if row.is_pressed == False:  # Row is low (pressed)
                        col.on()  # Restore high
                        return self.key_map[row_idx][col_idx]
                # Restore column high
                col.on()
            return None
        else:
            # Mock keypad: delegate to MockKeypad
            return self.mock.get_key(pygame_events)
