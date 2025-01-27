from typing import List
from ..models.weather_data import WeatherData
from ..utils.config import Config

class AlertService:
    """Service for checking weather alerts"""
    
    def check_alerts(self, weather_data) -> List[str]:
        """Check for weather alerts based on thresholds"""
        alerts = []
        
        # Temperature alerts
        if weather_data.temperature > Config.MAX_TEMP_THRESHOLD:
            alerts.append(
                f"⚠️ High temperature alert: {weather_data.temperature}°C\n"
                "Stay hydrated and avoid prolonged sun exposure"
            )
        elif weather_data.temperature < Config.MIN_TEMP_THRESHOLD:
            alerts.append(
                f"❄️ Low temperature alert: {weather_data.temperature}°C\n"
                "Dress warmly and watch for icy conditions"
            )
        
        # Wind alerts
        if weather_data.wind_speed > Config.SEVERE_WIND_THRESHOLD:
            alerts.append(
                f"💨 High wind alert: {weather_data.wind_speed} m/s\n"
                "Secure loose objects and exercise caution outdoors"
            )
        
        # Severe weather conditions
        if any(condition in weather_data.description.lower() 
               for condition in ['thunderstorm', 'tornado', 'hurricane']):
            alerts.append(
                "⛈️ Severe weather warning!\n"
                "Stay indoors and follow local authority guidelines"
            )
        
        return alerts 