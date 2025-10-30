# MEB-x Kiosk Application

A standalone kiosk application for Raspberry Pi Zero 2 W providing access to educational books and videos using a 3x4 matrix keypad interface.

## Hardware Requirements

- Raspberry Pi Zero 2 W with Raspberry Pi OS Lite
- 3x4 Matrix Keypad connected to GPIO pins:
  - ROW_PINS = [18, 19, 20]
  - COL_PINS = [12, 13, 16, 26]
- HDMI display (1280x720 resolution)

## Software Requirements

- Python 3.x (pre-installed on Raspberry Pi OS Lite)
- Dependencies listed in `requirements.txt`

## Installation

1. Copy the `meb-x` directory to `/home/oladiran/meb-x` on the Raspberry Pi
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `installer/meb-x.service` to `/etc/systemd/system/`
4. Enable autostart: `sudo systemctl enable meb-x.service`
5. Reboot the Raspberry Pi

## Current Features (MUS - Minimum Usable State)

- **FR-001**: Autostart on boot - Application launches automatically on startup
- **FR-002**: Splash screen - Displays EU logo for 3 seconds on startup
- **FR-003**: Main dashboard - Shows "Books" and "Videos" options on dark gray background
- **FR-004**: Keypad navigation - '1' highlights "Books", '2' highlights "Videos"

## Future Development

- **FR-005**: Automatic content downloading when internet is available
- **FR-006**: Content lists for books and videos
- **FR-007**: Content player/viewer for selected books and videos

## Project Structure

```
/meb-x
├── src/
│   ├── app.py              # Main application entry point
│   ├── states/             # State classes for the state machine
│   ├── hardware/           # Hardware interfaces (keypad)
│   └── ui/                 # UI system (components, renderer)
├── assets/                 # Images, fonts, and other media
├── config/                 # Configuration files
├── content/                # Downloaded books and videos
├── docs/                   # Documentation
├── installer/              # Service files for installation
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Running the Application

To run manually for testing (without service):

```bash
cd /home/oladiran/meb-x/src
python app.py
```

Note: The application detects if it's running on a Raspberry Pi and adjusts display mode accordingly (fullscreen on Pi, windowed on other platforms).
