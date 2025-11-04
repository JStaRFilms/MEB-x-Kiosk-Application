"""
MEB-x UI Components

Reusable UI components for consistent interface design.
"""

import pygame
from typing import Optional, Callable


class UIComponent:
    """Base class for all UI components."""

    def __init__(self, renderer, x: int, y: int, width: int, height: int):
        self.renderer = renderer
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True

    def contains_point(self, point: tuple) -> bool:
        """Check if point is within component bounds."""
        return self.rect.collidepoint(point)

    def render(self, screen):
        """Render the component. Override in subclasses."""
        pass

    def handle_event(self, event):
        """Handle events. Override in subclasses."""
        pass


class Card(UIComponent):
    """Card component with background, border, and optional shadow."""

    def __init__(self, renderer, x: int, y: int, width: int, height: int,
                 background_color: str = 'surface', border_color: str = 'border',
                 border_radius: str = 'md', has_shadow: bool = True):
        super().__init__(renderer, x, y, width, height)
        self.background_color = background_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.has_shadow = has_shadow

    def render(self, screen):
        if not self.visible:
            return

        if self.has_shadow:
            self.renderer.draw_shadow(screen, self.rect)

        # Draw background
        self.renderer.draw_rect(screen, self.background_color, self.rect, self.border_radius)

        # Draw border
        self.renderer.draw_border(screen, self.rect, self.border_color, border_radius=self.border_radius)


