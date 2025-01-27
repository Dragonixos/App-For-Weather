import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    @classmethod
    def initialize(cls):
        """Initialize configuration from environment variables"""
        # Get the project root directory
        cls.ROOT_DIR = Path(__file__).parent.parent.parent
        
        # Ensure config directories exist
        cls.CONFIG_DIR = Path(os.path.expanduser("~/.config/weather-app"))
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Cache directory for weather icons
        cls.CACHE_DIR = cls.CONFIG_DIR / "cache"
        cls.CACHE_DIR.mkdir(exist_ok=True)
        
        # Load settings from environment
        cls.WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '800'))
        cls.WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
        cls.REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', '300'))  # seconds
        
        # Weather alert thresholds
        cls.MAX_TEMP_THRESHOLD = float(os.getenv('MAX_TEMP_THRESHOLD', '35'))  # °C
        cls.MIN_TEMP_THRESHOLD = float(os.getenv('MIN_TEMP_THRESHOLD', '0'))   # °C
        cls.SEVERE_WIND_THRESHOLD = float(os.getenv('WIND_THRESHOLD', '20'))   # m/s
        cls.WIND_THRESHOLD = cls.SEVERE_WIND_THRESHOLD  # Alias for backward compatibility
        
        # API configurations
        cls.OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
        cls.FRIGATE_URL = os.getenv('FRIGATE_URL', 'http://localhost:5000')
        cls.FRIGATE_API_KEY = os.getenv('FRIGATE_API_KEY')

# Initialize configuration when module is loaded
Config.initialize() 