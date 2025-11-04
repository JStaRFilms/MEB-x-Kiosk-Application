# Feature: Content Display System

## 1. Overview

The Content Display System provides a complete content consumption experience for the MEB-x Kiosk, allowing users to browse, select, and view educational content including books (PDF/text) and videos. The system consists of three main components: content browsing menus, a unified content viewer, and external video playback integration.

### User Story
As a user, I want to open and view a selected book or video, so that I can consume the educational material.

### Expected Behavior
Selecting a book or video from its respective list opens it for viewing. For books, this provides a paginated viewer with navigation controls. For videos, this launches a full-screen media player.

## 2. Content Selection and Navigation

### Purpose
The content display system allows users to browse and select between different types of media content (books and videos) from the local content library, providing navigable list interfaces controlled by the 3x4 keypad.

### Dashboard Integration
- **Books Option**: Press '1' to access books menu
- **Videos Option**: Press '2' to access videos menu
- **Navigation**: Clean transition between dashboard and content menus

## 3. Books Menu Implementation

### Purpose
The `Books Menu` feature allows users to browse and select downloaded books from the local content library, providing a navigable list interface controlled by the 3x4 keypad.

### State Architecture
- **BOOKS_MENU State**: State class in `src/states/books_menu.py`
- **Transition Logic**: '1' key from DASHBOARD → BOOKS_MENU → VIEWER (on selection)
- **Navigation Keys**:
  - '8' (up): Scroll up in list
  - '2' (down): Scroll down in list
  - '5' (select): Open selected book in viewer
  - '*' (back): Return to dashboard

### Directory Scanning
- Scans `/content/books` directory for available files
- Supports common book formats: .txt, .pdf, .epub, .docx
- Dynamic list updates after new downloads
- Filename-based titles with truncation for long names

### UI Components
- Centered scrollable list display (800px width, 8 items visible)
- Selection highlighting with background color change
- Scrollbar indicator for list navigation
- Download progress indicator during content updates
- Status messages for empty directories

### Keypad Integration
```python
# Key mappings for navigation
NAV_UP = '8'
NAV_DOWN = '2'
NAV_SELECT = '5'
NAV_BACK = '*'
```

## 4. Videos Menu Implementation

### Purpose
The `Videos Menu` feature allows users to browse and select downloaded videos from the local content library, providing a navigable list interface controlled by the 3x4 keypad.

### State Architecture
- **VIDEOS_MENU State**: State class in `src/states/videos_menu.py`
- **Transition Logic**: '2' key from DASHBOARD → VIDEOS_MENU → VIEWER (on selection)
- **Navigation Keys**:
  - '8' (up): Scroll up in list
  - '2' (down): Scroll down in list
  - '5' (select): Open selected video in player
  - '*' (back): Return to dashboard

### Directory Scanning
- Scans `/content/videos` directory for available files
- Supports common video formats: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm
- Dynamic list updates after new downloads
- Filename-based titles with truncation for long names

### UI Components
- Centered scrollable list display (800px width, 8 items visible)
- Selection highlighting with background color change
- Scrollbar indicator for list navigation
- Download progress indicator during content updates
- Status messages for empty directories

### Keypad Integration
```python
# Key mappings for navigation
NAV_UP = '8'
NAV_DOWN = '2'
NAV_SELECT = '5'
NAV_BACK = '*'
```

## 5. Content Viewer Implementation

### Purpose
The `Content Viewer` provides a unified interface for consuming different types of content, handling both document viewing and video playback with appropriate controls and user feedback.

### State Architecture
- **VIEWER State**: State class in `src/states/viewer.py`
- **Transition Logic**: BOOKS_MENU/VIDEOS_MENU (select) → VIEWER → BOOKS_MENU/VIDEOS_MENU (exit)
- **Content Types**: Books (PDF/text) and Videos (external player)

### Book Viewing Features
- **PDF Support**: Renders PDF pages as images using PyMuPDF for full formatting preservation
- **Text Support**: Paginated text display with word wrapping
- **Navigation**: Page-by-page navigation with prev/next controls
- **Performance**: Image caching for smooth PDF page transitions
- **Fallback**: Text extraction fallback if image rendering fails

### Video Playing Features
- **External Players**: Supports multiple video players (mpv, omxplayer, vlc, mplayer)
- **Auto-Detection**: Automatically detects available players on the system
- **Full-Screen**: Launches videos in full-screen mode
- **Process Management**: Proper cleanup and monitoring of video processes
- **Error Handling**: Clear messages when no compatible players are found

