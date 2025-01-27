from dataclasses import dataclass
from typing import List

@dataclass
class WeatherWarning:
    """Weather warning data model"""
    severity: str  # 'low', 'medium', 'high'
    title: str
    message: str
    icon: str

class WeatherWarnings:
    """Weather warnings manager"""
    
    # Severity levels
    SEVERITY_LOW = "low"
    SEVERITY_MEDIUM = "medium"
    SEVERITY_HIGH = "high"
    
    # Severity colors (dark theme)
    SEVERITY_COLORS = {
        SEVERITY_LOW: "#FDD835",      # Yellow
        SEVERITY_MEDIUM: "#FB8C00",   # Orange
        SEVERITY_HIGH: "#D32F2F"      # Red
    }
    
    # Warning icons
    ICONS = {
        "temperature_high": "🌡️",
        "temperature_low": "❄️",
        "wind": "💨",
        "rain": "🌧️",
        "storm": "⛈️",
        "humidity": "💧",
        "snow": "🌨️"
    }
    
    @classmethod
    def check_warnings(cls, weather_data) -> List[WeatherWarning]:
        """Check for all possible weather warnings"""
        warnings = []
        
        # Temperature warnings
        if weather_data.temperature > 35:
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_HIGH,
                title="Extreme Heat Warning",
                message="Temperature is dangerously high. Stay hydrated and avoid prolonged sun exposure.",
                icon=cls.ICONS["temperature_high"]
            ))
        elif weather_data.temperature > 30:
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_MEDIUM,
                title="High Temperature Alert",
                message="High temperatures expected. Stay hydrated and seek shade when possible.",
                icon=cls.ICONS["temperature_high"]
            ))
        elif weather_data.temperature < 0:
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_HIGH,
                title="Freezing Temperature Warning",
                message="Temperature is below freezing. Risk of ice formation.",
                icon=cls.ICONS["temperature_low"]
            ))
        elif weather_data.temperature < 5:
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_MEDIUM,
                title="Low Temperature Alert",
                message="Cold temperatures expected. Dress warmly.",
                icon=cls.ICONS["temperature_low"]
            ))
        
        # Wind warnings
        if weather_data.wind_speed > 20:
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_HIGH,
                title="Strong Wind Warning",
                message="Dangerous wind conditions. Secure loose objects and avoid unnecessary travel.",
                icon=cls.ICONS["wind"]
            ))
        elif weather_data.wind_speed > 15:
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_MEDIUM,
                title="Wind Advisory",
                message="Strong winds expected. Exercise caution outdoors.",
                icon=cls.ICONS["wind"]
            ))
        
        # Storm warnings
        if "thunderstorm" in weather_data.description.lower():
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_HIGH,
                title="Thunderstorm Warning",
                message="Severe thunderstorm conditions. Seek shelter immediately.",
                icon=cls.ICONS["storm"]
            ))
        elif "storm" in weather_data.description.lower():
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_MEDIUM,
                title="Storm Alert",
                message="Stormy conditions expected. Stay prepared.",
                icon=cls.ICONS["storm"]
            ))
        
        # Rain and snow warnings
        if "heavy rain" in weather_data.description.lower():
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_MEDIUM,
                title="Heavy Rain Alert",
                message="Heavy rainfall expected. Be aware of flooding risks.",
                icon=cls.ICONS["rain"]
            ))
        elif "snow" in weather_data.description.lower():
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_MEDIUM,
                title="Snow Alert",
                message="Snowy conditions expected. Exercise caution while traveling.",
                icon=cls.ICONS["snow"]
            ))
        
        # Humidity warnings
        if weather_data.humidity > 85:
            warnings.append(WeatherWarning(
                severity=cls.SEVERITY_LOW,
                title="High Humidity Alert",
                message="Very humid conditions. Stay hydrated.",
                icon=cls.ICONS["humidity"]
            ))
        
        return warnings 