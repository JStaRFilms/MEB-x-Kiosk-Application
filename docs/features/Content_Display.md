# Feature: Content Display System

## 1. Books Menu Implementation

### Purpose
The `Books Menu` feature allows users to browse and select downloaded books from the local content library, providing a navigable list interface controlled by the 3x4 keypad.

### User Story
As a user, I want to see a list of available books on the dashboard, so that I can browse and select a book to read.

### Expected Behavior
After navigating to the "Books" section from the dashboard, the UI displays a list of locally available books found in `/content/books`. The list is navigable using keypad controls for scrolling and selection.

## 2. Implementation Details

### State Architecture
- **BOOKS_MENU State**: New state class in `src/states/books_menu.py`
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

### File Structure Updates
```
src/states/
├── books_menu.py      # New: Books list state
```

## 3. State Transitions

```
DASHBOARD (press '1') → BOOKS_MENU (press '*') → DASHBOARD
```

## 4. Acceptance Criteria

* [x] Pressing '1' on the dashboard navigates to the books list
* [x] The books list displays the titles of all files in the `/content/books` directory
* [x] The user can scroll up and down the list using the keypad ('8' up, '2' down)
* [x] Pressing '5' on a book item logs the selection (placeholder for future reading action)
* [x] Pressing '*' returns the user to the main dashboard

## 5. Future Extensions

This implements the foundation for FR-006. Future enhancements include:
- VIDEOS_MENU state for video content
- Search/filter functionality
- Content metadata display (author, description)
- Thumbnail/preview images
- Actual content viewing integration (FR-007)