### UI Components
- **Background**: Subtle light grey background (RGB: 252, 252, 252) for eye comfort
- **Title Display**: Shows current content name and type
- **Navigation Instructions**: Context-sensitive control hints
- **Page Indicators**: Current page / total pages for documents
- **Loading States**: Progress feedback during content loading
- **Error Messages**: Clear feedback for missing files or unsupported formats

### Keypad Integration
```python
# Universal exit key
NAV_EXIT = '*'

# Book-specific navigation
NAV_PREV_PAGE = '4'  # Left arrow
NAV_NEXT_PAGE = '6'  # Right arrow
NAV_SCROLL_UP = '8'   # Up arrow
NAV_SCROLL_DOWN = '2' # Down arrow
```

## 6. State Transitions

```
DASHBOARD (press '1') → BOOKS_MENU (press '5') → VIEWER (press '*') → BOOKS_MENU (press '*') → DASHBOARD
DASHBOARD (press '2') → VIDEOS_MENU (press '5') → VIEWER (press '*') → VIDEOS_MENU (press '*') → DASHBOARD
```

## 7. Technical Implementation

### Dependencies
- **PyMuPDF (fitz)**: PDF rendering and text extraction
- **pygame**: UI rendering and image display
- **subprocess**: External video player management

### File Structure
```
src/states/
├── books_menu.py      # Books list state
├── videos_menu.py     # Videos list state
├── viewer.py          # Content viewer state

content/
├── books/             # Book files (.pdf, .txt, .epub, .docx)
└── videos/            # Video files (.mp4, .avi, .mkv, etc.)
```

### PDF Rendering Process
1. Load PDF document using PyMuPDF
2. Calculate appropriate zoom level to fit screen
3. Render page as high-quality PNG image
4. Convert to pygame Surface for display
5. Cache rendered images for performance

### Video Player Detection
1. Test availability of common video players
2. Try players in order of preference (mpv → omxplayer → vlc → mplayer)
3. Launch selected player with fullscreen arguments
4. Monitor process lifecycle and handle cleanup

## 8. Acceptance Criteria

### Books Menu
* [x] Pressing '1' on the dashboard navigates to the books list
* [x] The books list displays the titles of all files in the `/content/books` directory
* [x] The user can scroll up and down the list using the keypad ('8' up, '2' down)
* [x] Pressing '5' on a book item opens it in the content viewer
* [x] Pressing '*' returns the user to the main dashboard

### Videos Menu
* [x] Pressing '2' on the dashboard navigates to the videos list
* [x] The videos list displays the titles of all files in the `/content/videos` directory
* [x] The user can scroll up and down the list using the keypad ('8' up, '2' down)
* [x] Pressing '5' on a video item opens it in the content viewer
* [x] Pressing '*' returns the user to the main dashboard

### Content Viewer
* [x] Selecting a book from the list opens it in a viewer with proper formatting
* [x] The user can navigate pages of a book using keypad controls ('4'/'6')
* [x] Selecting a video from the list launches it in full-screen external player
* [x] Exiting the video player returns the user to the video list
* [x] A consistent "exit" command ('*') works in both book and video viewers
* [x] PDF files display with full formatting (images, layout, fonts)
* [x] Text files display with proper pagination and word wrapping
* [x] Clear error messages for missing files or unsupported formats
* [x] Subtle grey background for improved readability

## 9. Raspberry Pi Deployment Notes

### Video Player Installation
**⚠️ IMPORTANT**: These commands are only for Raspberry Pi/Linux deployment. They will not work on Windows development machines.

On the target Raspberry Pi hardware, install video players with:
```bash
# Install recommended modern video player
sudo apt update
sudo apt install mpv

# Alternative classic Raspberry Pi player
sudo apt install omxplayer
```

**Windows Development**: Video player detection will correctly show "No video players available" during development. This is expected behavior - video playback only works on Raspberry Pi with installed players.

### Performance Considerations
- PDF rendering may take 1-2 seconds for first page of large documents
- Image caching prevents re-rendering of previously viewed pages
- Video playback runs in separate process to avoid blocking UI

## 10. Future Extensions

This completes the core content viewing functionality. Future enhancements may include:
- Zoom controls for PDF viewing
- Bookmarking system for documents
- Video playback controls (pause, seek)
- Content search functionality
- Thumbnail previews in menus
- Content metadata display (author, duration, file size)
