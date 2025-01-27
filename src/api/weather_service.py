import requests
from typing import Dict, Any, Optional
from ..utils.config import Config
from ..models.weather_data import WeatherData, ForecastData
from datetime import datetime

class WeatherService:
    """Service for interacting with OpenWeather API"""
    
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        if not self.api_key:
            raise ValueError("OpenWeather API key not found in configuration")
        self.base_url = "http://api.openweathermap.org/data/3.0"

    def get_current_weather(self, city: str) -> Optional[WeatherData]:
        """Get current weather for a city"""
        try:
            # First get coordinates from geocoding API
            geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': city,
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(geocoding_url, params=params)
            response.raise_for_status()
            
            locations = response.json()
            if not locations:
                raise ValueError(f"City not found: {city}")
            
            location = locations[0]
            lat = location['lat']
            lon = location['lon']
            
            # Get current weather using coordinates
            url = f"{self.base_url}/onecall"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'exclude': 'minutely,hourly,daily,alerts'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 401:
                raise ValueError(f"Invalid API key: {self.api_key}")
            response.raise_for_status()
            
            data = response.json()
            current = data['current']
            
            return WeatherData(
                temperature=current['temp'],
                feels_like=current['feels_like'],
                humidity=current['humidity'],
                wind_speed=current['wind_speed'],
                wind_deg=current['wind_deg'],
                pressure=current['pressure'],
                description=current['weather'][0]['description'],
                timestamp=datetime.fromtimestamp(current['dt']),
                location=city,
                icon_code=current['weather'][0]['icon']
            )
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting weather data: {e}")
            return None
        except ValueError as e:
            print(f"Configuration error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_forecast(self, city: str) -> Optional[ForecastData]:
        """Get 7-day forecast for a city"""
        try:
            # First get coordinates from geocoding API
            geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': city,
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(geocoding_url, params=params)
            response.raise_for_status()
            
            locations = response.json()
            if not locations:
                raise ValueError(f"City not found: {city}")
            
            location = locations[0]
            lat = location['lat']
            lon = location['lon']
            
            # Get forecast using coordinates
            url = f"{self.base_url}/onecall"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'exclude': 'current,minutely,hourly,alerts'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data['daily'][:7]:  # Get first 7 days
                forecast = WeatherData(
                    temperature=item['temp']['day'],
                    feels_like=item['feels_like']['day'],
                    humidity=item['humidity'],
                    wind_speed=item['wind_speed'],
                    wind_deg=item['wind_deg'],
                    pressure=item['pressure'],
                    description=item['weather'][0]['description'],
                    timestamp=datetime.fromtimestamp(item['dt']),
                    location=city,
                    icon_code=item['weather'][0]['icon']
                )
                forecasts.append(forecast)
            
            return ForecastData(
                location=city,
                daily_forecasts=forecasts
            )
        except Exception as e:
            print(f"Error getting forecast data: {e}")
            return None 