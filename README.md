I'll create a comprehensive README.md for the weather app:

```markdown:README.md
# Weather & Camera Monitor

A modern desktop application that combines weather monitoring with security camera integration, built with Python and PyQt5.

![App Screenshot](docs/screenshot.png)

## Features

- **Real-time Weather Data**
  - Current temperature and conditions
  - 7-day weather forecast
  - Weather alerts and warnings
  - Customizable temperature thresholds
  - Interactive temperature graph

- **Security Camera Integration**
  - Live camera feeds via Frigate NVR
  - Multi-camera support
  - Fullscreen camera view
  - Resizable camera windows
  - Automatic refresh

- **Modern UI**
  - Dark theme with purple accents
  - Responsive layout
  - Smooth animations
  - System tray integration
  - Desktop notifications

## Installation

### Arch Linux
```bash
# Clone the repository
git clone https://github.com/yourusername/weather-camera-app.git
cd weather-camera-app

# Run the installer
chmod +x install.sh
./install.sh
```

### Dependencies
- Python 3.8+
- PyQt5
- OpenWeather API key
- Frigate NVR (optional, for camera support)
- ImageMagick
- Noto Sans & Hack fonts

## Configuration

1. Edit the configuration file at `~/.config/weather-app/.env`:
```ini
OPENWEATHER_API_KEY=your_api_key_here
MAX_TEMP_THRESHOLD=35
MIN_TEMP_THRESHOLD=0
WIND_THRESHOLD=20
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
REFRESH_INTERVAL=300
FRIGATE_URL=http://localhost:5000
FRIGATE_API_KEY=
```

2. Get an API key from [OpenWeather](https://openweathermap.org/api)

## Usage

### Starting the App
```bash
./run.sh
```

Or find "Weather App" in your applications menu.

### Features Guide

- **Weather Display**
  - Click on forecast days to see detailed information
  - Hover over graph points for temperature details
  - Weather alerts appear automatically when conditions meet thresholds

- **Camera Controls**
  - Double-click camera view for fullscreen
  - Use the camera selector to switch between cameras
  - Click refresh button to manually update feed
  - Resize camera window using the grip handle

## Development

### Project Structure
```
weather-app/
├── src/
│   ├── api/           # API services
│   ├── ui/            # UI components
│   ├── utils/         # Utilities
│   └── notifications/ # Alert system
├── tests/             # Unit tests
├── docs/             # Documentation
└── assets/           # Images & resources
```

### Running Tests
```bash
pip install pytest
pytest tests/
```

### Building from Source
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Weather data provided by [OpenWeather](https://openweathermap.org/)
- Camera integration powered by [Frigate NVR](https://frigate.video/)
- Icons and design elements from [Material Design](https://material.io/)

## Support

- Report issues on GitHub
- Join our [Discord community](discord-link)
- Check the [Wiki](wiki-link) for detailed documentation

## Authors

- Your Name - Initial work - [GitHub](https://github.com/yourusername)

## Roadmap

- [ ] Mobile app version
- [ ] Additional weather data providers
- [ ] Custom alert rules
- [ ] Weather history tracking
- [ ] Camera motion detection
```

This README:
1. Provides a clear overview of features
2. Includes installation instructions for Arch Linux
3. Details configuration steps
4. Explains usage and features
5. Includes development information
6. Has proper formatting and structure
7. Includes sections for contributing and support

Let me know if you'd like to adjust any sections or add more details!
