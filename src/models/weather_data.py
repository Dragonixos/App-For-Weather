from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class WeatherData:
    """Weather data model"""
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    wind_deg: int  # Add wind direction in degrees
    pressure: int  # Add pressure in hPa
    description: str
    timestamp: datetime
    location: str
    icon_code: str
    
    def temperature_fahrenheit(self) -> float:
        """Convert temperature to Fahrenheit"""
        return (self.temperature * 9/5) + 32
    
    def get_wind_direction(self) -> str:
        """Convert wind degrees to cardinal direction"""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(self.wind_deg / 22.5) % 16
        return directions[index]
    
    def get_pressure_trend(self) -> str:
        """Get pressure trend indicator"""
        if self.pressure > 1013:
            return "↑"  # High pressure
        elif self.pressure < 1013:
            return "↓"  # Low pressure
        return "→"  # Normal pressure

@dataclass
class ForecastData:
    """Forecast data model"""
    location: str
    daily_forecasts: List[WeatherData] 