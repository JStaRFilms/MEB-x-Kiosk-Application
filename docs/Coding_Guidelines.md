# MEB-x Coding Guidelines

## 1. Architecture

The MEB-x application will be built using a **State-Machine Architecture**. The application will always be in one of several defined states, and transitions between states will be triggered by user input (keypad) or internal events (e.g., splash screen timer).

*   **States:** `SPLASH`, `DASHBOARD`, `BOOKS_MENU`, `VIDEOS_MENU`, `VIEWER`
*   **Main Loop:** A single main loop will run continuously, checking for events (keypad presses) and updating the screen based on the current state.
*   **Modularity:** Each state will be represented by its own class or set of functions to keep the code organized and maintainable.

## 2. File Structure

A canonical project directory structure will be enforced:

```
/meb-x
├── src/
│   ├── app.py              # Main application entry point and state machine loop
│   ├── states/
│   │   ├── __init__.py
│   │   ├── splash.py       # Logic for the splash screen state
│   │   ├── dashboard.py    # Logic for the dashboard state
│   │   └── base_state.py   # Abstract base class for all states
│   ├── hardware/
│   │   ├── __init__.py
│   │   └── keypad.py       # Wrapper for keypad interaction using gpiozero
│   └── ui/
│       ├── __init__.py
│       ├── components.py   # Reusable UI components (buttons, lists)
│       └── renderer.py     # Handles all Pygame drawing calls
├── assets/
│   ├── images/
│   │   ├── eu_logo.png     # The EU logo for the splash screen
│   │   └── background.png  # Background image for the dashboard
│   └── fonts/
│       └── default.ttf     # A clear, readable font
├── config/
│   └── app_config.json     # Configuration file (e.g., keypad mappings, content paths)
├── content/
│   ├── books/              # Downloaded books will be stored here
│   └── videos/              # Downloaded videos will be stored here
├── docs/
│   ├── Project_Requirements.md
│   ├── Coding_Guidelines.md
│   └── Builder_Handoff_Report.md
├── installer/
│   └── meb-x.service       # systemd service file for autostart
├── requirements.txt        # Python dependencies
└── README.md               # Project setup and usage instructions
```

## 3. Coding Vibe

*   **Language:** Python 3.
*   **Formatting:** Adhere to PEP 8. Use `black` for automatic formatting.
*   **Linting:** Use `flake8` or `pylint` to ensure code quality.
*   **Docstrings:** Use clear and concise docstrings for all classes, functions, and modules following the Google style.
*   **Type Hinting:** Use type hints for all function signatures and variables to improve readability and maintainability.
*   **Error Handling:** Implement robust error handling, especially for hardware interactions (GPIO) and file I/O. Log errors to a file for debugging.
*   **Constants:** Avoid magic numbers and strings. Define constants in a dedicated `constants.py` file or within the relevant class/module.

## 4. In-IDE Assistant Priming

When using an in-IDE assistant (like GitHub Copilot), provide it with the following context for best results:

*   **Primary Context Files:** `src/app.py`, `docs/Project_Requirements.md`, and this `docs/Coding_Guidelines.md` file.
*   **Key Architectural Concept:** "This project uses a state-machine architecture. When generating code, please create or modify the appropriate state class in the `src/states/` directory and ensure transitions are handled in `src/app.py`."
*   **Hardware Abstraction:** "All hardware interactions, such as reading from the keypad, must be done through the classes in the `src/hardware/` directory. Do not access GPIO pins directly from UI or state logic."
*   **UI Rendering:** "All screen drawing logic should be contained within the `src/ui/renderer.py` module. State classes should call methods on the renderer, not call Pygame functions directly."
