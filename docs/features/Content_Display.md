# Feature: Content Display System

## 1. Content Selection and Navigation

### Purpose
The content display system allows users to browse and select between different types of media content (books and videos) from the local content library, providing navigable list interfaces controlled by the 3x4 keypad.

### User Story
As a user, I want to see options for different content types on the dashboard, so that I can choose between books and videos to consume.

### Expected Behavior
The dashboard displays "Books" and "Videos" options. Users can press '1' for books or '2' for videos to navigate to the respective content menus, where they can browse available content.

## 2. Books Menu Implementation

### Purpose
The `Books Menu` feature allows users to browse and select downloaded books from the local content library, providing a navigable list interface controlled by the 3x4 keypad.

### State Architecture
- **BOOKS_MENU State**: State class in `src/states/books_menu.py`
- **Transition Logic**: '1' key from DASHBOARD → BOOKS_MENU
- **Navigation Keys**:
  - '8' (up): Scroll up in list
  - '2' (down): Scroll down in list
  - '5' (select): Choose highlighted item (logs action)
  - '*' (back): Return to dashboard

### Directory Scanning
- Scans `/content/books` directory for available files
- Supports common book formats: .txt, .pdf, .epub
- Dynamic list updates after new downloads
- Basic filename-based titles

### UI Components
- Centered scrollable list display
- Selection highlighting with color change
- Page indicator for long lists (future)
- Smooth scrolling animation (basic implementation)

### Keypad Integration
```python
# Key mappings for navigation
NAV_UP = '8'
NAV_DOWN = '2'
NAV_SELECT = '5'
NAV_BACK = '*'
```

## 3. Videos Menu Implementation

### Purpose
The `Videos Menu` feature allows users to browse and select downloaded videos from the local content library, providing a navigable list interface controlled by the 3x4 keypad.

### State Architecture
- **VIDEOS_MENU State**: State class in `src/states/videos_menu.py`
- **Transition Logic**: '2' key from DASHBOARD → VIDEOS_MENU
- **Navigation Keys**:
  - '8' (up): Scroll up in list
  - '2' (down): Scroll down in list
  - '5' (select): Choose highlighted item (logs action)
  - '*' (back): Return to dashboard

### Directory Scanning
- Scans `/content/videos` directory for available files
- Supports common video formats: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm
- Dynamic list updates after new downloads
- Basic filename-based titles

### UI Components
- Centered scrollable list display
- Selection highlighting with color change
- Page indicator for long lists (future)
- Smooth scrolling animation (basic implementation)

### Keypad Integration
```python
# Key mappings for navigation
NAV_UP = '8'
NAV_DOWN = '2'
NAV_SELECT = '5'
NAV_BACK = '*'
```

### File Structure Updates
```
src/states/
├── books_menu.py      # Books list state
├── videos_menu.py     # New: Videos list state
```

## 4. State Transitions

```
DASHBOARD (press '1') → BOOKS_MENU (press '*') → DASHBOARD
DASHBOARD (press '2') → VIDEOS_MENU (press '*') → DASHBOARD
```

## 5. Acceptance Criteria

### Books Menu
* [x] Pressing '1' on the dashboard navigates to the books list
* [x] The books list displays the titles of all files in the `/content/books` directory
* [x] The user can scroll up and down the list using the keypad ('8' up, '2' down)
* [x] Pressing '5' on a book item logs the selection (placeholder for future reading action)
* [x] Pressing '*' returns the user to the main dashboard

### Videos Menu
* [x] Pressing '2' on the dashboard navigates to the videos list
* [x] The videos list displays the titles of all files in the `/content/videos` directory
* [x] The user can scroll up and down the list using the keypad ('8' up, '2' down)
* [x] Pressing '5' on a video item logs the selection (placeholder for future video player)
* [x] Pressing '*' returns the user to the main dashboard

## 6. Future Extensions

This implements the foundation for FR-006. Future enhancements include:
- Search/filter functionality
- Content metadata display (author, description)
- Thumbnail/preview images
- Actual content viewing integration (FR-007)
