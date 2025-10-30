"""
MEB-x Base State Class

Abstract base class for all application states.
"""

from abc import ABC, abstractmethod


class BaseState(ABC):
    """Base class for all states in the MEB-x application."""

    def __init__(self):
        self.should_transition = False
        self.next_state = None

    @abstractmethod
    def update(self, dt: float):
        """
        Update the state logic (e.g., timers).

        Args:
            dt (float): Time elapsed since last update in seconds.
        """
        pass

    @abstractmethod
    def handle_events(self, events: list):
        """
        Handle events such as keypad presses.

        Args:
            events (list): List of events, e.g., [('key_press', '1')].
        """
        pass

    @abstractmethod
    def render(self, screen, font):
        """
        Render the state's UI to the screen.

        Args:
            screen: Pygame screen surface to draw on.
            font: Pygame font object for text rendering.
        """
        pass
