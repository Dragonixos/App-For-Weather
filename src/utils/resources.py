import os
from pathlib import Path
import requests
from typing import Optional
import base64

class Resources:
    """Resource manager for the application"""
    
    # Get the resources directory path
    RESOURCES_DIR = Path(__file__).parent.parent.parent / 'resources'
    
    # OpenWeather icon URLs - try both HTTP and HTTPS
    WEATHER_ICON_URLS = [
        "http://openweathermap.org/img/wn/{icon_code}@2x.png",
        "https://openweathermap.org/img/wn/{icon_code}@2x.png"
    ]
    
    # Weather icon mappings
    WEATHER_ICONS = {
        'clear sky': 'sun.png',
        'few clouds': 'partly-cloudy.png',
        'scattered clouds': 'cloudy.png',
        'broken clouds': 'cloudy.png',
        'shower rain': 'rain.png',
        'rain': 'rain.png',
        'thunderstorm': 'storm.png',
        'snow': 'snow.png',
        'mist': 'fog.png'
    }
    
    # Base64 encoded PNG icon (simple weather + camera icon)
    APP_ICON_BASE64 = """
    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
    """
    
    @classmethod
    def get_app_icon(cls):
        """Get application icon as bytes"""
        return base64.b64decode(cls.APP_ICON_BASE64.strip())
    
    @classmethod
    def get_weather_icon(cls, description: str) -> str:
        """Get the path to the weather icon for the given description"""
        icon_name = cls.WEATHER_ICONS.get(description.lower(), 'unknown.png')
        icon_path = cls.RESOURCES_DIR / 'weather' / icon_name
        if not icon_path.exists():
            print(f"Warning: Weather icon not found: {icon_path}")
        return str(icon_path)

    @classmethod
    def get_weather_icon_url(cls, icon_code: str) -> str:
        """Get the working URL for the weather icon"""
        # Try HTTP first as it's more likely to work with SSL issues
        return cls.WEATHER_ICON_URLS[0].format(icon_code=icon_code)

    @classmethod
    def download_icon(cls, icon_code: str) -> Optional[bytes]:
        """Download weather icon and return the raw data"""
        for url_template in cls.WEATHER_ICON_URLS:
            try:
                url = url_template.format(icon_code=icon_code)
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return response.content
            except Exception as e:
                print(f"Error downloading icon from {url}: {e}")
                continue
        return None 