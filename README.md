# MEB-x Educational Kiosk Application

A comprehensive standalone kiosk application for Raspberry Pi providing access to educational books and videos through an intuitive 3x4 matrix keypad interface. Designed for deployment in educational environments where traditional input devices may not be available.

## 🎯 Overview

MEB-x (Multi-format Educational Browser for Raspberry Pi) is a state-of-the-art kiosk application that transforms a Raspberry Pi into a dedicated educational content platform. Users can browse, select, and consume educational materials using only a numeric keypad, making it accessible for various user groups and environments.

### Key Features
- **📚 Complete Book Viewing**: PDF documents with full formatting preservation and text file support
- **🎥 Video Playback**: Full-screen video playback with multiple player support
- **📱 Intuitive Navigation**: 3x4 keypad interface with clear visual feedback
- **⬇️ Automatic Content Updates**: Background downloading of new educational materials
- **🔄 Auto-Start**: Seamless boot-to-application experience
- **🎨 Modern UI**: Clean, accessible interface with subtle theming

## 🛠️ Hardware Requirements

### Core Hardware
- **Raspberry Pi Zero 2 W** or **Raspberry Pi 4/5** (recommended for better performance)
- **Raspberry Pi OS Lite** (64-bit recommended for Pi 4/5)
- **HDMI Display** (1280x720 resolution or higher)
- **3x4 Matrix Keypad** connected to GPIO pins

### GPIO Pin Configuration
```python
ROW_PINS = [18, 19, 20]      # GPIO pins for keypad rows
COL_PINS = [12, 13, 16, 26]  # GPIO pins for keypad columns
```

### Optional Hardware
- **USB WiFi Adapter** (for Pi Zero 2 W if WiFi is unreliable)
- **Powered USB Hub** (for additional peripherals if needed)

## 📦 Software Requirements

### Operating System
- **Raspberry Pi OS Lite** (64-bit for Pi 4/5, 32-bit for Pi Zero 2 W)
- **Python 3.9+** (pre-installed on Raspberry Pi OS)

### Dependencies
All required Python packages are listed in `requirements.txt`:
- `pygame` - Graphics and UI rendering
- `gpiozero` - GPIO hardware interface
- `RPi.GPIO` - Low-level GPIO control
- `requests` - HTTP client for content downloading
- `yt-dlp` - YouTube video downloading
- `PyMuPDF` - PDF document processing

## 🚀 Installation & Setup

### 1. Prepare Raspberry Pi
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3-pip python3-dev

# Optional: Install video players for full functionality
sudo apt install -y mpv omxplayer
```

### 2. Deploy Application
```bash
# Create application directory
sudo mkdir -p /home/oladiran/meb-x
sudo chown oladiran:oladiran /home/oladiran/meb-x

