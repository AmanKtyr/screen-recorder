# Professional Screen Recorder

A professional-grade screen recording application with advanced audio options, region selection, and a user-friendly interface.

## Features

- **High-Quality Screen Recording**: Capture your screen in high definition
- **Region Selection**: Record your entire screen or select a specific region
- **Flexible Audio Options**:
  - Record with microphone audio
  - Record with system audio
  - Record with both microphone and system audio
  - Record without audio
- **Switch Audio Sources During Recording**: Toggle microphone and system audio on/off while recording
- **Pause and Resume**: Pause your recording and resume when ready
- **Countdown Timer**: Configurable countdown before recording starts
- **Hotkey Support**: Control recording with customizable keyboard shortcuts
- **System Tray Integration**: Minimize to system tray while recording
- **Recordings Manager**: Browse, play, and manage your recordings
- **Professional UI**: Clean, intuitive interface for easy operation
- **Customizable Settings**: Configure video quality, frame rate, audio settings, and more

## Requirements

- Python 3.8+
- PyQt5
- OpenCV
- SoundDevice
- SoundFile
- NumPy
- FFmpeg (must be installed and in PATH)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/screen-recorder.git
   cd screen-recorder
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install FFmpeg:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - Linux: `sudo apt install ffmpeg`
   - Mac: `brew install ffmpeg`

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Select your audio source:
   - Microphone
   - System Sound
   - Both Microphone and System Sound
   - No Audio

3. Click "Start Recording" to begin

4. Optionally select a specific region to record

5. During recording, you can:
   - Toggle microphone on/off
   - Toggle system audio on/off
   - Pause/Resume recording
   - Stop recording
   - Use hotkeys to control recording (configurable in Settings)

6. When finished, click "Stop Recording" to save your recording

7. Use the Recordings Manager to view, play, and manage your recordings

## Project Structure

```
screen-recorder/
├── main.py                    # Main application entry point
├── requirements.txt           # Required packages
├── ui/                        # User interface modules
│   ├── __init__.py
│   ├── home_screen.py         # Home screen with start button
│   ├── recording_screen.py    # Recording screen with controls
│   ├── settings_screen.py     # Settings configuration screen
│   ├── recordings_manager.py  # Recordings browser and manager
│   ├── region_selector.py     # Screen region selection tool
│   └── countdown_timer.py     # Countdown timer before recording
├── core/                      # Core functionality
│   ├── __init__.py
│   ├── screen_recorder.py     # Screen recording logic
│   └── audio_manager.py       # Audio recording logic
└── utils/                     # Utility modules
    ├── __init__.py
    ├── settings.py            # Application settings
    └── hotkey_manager.py      # Global hotkey management
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
