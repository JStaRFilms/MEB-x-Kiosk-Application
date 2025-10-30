# MEB-x Project Requirements Document

## 1. Project Overview

The MEB-x project is a standalone kiosk application designed to run on a Raspberry Pi Zero 2 W. Its primary purpose is to provide a user-friendly dashboard for accessing educational content, specifically books and videos. The system will boot directly into the application, display a splash screen, and present a navigable interface controlled entirely by a 3x4 hardware keypad. The content should be updated automatically when an internet connection is available.

## 2. Target Environment

*   **Hardware:** Raspberry Pi Zero 2 W Rev 1.0
*   **OS:** Raspberry Pi OS Lite (32-bit)
*   **Python Version:** 3.x (pre-installed on Raspberry Pi OS Lite)
*   **Input:** 3x4 Matrix Keypad
*   **Display:** Connected display via HDMI or DSI

## 3. Functional Requirements (FRs)

| Requirement ID | Description | User Story | Expected Behavior/Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| FR-001 | **Autostart on Boot** | As a user, I want the device to automatically launch the MEB-x application when it powers on, so that I don't need any manual intervention. | The application starts automatically after the Raspberry Pi OS finishes booting, displaying the splash screen without requiring a login or command execution. | MUS |
| FR-002 | **Display Splash Screen** | As a user, I want to see the EU logo on startup, so that I know the application is initializing. | Upon launch, the application displays a full-screen splash screen with the EU logo for a few seconds before transitioning to the main dashboard. | MUS |
| FR-003 | **Display Main Dashboard UI** | As a user, I want to see a clear and simple dashboard, so that I can easily understand the available options. | After the splash screen, the application displays a full-screen graphical dashboard. The dashboard will have distinct, navigable sections for "Books" and "Videos". | MUS |
| FR-004 | **Keypad Navigation** | As a user, I want to navigate the dashboard using the 3x4 keypad, so that I can interact with the interface without a mouse or keyboard. | The application responds to key presses from the 3x4 keypad. Specific keys will be mapped to actions (e.g., '1' selects "Books", '2' selects "Videos", '*' navigates back). The UI provides visual feedback for the current selection. | MUS |
| FR-005 | **Automatic Content Downloading** | As an administrator, I want the system to automatically download new books and videos when connected to the internet, so that the content is always up-to-date without manual effort. | The system periodically checks for an internet connection. If available, it connects to a pre-configured content source, downloads new or updated books and videos, and stores them locally. | Future |
| FR-006 | **Display Downloaded Content** | As a user, I want to see a list of available books and videos on the dashboard, so that I can browse and select content to consume. | After navigating to the "Books" or "Videos" section, the UI displays a scrollable or paginated list of the locally available content items, showing their titles. | Future |
| FR-007 | **Content Player/Viewer** | As a user, I want to open and view a selected book or video, so that I can consume the educational material. | Selecting a book opens its content (e.g., PDF, text reader) within the application. Selecting a video starts playback, either within the application UI or by launching an external media player. | Future |

## 4. Hardware Configuration

*   **Keypad:** 3x4 Matrix Keypad
*   **GPIO Pinout:**
    *   ROW_PINS = `[18, 19, 20]`
    *   COL_PINS = `[12, 13, 16, 26]`
