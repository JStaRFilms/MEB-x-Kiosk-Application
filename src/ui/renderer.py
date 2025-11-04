"""
MEB-x UI Renderer

Handles all Pygame drawing calls and provides utilities for consistent UI rendering.
"""

import pygame
import math


class UIRenderer:
    """Handles UI rendering utilities and constants."""

    def __init__(self):
        # Color palette (RGB tuples)
        self.colors = {
            'background': (255, 255, 255),      # White
            'surface': (248, 250, 252),         # Light gray
            'primary': (37, 99, 235),           # Blue
            'primary_hover': (29, 78, 216),     # Darker blue
            'secondary': (107, 114, 128),       # Gray
            'accent': (16, 185, 129),           # Green
            'text_primary': (17, 24, 39),       # Dark gray
            'text_secondary': (75, 85, 99),     # Medium gray
            'text_muted': (107, 114, 128),      # Light gray
            'border': (229, 231, 235),          # Very light gray
            'border_focus': (37, 99, 235),      # Blue
            'error': (239, 68, 68),             # Red
            'success': (16, 185, 129),          # Green
            'warning': (245, 158, 11),          # Yellow
        }

        # Typography scale (font sizes in pixels)
        self.font_sizes = {
            'xs': 12,
            'sm': 14,
            'base': 16,
            'lg': 18,
            'xl': 20,
            '2xl': 24,
            '3xl': 30,
            '4xl': 36,
            '5xl': 48,
            '6xl': 60,
        }

        # Spacing scale (8px grid system)
        self.spacing = {
            'xs': 4,
            'sm': 8,
            'md': 16,
            'lg': 24,
            'xl': 32,
            '2xl': 48,
            '3xl': 64,
        }

        # Border radius
        self.border_radius = {
            'none': 0,
            'sm': 4,
            'md': 8,
            'lg': 12,
            'xl': 16,
            'full': 9999,
        }

        # Initialize fonts (will be set by load_fonts)
        self.fonts = {}

    def load_fonts(self, font_path: str):
        """Load fonts at different sizes."""
        for name, size in self.font_sizes.items():
            try:
                self.fonts[name] = pygame.font.Font(font_path, size)
            except Exception as e:
                print(f"Error loading font {name} ({size}px): {e}")
                # Fallback to default font
                self.fonts[name] = pygame.font.SysFont('arial', size)

    def get_color(self, name: str) -> tuple:
        """Get RGB color tuple by name."""
        return self.colors.get(name, (0, 0, 0))

    def get_font(self, size: str = 'base'):
        """Get font by size name."""
        return self.fonts.get(size, self.fonts.get('base', pygame.font.SysFont('arial', 16)))

    def get_spacing(self, size: str = 'md') -> int:
        """Get spacing value by name."""
        return self.spacing.get(size, 16)

    def draw_rect(self, screen, color_name: str, rect: pygame.Rect, border_radius: str = 'none'):
        """Draw a rounded rectangle."""
        color = self.get_color(color_name)
        radius = self.border_radius.get(border_radius, 0)

        if radius > 0:
            # Draw rounded rectangle
            pygame.draw.rect(screen, color, rect, border_radius=radius)
        else:
            pygame.draw.rect(screen, color, rect)

    def draw_border(self, screen, rect: pygame.Rect, color_name: str = 'border',
                   width: int = 1, border_radius: str = 'none'):
        """Draw a border around a rectangle."""
        color = self.get_color(color_name)
        radius = self.border_radius.get(border_radius, 0)

        # Create a slightly larger rect for the border
        border_rect = rect.inflate(width * 2, width * 2)
        inner_rect = rect

        if radius > 0:
            pygame.draw.rect(screen, color, border_rect, width, border_radius=radius)
        else:
            pygame.draw.rect(screen, color, border_rect, width)

    def draw_text(self, screen, text: str, position: tuple, font_size: str = 'base',
                 color_name: str = 'text_primary', align: str = 'left'):
        """Draw text with specified styling."""
        font = self.get_font(font_size)
        color = self.get_color(color_name)

        text_surface = font.render(text, True, color)

        if align == 'center':
            x = position[0] - text_surface.get_width() // 2
            y = position[1] - text_surface.get_height() // 2
        elif align == 'right':
            x = position[0] - text_surface.get_width()
            y = position[1] - text_surface.get_height() // 2
        else:  # left
            x = position[0]
            y = position[1] - text_surface.get_height() // 2

        screen.blit(text_surface, (x, y))

        return text_surface.get_rect(topleft=(x, y))

    def draw_shadow(self, screen, rect: pygame.Rect, blur: int = 4, opacity: int = 30):
        """Draw a simple shadow effect."""
        shadow_color = (0, 0, 0, opacity)
        shadow_surface = pygame.Surface((rect.width + blur * 2, rect.height + blur * 2), pygame.SRCALPHA)
        shadow_rect = pygame.Rect(blur, blur, rect.width, rect.height)

        # Simple shadow - could be enhanced with blur effect
        pygame.draw.rect(shadow_surface, shadow_color, shadow_rect, border_radius=8)

        screen.blit(shadow_surface, (rect.x - blur, rect.y - blur))

    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color string to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb: tuple) -> str:
        """Convert RGB tuple to hex color string."""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