class Button(UIComponent):
    """Interactive button component."""

    def __init__(self, renderer, x: int, y: int, width: int, height: int,
                 text: str, on_click: Optional[Callable] = None,
                 background_color: str = 'primary', hover_color: str = 'primary_hover',
                 text_color: str = 'background', font_size: str = 'base',
                 border_radius: str = 'md'):
        super().__init__(renderer, x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.background_color = background_color
        self.hover_color = hover_color
        self.current_bg_color = background_color
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius
        self.hovered = False

    def handle_event(self, event):
        if not self.enabled or not self.visible:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.contains_point(event.pos)
            self.current_bg_color = self.hover_color if self.hovered else self.background_color
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains_point(event.pos) and self.on_click:
                self.on_click()

    def render(self, screen):
        if not self.visible:
            return

        # Draw background
        self.renderer.draw_rect(screen, self.current_bg_color, self.rect, self.border_radius)

        # Draw text centered
        center_x = self.rect.centerx
        center_y = self.rect.centery
        self.renderer.draw_text(screen, self.text, (center_x, center_y),
                               self.font_size, self.text_color, 'center')


class Text(UIComponent):
    """Text display component."""

    def __init__(self, renderer, x: int, y: int, text: str,
                 font_size: str = 'base', color: str = 'text_primary',
                 align: str = 'left', max_width: Optional[int] = None):
        # Calculate initial size based on text
        font = renderer.get_font(font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        width = max_width if max_width else text_surface.get_width()
        height = text_surface.get_height()

        super().__init__(renderer, x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.align = align
        self.max_width = max_width

    def set_text(self, text: str):
        """Update the text content."""
        self.text = text
        # Recalculate size if needed
        if not self.max_width:
            font = self.renderer.get_font(self.font_size)
            text_surface = font.render(text, True, (0, 0, 0))
            self.rect.width = text_surface.get_width()

    def render(self, screen):
        if not self.visible:
            return

        self.renderer.draw_text(screen, self.text, (self.rect.x, self.rect.centery),
                               self.font_size, self.color, self.align)


class ListItem(UIComponent):
    """List item component with selection state."""

    def __init__(self, renderer, x: int, y: int, width: int, height: int,
                 text: str, selected: bool = False):
        super().__init__(renderer, x, y, width, height)
        self.text = text
        self.selected = selected
        self.padding = renderer.get_spacing('md')

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.selected = selected

    def render(self, screen):
        if not self.visible:
            return

        # Background color based on selection
        bg_color = 'primary' if self.selected else 'surface'
        text_color = 'background' if self.selected else 'text_primary'

        # Draw background
        self.renderer.draw_rect(screen, bg_color, self.rect, 'md')

        # Draw border if selected
        if self.selected:
            self.renderer.draw_border(screen, self.rect, 'border_focus', border_radius='md')

        # Draw text with padding
        text_x = self.rect.x + self.padding
        text_y = self.rect.centery
        self.renderer.draw_text(screen, self.text, (text_x, text_y),
                               'base', text_color, 'left')


class Scrollbar(UIComponent):
    """Vertical scrollbar component."""

    def __init__(self, renderer, x: int, y: int, width: int, height: int,
                 total_items: int, visible_items: int, current_scroll: int = 0):
        super().__init__(renderer, x, y, width, height)
        self.total_items = total_items
        self.visible_items = visible_items
        self.current_scroll = current_scroll
        self.thumb_height = max(20, (visible_items / max(total_items, 1)) * height)
        self.thumb_y = y + (current_scroll / max(total_items - visible_items, 1)) * (height - self.thumb_height)

    def update_scroll(self, current_scroll: int, total_items: int = None, visible_items: int = None):
        """Update scroll position and optionally item counts."""
        if total_items is not None:
            self.total_items = total_items
        if visible_items is not None:
            self.visible_items = visible_items

        self.current_scroll = max(0, min(current_scroll, max(self.total_items - self.visible_items, 0)))
        self.thumb_height = max(20, (self.visible_items / max(self.total_items, 1)) * self.rect.height)
        scrollable_range = max(self.total_items - self.visible_items, 1)
        self.thumb_y = self.rect.y + (self.current_scroll / scrollable_range) * (self.rect.height - self.thumb_height)

    def render(self, screen):
        if not self.visible or self.total_items <= self.visible_items:
            return

        # Draw track
        track_color = 'border'
        self.renderer.draw_rect(screen, track_color, self.rect, 'full')

        # Draw thumb
        thumb_rect = pygame.Rect(self.rect.x, int(self.thumb_y),
                                self.rect.width, int(self.thumb_height))
        thumb_color = 'secondary'
        self.renderer.draw_rect(screen, thumb_color, thumb_rect, 'full')


class ProgressBar(UIComponent):
    """Progress bar component."""

    def __init__(self, renderer, x: int, y: int, width: int, height: int,
                 progress: float = 0.0, background_color: str = 'border',
                 fill_color: str = 'primary', border_radius: str = 'full'):
        super().__init__(renderer, x, y, width, height)
        self.progress = max(0.0, min(1.0, progress))
        self.background_color = background_color
        self.fill_color = fill_color
        self.border_radius = border_radius

    def set_progress(self, progress: float):
        """Set progress value (0.0 to 1.0)."""
        self.progress = max(0.0, min(1.0, progress))

    def render(self, screen):
        if not self.visible:
            return

        # Draw background
        self.renderer.draw_rect(screen, self.background_color, self.rect, self.border_radius)

        # Draw fill
        if self.progress > 0:
            fill_width = int(self.rect.width * self.progress)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            self.renderer.draw_rect(screen, self.fill_color, fill_rect, self.border_radius)


class DownloadProgress(UIComponent):
    """Download progress indicator with filename and progress bar."""

    def __init__(self, renderer, x: int, y: int, width: int, height: int,
                 filename: str = "", progress: float = 0.0):
        super().__init__(renderer, x, y, width, height)
        self.filename = filename
        self.progress = progress
        self.bar_height = 8
        self.padding = renderer.get_spacing('sm')

        # Create progress bar
        bar_y = y + height - self.bar_height - self.padding
        self.progress_bar = ProgressBar(renderer, x + self.padding, bar_y,
                                       width - 2 * self.padding, self.bar_height,
                                       progress, 'border', 'accent', 'sm')

    def update_progress(self, filename: str, progress: float):
        """Update download progress."""
        self.filename = filename
        self.progress = progress
        self.progress_bar.set_progress(progress)

    def render(self, screen):
        if not self.visible:
            return

        # Draw filename text
        if self.filename:
            display_name = self.filename[:40] + '...' if len(self.filename) > 40 else self.filename
            text_rect = self.renderer.draw_text(screen, f"Downloading: {display_name}",
                                               (self.rect.x + self.padding, self.rect.y + self.padding),
                                               'sm', 'text_primary', 'left')

        # Draw progress bar
        self.progress_bar.render(screen)

        # Draw progress percentage
        percent_text = f"{int(self.progress * 100)}%"
        self.renderer.draw_text(screen, percent_text,
                               (self.rect.right - self.padding, self.rect.y + self.padding),
                               'sm', 'text_secondary', 'right')
