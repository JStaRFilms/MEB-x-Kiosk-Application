"""
MEB-x Content Viewer State

Displays books (PDF/text) and plays videos using external players.
"""

import os
import subprocess
import threading
import pygame
from src.states.base_state import BaseState
from src.ui.renderer import UIRenderer
from src.ui.components import Text

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False
    print("Warning: PyMuPDF not available. PDF viewing will be limited.")


class ViewerState(BaseState):
    """State for viewing books and playing videos."""

    # Global variables to pass data between states
    _pending_content_type = None
    _pending_content_path = None
    _pending_content_name = None

    @classmethod
    def set_pending_content(cls, content_type, content_path, content_name):
        """Set content to be viewed when state is activated."""
        cls._pending_content_type = content_type
        cls._pending_content_path = content_path
        cls._pending_content_name = content_name

    def __init__(self):
        """Initialize viewer state."""
        super().__init__()
        self.renderer = UIRenderer()
        self.renderer.load_fonts(os.path.join('assets', 'fonts', 'default.ttf'))

        # Get pending content
        self.content_type = self._pending_content_type
        self.content_path = self._pending_content_path
        self.content_name = self._pending_content_name

        # Clear pending content
        self._pending_content_type = None
        self._pending_content_path = None
        self._pending_content_name = None

        # Navigation keys
        self.NAV_EXIT = '*'
        self.NAV_PREV_PAGE = '4'  # Left arrow on keypad
        self.NAV_NEXT_PAGE = '6'  # Right arrow on keypad
        self.NAV_SCROLL_UP = '8'   # Up arrow
        self.NAV_SCROLL_DOWN = '2' # Down arrow

        # Book viewing state
        self.current_page = 0
        self.total_pages = 0
        self.scroll_offset = 0
        self.lines_per_page = 25
        self.pdf_document = None
        self.text_content = []
        self.text_lines = []
        self.pdf_page_images = {}  # Cache for rendered PDF pages

        # Video playing state
        self.video_process = None
        self.video_thread = None

        # UI state
        self.loading = True
        self.error_message = None

        self._init_ui()
        self._load_content()

    def _init_ui(self):
        """Initialize UI components."""
        screen_width, screen_height = 1280, 720

        # Title
        self.title = Text(self.renderer, 0, self.renderer.get_spacing('xl'),
                         f"Viewing: {self.content_name or 'Unknown'}", '2xl', 'text_primary', 'center')
        self.title.rect.centerx = screen_width // 2

        # Loading message
        self.loading_text = Text(self.renderer, 0, 0, "Loading content...", 'lg', 'text_secondary', 'center')
        self.loading_text.rect.center = (screen_width // 2, screen_height // 2)

        # Error message
        self.error_text = Text(self.renderer, 0, 0, "", 'lg', 'error', 'center')
        self.error_text.rect.center = (screen_width // 2, screen_height // 2)

        # Book navigation instructions
        self.book_instructions = Text(self.renderer, 0, screen_height - self.renderer.get_spacing('xl'),
                                     "4/6 Prev/Next Page • 8/2 Scroll • * Exit", 'sm', 'text_muted', 'center')
        self.book_instructions.rect.centerx = screen_width // 2

        # Video instructions
        self.video_instructions = Text(self.renderer, 0, screen_height - self.renderer.get_spacing('xl'),
                                      "Video playing... Press * to exit", 'sm', 'text_muted', 'center')
        self.video_instructions.rect.centerx = screen_width // 2

    def _load_content(self):
        """Load the content based on type."""
        try:
            if self.content_type == 'book':
                self._load_book()
            elif self.content_type == 'video':
                self._load_video()
            else:
                self.error_message = f"Unknown content type: {self.content_type}"
        except Exception as e:
            self.error_message = f"Error loading content: {str(e)}"
        finally:
            self.loading = False

    def _load_book(self):
        """Load book content (PDF or text)."""
        if not os.path.exists(self.content_path):
            self.error_message = "Content file not found"
            return

        file_ext = os.path.splitext(self.content_path)[1].lower()

        if file_ext == '.pdf' and HAS_FITZ:
            # Load PDF
            self.pdf_document = fitz.open(self.content_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = 0
        elif file_ext == '.txt':
            # Load text file
            with open(self.content_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.text_content = f.read()
            self.text_lines = self.text_content.split('\n')
            self.total_pages = max(1, len(self.text_lines) // self.lines_per_page + 1)
            self.current_page = 0
        else:
            self.error_message = f"Unsupported file format: {file_ext}"

    def _load_video(self):
        """Start video playback in a separate thread."""
        if not os.path.exists(self.content_path):
            self.error_message = "Video file not found"
            return

        # Check if any video players are available
        available_players = self._check_available_players()
        if not available_players:
            self.error_message = "No video players available. Please install mpv or omxplayer."
            return

        def play_video():
            try:
                # Try available players
                for player_cmd in available_players:
                    try:
                        print(f"Trying to play video with: {' '.join(player_cmd)}")
                        self.video_process = subprocess.Popen(
                            player_cmd,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        # Don't wait here - let it play in background
                        # We'll check if it's still running in update()
                        print(f"Video player {player_cmd[0]} started successfully")
                        return  # Success, exit the loop
                    except FileNotFoundError:
                        print(f"Player {player_cmd[0]} not found")
                        continue
                    except Exception as e:
                        print(f"Error with player {player_cmd[0]}: {e}")
                        continue

                # If we get here, all players failed
                print("All video players failed to start")
            except Exception as e:
                print(f"Video playback error: {e}")

        self.video_thread = threading.Thread(target=play_video, daemon=True)
        self.video_thread.start()

    def _check_available_players(self):
        """Check which video players are available on the system."""
        players = [
            ['mpv', '--fullscreen', '--no-osc', self.content_path],
            ['omxplayer', '-o', 'hdmi', self.content_path],
            ['vlc', '--fullscreen', '--no-osd', self.content_path],
            ['mplayer', '-fs', self.content_path]
        ]

        available = []
        for player_cmd in players:
            try:
                # Check if the player executable exists
                subprocess.run([player_cmd[0], '--help'],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             timeout=5)
                available.append(player_cmd)
                print(f"Found video player: {player_cmd[0]}")
            except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
                continue

        return available

    def _get_pdf_page_image(self, page_num):
        """Render PDF page as image and return pygame surface."""
        if page_num not in self.pdf_page_images and self.pdf_document:
            try:
                page = self.pdf_document[page_num]
                # Render page at appropriate resolution for 1280x720 screen
                # Calculate zoom to fit page in content area
                screen_width, screen_height = 1280, 720
                content_width = screen_width - 2 * self.renderer.get_spacing('xl')
                content_height = screen_height - 200  # Leave space for title and instructions

                # Get page size
                page_rect = page.rect
                page_width = page_rect.width
                page_height = page_rect.height

                # Calculate zoom to fit
                zoom_x = content_width / page_width
                zoom_y = content_height / page_height
                zoom = min(zoom_x, zoom_y, 2.0)  # Max zoom of 2.0 to prevent too large images

                matrix = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=matrix)

                # Convert to pygame surface
                img_data = pix.tobytes("png")
                from io import BytesIO
                img_bytes = BytesIO(img_data)
                import pygame.image
                surface = pygame.image.load(img_bytes)
                self.pdf_page_images[page_num] = surface
            except Exception as e:
                print(f"Error rendering PDF page {page_num}: {e}")
                return None

        return self.pdf_page_images.get(page_num)

    def _get_current_page_text(self):
        """Get text content for current page."""
        if self.pdf_document:
            # For PDFs, we now render as images, but keep text fallback
            try:
                page = self.pdf_document[self.current_page]
                return page.get_text()
            except Exception as e:
                return f"Error reading PDF page: {e}"
        else:
            # Text file
            start_line = self.current_page * self.lines_per_page
            end_line = min(start_line + self.lines_per_page, len(self.text_lines))
            return '\n'.join(self.text_lines[start_line:end_line])

    def update(self, dt: float):
        # Check video status
        if self.content_type == 'video':
            if self.video_process:
                # Check if video process is still running
                if self.video_process.poll() is not None:
                    # Video process has finished
                    print("Video process finished")
                    self.should_transition = True
                    self.next_state = 'VIDEOS_MENU'
            elif self.video_thread and self.video_thread.is_alive():
                # Video thread is still running but no process started yet
                pass
            elif self.video_thread and not self.video_thread.is_alive():
                # Video thread finished without starting a process (error)
                if not self.error_message:
                    self.error_message = "Failed to start video player"

    def handle_events(self, events: list):
        for event_type, key in events:
            if event_type == 'key_press':
                if key == self.NAV_EXIT:
                    # Clean up video process if running
                    if self.video_process:
                        try:
                            self.video_process.terminate()
                            self.video_process.wait(timeout=2)
                        except:
                            try:
                                self.video_process.kill()
                            except:
                                pass

                    # Return to appropriate menu
                    if self.content_type == 'book':
                        self.next_state = 'BOOKS_MENU'
                    else:
                        self.next_state = 'VIDEOS_MENU'
                    self.should_transition = True

                elif self.content_type == 'book' and not self.loading and not self.error_message:
                    # Book navigation
                    if key == self.NAV_NEXT_PAGE and self.current_page < self.total_pages - 1:
                        self.current_page += 1
                        self.scroll_offset = 0
                    elif key == self.NAV_PREV_PAGE and self.current_page > 0:
                        self.current_page -= 1
                        self.scroll_offset = 0

    def render(self, screen, ui_font):
        # Clear screen with light grey background (2% grey shade)
        screen.fill((230, 230, 230))

        # Render title
        self.title.render(screen)

        if self.loading:
            self.loading_text.render(screen)
            return

        if self.error_message:
            self.error_text.set_text(self.error_message)
            self.error_text.render(screen)
            return

        if self.content_type == 'book':
            self._render_book(screen)
        elif self.content_type == 'video':
            self._render_video_status(screen)

    def _render_book(self, screen):
        """Render book content."""
        screen_width, screen_height = 1280, 720

        # Content area
        content_x = self.renderer.get_spacing('xl')
        content_y = self.title.rect.bottom + self.renderer.get_spacing('lg')
        content_width = screen_width - 2 * content_x
        content_height = screen_height - content_y - self.renderer.get_spacing('3xl')

        if self.pdf_document and HAS_FITZ:
            # Render PDF as image
            page_image = self._get_pdf_page_image(self.current_page)
            if page_image:
                # Center the image in the content area
                img_rect = page_image.get_rect()
                img_rect.centerx = screen_width // 2
                img_rect.centery = content_y + content_height // 2

                # Ensure image doesn't go outside content bounds
                if img_rect.left < content_x:
                    img_rect.left = content_x
                if img_rect.right > screen_width - content_x:
                    img_rect.right = screen_width - content_x
                if img_rect.top < content_y:
                    img_rect.top = content_y
                if img_rect.bottom > content_y + content_height:
                    img_rect.bottom = content_y + content_height

                screen.blit(page_image, img_rect)
            else:
                # Fallback to text rendering if image fails
                self._render_book_text(screen, content_x, content_y, content_width, content_height)
        else:
            # Render text file
            self._render_book_text(screen, content_x, content_y, content_width, content_height)

        # Render page info
        page_info = f"Page {self.current_page + 1} of {self.total_pages}"
        page_text_component = Text(self.renderer, 0, screen_height - self.renderer.get_spacing('2xl'),
                                 page_info, 'sm', 'text_muted', 'center')
        page_text_component.rect.centerx = screen_width // 2
        page_text_component.render(screen)

        # Render instructions
        self.book_instructions.render(screen)

    def _render_book_text(self, screen, content_x, content_y, content_width, content_height):
        """Render book as text (fallback for PDFs or text files)."""
        screen_width, screen_height = 1280, 720

        # Get current page text
        page_text = self._get_current_page_text()

        # Render page text
        font = self.renderer.get_font('base')
        line_height = font.get_linesize()
        max_lines = content_height // line_height

        # Split text into lines that fit
        words = page_text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] <= content_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Render visible lines
        start_line = self.scroll_offset
        end_line = min(start_line + max_lines, len(lines))

        for i in range(start_line, end_line):
            line_idx = i - start_line
            line_y = content_y + line_idx * line_height
            if line_y + line_height > screen_height - self.renderer.get_spacing('xl'):
                break

            line_surface = font.render(lines[i], True, self.renderer.get_color('text_primary'))
            screen.blit(line_surface, (content_x, line_y))

    def _render_video_status(self, screen):
        """Render video playing status."""
        screen_width, screen_height = 1280, 720

        # Status message
        status_text = Text(self.renderer, 0, 0, "Video is playing in full screen", 'lg', 'text_secondary', 'center')
        status_text.rect.center = (screen_width // 2, screen_height // 2)
        status_text.render(screen)

        # Render instructions
        self.video_instructions.render(screen)
