"""
MEB-x Keypad Handler

Provides interface for the 3x4 matrix keypad using gpiozero.
"""

import platform
from gpiozero import Button, OutputDevice
import time


class Keypad:
    def __init__(self):
        self.is_rpi = 'raspberrypi' in platform.platform().lower()
        self.row_pins = [18, 19, 20]  # GPIO input pins for rows
        self.col_pins = [12, 13, 16, 26]  # GPIO output pins for columns

        # Keypad mapping (3 rows x 4 columns)
        self.key_map = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C']
        ]

        if self.is_rpi:
            # Setup rows as buttons with pull-up
            self.rows = [Button(pin, pull_up=True) for pin in self.row_pins]
            # Setup columns as outputs
            self.cols = [OutputDevice(pin) for pin in self.col_pins]

            # Set all columns high initially
            for col in self.cols:
                col.on()
        else:
            # Not on Pi, no GPIO setup
            self.rows = []
            self.cols = []

    def get_key(self):
        """
        Scan the keypad and return the pressed key character or None.

        Returns:
            str or None: The key character pressed or None if no key is pressed.
        """
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
