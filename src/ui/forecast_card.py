from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtGui import QPixmap
from ..utils.styles import Styles
from ..models.weather_data import WeatherData
from ..utils.resources import Resources

class ForecastCard(QFrame):
    """Widget to display a daily forecast"""
    
    # Add signal for click events
    clicked = pyqtSignal(WeatherData)
    
    def __init__(self, forecast: WeatherData, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.FORECAST_CARD)
        self.setFixedWidth(150)
        self.forecast = forecast
        self.is_selected = False  # Track selection state
        
        # Make the card look clickable
        self.setCursor(Qt.PointingHandCursor)
        
        # Create main layout with left margin for indentation
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Add spacer widget for indentation
        self.spacer = QWidget()
        self.spacer.setFixedWidth(0)  # Start with no indent
        self.main_layout.addWidget(self.spacer)
        
        # Content layout
        layout = QVBoxLayout()
        layout.setSpacing(3)
        self.main_layout.addLayout(layout)
        
        # Date (now using regular text color)
        date_label = QLabel(forecast.timestamp.strftime('%A\n%b %d'))
        date_label.setObjectName("forecastDate")
        date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(date_label)
        
        # Weather icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(50, 50)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # Load icon
        self.load_icon(forecast.icon_code)
        
        # Temperature
        temp_label = QLabel(f"{forecast.temperature:.1f}°C")
        temp_label.setObjectName("forecastTemp")
        temp_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(temp_label)
        
        # Description
        desc_label = QLabel(forecast.description.title())
        desc_label.setObjectName("forecastDesc")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Details
        details_layout = QGridLayout()
        
        # Feels like
        feels_like = QLabel("Feels like")
        feels_like.setObjectName("forecastDetailLabel")
        details_layout.addWidget(feels_like, 0, 0)
        
        feels_like_value = QLabel(f"{forecast.feels_like:.1f}°C")
        feels_like_value.setObjectName("forecastDetailValue")
        details_layout.addWidget(feels_like_value, 0, 1)
        
        # Humidity
        humidity = QLabel("Humidity")
        humidity.setObjectName("forecastDetailLabel")
        details_layout.addWidget(humidity, 1, 0)
        
        humidity_value = QLabel(f"{forecast.humidity}%")
        humidity_value.setObjectName("forecastDetailValue")
        details_layout.addWidget(humidity_value, 1, 1)
        
        # Wind
        wind = QLabel("Wind")
        wind.setObjectName("forecastDetailLabel")
        details_layout.addWidget(wind, 2, 0)
        
        # Wind speed and direction
        wind_layout = QVBoxLayout()
        wind_speed = QLabel(f"{forecast.wind_speed} m/s")
        wind_speed.setObjectName("forecastDetailValue")
        wind_layout.addWidget(wind_speed)
        
        wind_dir = QLabel(f"{forecast.get_wind_direction()}")
        wind_dir.setObjectName("forecastDetailSecondary")
        wind_layout.addWidget(wind_dir)
        
        details_layout.addLayout(wind_layout, 2, 1)
        
        # Pressure
        pressure = QLabel("Pressure")
        pressure.setObjectName("forecastDetailLabel")
        details_layout.addWidget(pressure, 3, 0)
        
        # Pressure value and trend
        pressure_layout = QVBoxLayout()
        pressure_value = QLabel(f"{forecast.pressure} hPa")
        pressure_value.setObjectName("forecastDetailValue")
        pressure_layout.addWidget(pressure_value)
        
        pressure_trend = QLabel(f"{forecast.get_pressure_trend()}")
        pressure_trend.setObjectName("forecastDetailSecondary")
        pressure_layout.addWidget(pressure_trend)
        
        details_layout.addLayout(pressure_layout, 3, 1)
        
        layout.addLayout(details_layout)
        
    def load_icon(self, icon_code: str):
        """Load weather icon"""
        icon_data = Resources.download_icon(icon_code)
        if icon_data:
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.icon_label.setPixmap(pixmap)

    def enterEvent(self, event):
        """Handle mouse enter events"""
        if not self.is_selected:
            self.spacer.setFixedWidth(10)  # Add indent on hover
            self.setStyleSheet(f"""
                {Styles.FORECAST_CARD}
                QFrame {{
                    background-color: {Styles.CARD_COLOR};
                    border: 1px solid {Styles.PRIMARY_COLOR};
                }}
            """)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave events"""
        if not self.is_selected:
            self.spacer.setFixedWidth(0)  # Remove indent
            self.setStyleSheet(Styles.FORECAST_CARD)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse click events"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.forecast)
        super().mousePressEvent(event)
    
    def set_selected(self, selected: bool):
        """Set the selected state of the card"""
        self.is_selected = selected
        if selected:
            self.spacer.setFixedWidth(15)  # Larger indent for selection
            self.setStyleSheet(f"""
                {Styles.FORECAST_CARD}
                QFrame {{
                    background-color: {Styles.CARD_COLOR};
                    border: 1px solid {Styles.PRIMARY_COLOR};
                }}
            """)
        else:
            self.spacer.setFixedWidth(0)
            self.setStyleSheet(Styles.FORECAST_CARD) 