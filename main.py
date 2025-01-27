#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.utils.config import Config
from src.ui.main_window import MainWindow

def verify_project_structure():
    """Verify that all required files and directories exist"""
    required_paths = [
        'src/utils/config.py',
        'src/models/weather_data.py',
        'src/api/weather_service.py',
        'src/notifications/alert_service.py',
        'src/ui/main_window.py'
    ]
    
    missing_files = []
    for path in required_paths:
        if not Path(path).is_file():
            missing_files.append(path)
    
    return missing_files

def verify_env_file():
    """Verify that .env file exists and contains required values"""
    env_path = Path('.env')
    if not env_path.exists():
        print(f"Error: .env file not found in {env_path.absolute()}")
        return False
    
    print(f"Found .env file at {env_path.absolute()}")
    with open(env_path) as f:
        contents = f.read()
        print("\n.env file contents:")
        # Print contents but mask the full API key
        for line in contents.splitlines():
            if line.startswith('OPENWEATHER_API_KEY='):
                key = line.split('=')[1]
                print(f"OPENWEATHER_API_KEY={key[:8]}...")
            else:
                print(line)
    return True

def main():
    """Main application entry point"""
    try:
        # Verify .env file
        if not verify_env_file():
            return 1
            
        # Enable high DPI scaling
        if hasattr(QApplication, 'setAttribute'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Create application
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        # Set application metadata
        app.setApplicationName("Weather App")
        app.setOrganizationName("WeatherApp")
        app.setOrganizationDomain("weatherapp.local")
        
        # Verify configuration
        if not Config.OPENWEATHER_API_KEY:
            raise ValueError("OpenWeather API key not found. Please set OPENWEATHER_API_KEY in .env file")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start event loop
        return app.exec_()
        
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 