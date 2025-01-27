#!/bin/bash

# Check if yay is installed
if ! command -v yay &> /dev/null; then
    echo "Installing yay (AUR helper)..."
    sudo pacman -S --needed git base-devel
    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si
    cd ..
    rm -rf yay
fi

# Install system dependencies
echo "Installing system dependencies..."
yay -S --needed \
    python \
    python-pip \
    python-virtualenv \
    imagemagick \
    ttf-hack \
    noto-fonts \
    qt5-base \
    qt5-svg

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create config directory
mkdir -p ~/.config/weather-app

# Create default .env file if it doesn't exist
if [ ! -f ~/.config/weather-app/.env ]; then
    cat > ~/.config/weather-app/.env << EOL
OPENWEATHER_API_KEY=your_api_key_here
MAX_TEMP_THRESHOLD=35
MIN_TEMP_THRESHOLD=0
WIND_THRESHOLD=20
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
REFRESH_INTERVAL=300
FRIGATE_URL=http://localhost:5000
FRIGATE_API_KEY=
EOL
    echo "Created default .env file at ~/.config/weather-app/.env"
    echo "Please edit the file and add your OpenWeather API key"
fi

# Make scripts executable
chmod +x run.sh
chmod +x main.py

# Create icon file
ICON_DIR=~/.local/share/icons/hicolor/128x128/apps
mkdir -p $ICON_DIR

# Create icon
convert -size 128x128 xc:none \
    -fill '#6200EA' \
    -draw 'circle 64,64 64,4' \
    -draw 'rectangle 32,32 96,96' \
    -fill white \
    -draw 'circle 64,64 64,8' \
    $ICON_DIR/weather-app.png

# Create desktop entry
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/weather-app.desktop << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Weather App
Comment=Weather monitoring application
Exec=$(pwd)/run.sh
Icon=weather-app
Terminal=false
Categories=Utility;
EOL

# Update icon cache
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor

# Update font cache
fc-cache -f

echo "Installation complete!"
echo "1. Edit ~/.config/weather-app/.env to set your API keys"
echo "2. Run the app with ./run.sh"
echo "3. Find Weather App in your applications menu" 