# Copy application files to Raspberry Pi
# (Use scp, rsync, or your preferred transfer method)
scp -r meb-x/* oladiran@raspberry-pi:/home/oladiran/meb-x/
```

### 3. Install Python Dependencies
```bash
cd /home/oladiran/meb-x
pip3 install -r requirements.txt
```

### 4. Configure Auto-Start
```bash
# Copy systemd service file
sudo cp installer/meb-x.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable meb-x.service
sudo systemctl start meb-x.service

# Check service status
sudo systemctl status meb-x.service
```

### 5. Initial Content Setup
The application will automatically download content based on the configuration in `config/app_config.json`. Ensure internet connectivity for initial content population.

## 🎮 User Interface & Navigation

### Keypad Layout & Controls
```
┌───┬───┬───┐
│ 1 │ 2 │ 3 │
├───┼───┼───┤
│ 4 │ 5 │ 6 │
├───┼───┼───┤
│ 7 │ 8 │ 9 │
├───┼───┼───┤
│ * │ 0 │ # │
└───┴───┴───┘
```

### Main Navigation
- **Dashboard**: `1` (Books) • `2` (Videos)
- **Menu Navigation**: `8` (Up) • `2` (Down) • `5` (Select) • `*` (Back)
- **Content Viewing**: `4`/`6` (Prev/Next Page) • `*` (Exit)

### Application Flow
```
Splash Screen → Dashboard → Books/Videos Menu → Content Viewer → Menu
     ↓            ↓              ↓                      ↓         ↓
   3 seconds     1/2          8/2/5/*               4/6/*     5/*
```

## ✨ Features & Functionality

### ✅ Implemented Features (FR-001 through FR-007)

#### FR-001: System Integration
- **Auto-start on boot** via systemd service
- **Clean shutdown** and resource management
- **Error recovery** and logging

#### FR-002: User Experience
- **Splash screen** with EU logo (3-second display)
- **Smooth transitions** between application states
- **Visual feedback** for all user interactions

#### FR-003: Dashboard Interface
- **Clean main menu** with Books and Videos options
- **Visual highlighting** of selected options
- **Dark background** for reduced eye strain

#### FR-004: Keypad Navigation
- **Responsive input** with debounced keypad scanning
- **Visual feedback** for key presses
- **Intuitive mapping** of numeric keys to functions

#### FR-005: Content Management
- **Automatic downloading** from configured sources
- **YouTube video support** via yt-dlp integration
- **Version control** to prevent re-downloads
- **Background updates** without interrupting user experience

#### FR-006: Content Browsing
- **Books menu** with scrollable list interface
- **Videos menu** with identical navigation patterns
- **Real-time content updates** when entering menus
- **File format detection** and display

#### FR-007: Content Consumption ⭐ **NEW**
- **PDF Viewing**: Full formatting preservation with image rendering
- **Text Documents**: Paginated display with word wrapping
- **Video Playback**: External player integration (mpv, omxplayer, vlc)
- **Unified Interface**: Consistent controls across content types
- **Error Handling**: Clear messages for missing content or players

### Content Viewer Details

#### Book Viewing
- **PDF Support**: Renders pages as images for perfect formatting
- **Text Support**: Clean pagination with proper line breaks
- **Navigation**: Page-by-page controls with visual indicators
- **Performance**: Image caching for smooth transitions

#### Video Playback
- **Multi-Player Support**: Automatic detection of available players
- **Full-Screen Mode**: Immersive viewing experience
- **Process Management**: Clean startup and shutdown
- **Fallback Options**: Multiple player preferences

## 📁 Project Structure

```
/home/oladiran/meb-x/
├── src/
│   ├── app.py                 # Main application & state management
│   ├── states/
│   │   ├── base_state.py      # Abstract state class
│   │   ├── splash.py          # EU logo splash screen
│   │   ├── dashboard.py       # Main menu interface
│   │   ├── books_menu.py      # Books browsing interface
│   │   ├── videos_menu.py     # Videos browsing interface
│   │   └── viewer.py          # Content viewer ⭐ NEW
│   ├── hardware/
│   │   └── keypad.py          # GPIO keypad interface
│   ├── services/
│   │   └── downloader.py      # Content download service
│   └── ui/
│       ├── renderer.py        # UI rendering utilities
│       └── components.py      # Reusable UI components
├── assets/
│   ├── fonts/default.ttf      # UI font
│   └── images/                # Logos and backgrounds
├── config/
│   └── app_config.json        # Application configuration
├── content/
│   ├── books/                 # Downloaded book files
│   └── videos/                # Downloaded video files
├── docs/
│   ├── features/              # Feature documentation
│   ├── Builder_Handoff_Report.md
│   ├── Coding_Guidelines.md
│   └── Project_Requirements.md
├── installer/
│   └── meb-x.service          # Systemd service file
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
└── .gitignore                 # Git ignore rules
```

## 🔧 Configuration

### Application Settings (`config/app_config.json`)
```json
{
  "content": {
    "enabled": true,
    "source_url": "https://gist.githubusercontent.com/.../content.json",
    "check_interval_hours": 24,
    "timeout_seconds": 30
  }
}
```

### Content Source Format
The application expects a JSON array of content items:
```json
[
  {
    "name": "Mathematics Handbook",
    "type": "book",
    "url": "https://example.com/handbook.pdf"
  },
  {
    "name": "Educational Video",
    "type": "video",
    "url": "https://youtube.com/watch?v=..."
  }
]
```

## 🧪 Testing & Development

### Manual Testing
```bash
# Run application manually (bypasses service)
cd /home/oladiran/meb-x/src
python3 app.py

# Check service logs
sudo journalctl -u meb-x.service -f

# Restart service after changes
sudo systemctl restart meb-x.service
```

### Development Environment
- **Platform Detection**: Application automatically adjusts for development vs. production
- **Windowed Mode**: Non-Raspberry Pi systems run in windowed mode
- **Mock Hardware**: GPIO interfaces gracefully handle missing hardware

### Troubleshooting
- **Video Not Playing**: Install `mpv` or `omxplayer` on Raspberry Pi
- **Content Not Downloading**: Check internet connectivity and source URL
- **Keypad Not Responding**: Verify GPIO pin connections
- **Application Won't Start**: Check service status and logs

## 📊 Performance & Compatibility

### System Requirements
- **RAM**: 512MB minimum (1GB recommended for video playback)
- **Storage**: 8GB SD card minimum (32GB recommended)
- **Network**: Ethernet or reliable WiFi for content updates

### Supported Content Formats
- **Books**: PDF (with formatting), TXT, EPUB, DOCX
- **Videos**: MP4, AVI, MKV, MOV, WMV, FLV, WebM
- **Sources**: Direct downloads, YouTube videos

### Video Player Compatibility
- **Primary**: `mpv` (modern, recommended)
- **Fallback**: `omxplayer` (Raspberry Pi optimized)
- **Additional**: `vlc`, `mplayer` (if available)

## 🤝 Contributing & Support

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Use type hints for function parameters
- Include docstrings for all classes and methods
- Test on target hardware before deployment

### Documentation
- Feature documentation in `docs/features/`
- Code documentation in docstrings
- API references for configuration options

### Issue Reporting
- Check service logs: `sudo journalctl -u meb-x.service`
- Verify hardware connections
- Test with known working content files

## 📄 License & Credits

This project is developed for educational kiosk deployments. The application uses royalty-free assets and open-source libraries.

### Acknowledgments
- **Raspberry Pi Foundation** for the excellent hardware platform
- **Python Community** for the robust ecosystem
- **Open Source Libraries** that make this project possible

---

## 🚀 Quick Start Summary

1. **Hardware Setup**: Connect keypad to GPIO pins, attach display
2. **Software Installation**: Flash Raspberry Pi OS, copy application files
3. **Dependency Installation**: `pip3 install -r requirements.txt`
4. **Service Configuration**: Enable auto-start with systemd
5. **Content Loading**: Application downloads content automatically
6. **Ready to Use**: Users can immediately browse and view educational materials

The MEB-x application provides a complete, production-ready educational content platform that transforms simple hardware into a powerful learning tool. 🎓
