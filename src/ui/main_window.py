from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QScrollArea, QSplitter)
from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QVariantAnimation
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QIcon
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import matplotlib
matplotlib.use('Qt5Agg')  # Must be called before importing pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from ..api.weather_service import WeatherService
from ..notifications.alert_service import AlertService
from ..utils.resources import Resources
from ..utils.styles import Styles
from ..utils.weather_warnings import WeatherWarnings
from .warning_card import WarningCard
from .forecast_card import ForecastCard
from .camera_viewer import CameraViewer

class DetailWidget(QFrame):
    """Widget to display a weather detail with icon"""
    def __init__(self, icon: str, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.DETAILS_WIDGET)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon_label)
        
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #666666;")
        layout.addWidget(self.title_label)
        
        self.value_label = QLabel()
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.value_label)
        
        # Add optional secondary value label
        self.secondary_label = QLabel()
        self.secondary_label.setAlignment(Qt.AlignCenter)
        self.secondary_label.setStyleSheet(f"""
            color: {Styles.SECONDARY_TEXT};
            font-size: 11px;
        """)
        layout.addWidget(self.secondary_label)

class WeatherCard(QFrame):
    """A card widget to display weather information"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.WEATHER_CARD)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Location
        self.location_label = QLabel()
        self.location_label.setObjectName("locationLabel")
        self.location_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.location_label)
        
        # Weather icon and temperature
        weather_layout = QHBoxLayout()
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(100, 100)
        self.icon_label.setAlignment(Qt.AlignCenter)
        weather_layout.addWidget(self.icon_label)
        
        temp_layout = QVBoxLayout()
        self.temp_label = QLabel()
        self.temp_label.setObjectName("temperatureLabel")
        self.temp_label.setAlignment(Qt.AlignCenter)
        temp_layout.addWidget(self.temp_label)
        
        self.desc_label = QLabel()
        self.desc_label.setObjectName("descriptionLabel")
        self.desc_label.setAlignment(Qt.AlignCenter)
        temp_layout.addWidget(self.desc_label)
        
        weather_layout.addLayout(temp_layout)
        layout.addLayout(weather_layout)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {Styles.BORDER_COLOR};")
        layout.addWidget(line)
        
        # Details grid
        details_layout = QGridLayout()
        details_layout.setSpacing(15)
        
        self.feels_like = DetailWidget("🌡️", "Feels Like")
        details_layout.addWidget(self.feels_like, 0, 0)
        
        self.humidity = DetailWidget("💧", "Humidity")
        details_layout.addWidget(self.humidity, 0, 1)
        
        self.wind = DetailWidget("🌪️", "Wind")
        details_layout.addWidget(self.wind, 0, 2)
        
        self.pressure = DetailWidget("⭕", "Pressure")
        details_layout.addWidget(self.pressure, 0, 3)
        
        layout.addLayout(details_layout)

class MainWindow(QMainWindow):
    """Main window of the weather app"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize services
        self.weather_service = WeatherService()
        self.alert_service = AlertService()
        
        # Create network manager for loading icons
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_icon_response)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 3))  # Reduce height of graph
        self.canvas = FigureCanvasQTAgg(self.figure)
        
        # Store current weather data
        self.current_weather = None
        self.forecast_data = None
        
        self.selected_forecast_card = None  # Track selected card
        
        # Set window icon
        icon_data = Resources.get_app_icon()
        icon = QIcon()
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)
        icon.addPixmap(pixmap)
        self.setWindowIcon(icon)
        
        self.setup_ui()
        
        # Load London weather by default
        self.city_input.setText("London")
        self.update_weather()
        
        # Setup rainbow border animation
        self.setup_border_animation()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Weather App")
        self.setMinimumSize(1200, 800)
        
        # Set window style
        self.setStyleSheet(Styles.MAIN_WINDOW)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Search bar at very top
        search_layout = QHBoxLayout()
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name...")
        self.city_input.setFixedWidth(200)
        self.city_input.returnPressed.connect(self.update_weather)
        search_layout.addWidget(self.city_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.update_weather)
        search_layout.addWidget(self.search_button)
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        # Main content with camera overlay
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left side with weather content
        weather_splitter = QSplitter(Qt.Vertical)
        
        # Current weather
        self.weather_card = WeatherCard()
        weather_splitter.addWidget(self.weather_card)
        
        # Forecast section
        forecast_widget = QWidget()
        forecast_layout = QVBoxLayout(forecast_widget)
        forecast_layout.setContentsMargins(0, 0, 0, 0)
        
        forecast_label = QLabel("7-Day Forecast")
        forecast_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            margin: 0px;
        """)
        forecast_layout.addWidget(forecast_label)
        
        # Horizontal layout for forecast cards
        forecast_row = QHBoxLayout()
        forecast_row.setSpacing(5)
        self.forecast_layout = forecast_row  # Update the reference
        forecast_layout.addLayout(forecast_row)
        
        forecast_widget.setMinimumHeight(150)  # Reduced height since we only need one row
        weather_splitter.addWidget(forecast_widget)
        
        # Graph
        self.canvas.setMinimumHeight(200)
        weather_splitter.addWidget(self.canvas)
        
        content_layout.addWidget(weather_splitter)
        
        # Right side - Alerts and Warnings
        alerts_widget = QWidget()
        alerts_layout = QVBoxLayout(alerts_widget)
        alerts_layout.setContentsMargins(0, 0, 0, 0)
        alerts_layout.setSpacing(5)
        
        # Camera viewer (positioned at top-right)
        self.camera_viewer = CameraViewer()
        self.camera_viewer.setFixedWidth(350)
        self.camera_viewer.setFixedHeight(300)
        alerts_layout.addWidget(self.camera_viewer)
        
        # Alerts frame
        self.alerts_frame = QFrame()
        self.alerts_frame.setStyleSheet(Styles.ALERTS_FRAME)
        alerts_frame_layout = QVBoxLayout(self.alerts_frame)
        alerts_frame_layout.setSpacing(5)
        
        alerts_title = QLabel("Weather Alerts")
        alerts_title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
        """)
        alerts_frame_layout.addWidget(alerts_title)
        
        self.alerts_label = QLabel()
        self.alerts_label.setWordWrap(True)
        alerts_frame_layout.addWidget(self.alerts_label)
        
        alerts_layout.addWidget(self.alerts_frame)
        self.alerts_frame.hide()
        
        # Warnings frame
        self.warnings_frame = QFrame()
        warnings_layout = QVBoxLayout(self.warnings_frame)
        warnings_layout.setSpacing(5)
        
        warnings_header = QLabel("Weather Warnings")
        warnings_header.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            margin: 0px;
        """)
        warnings_layout.addWidget(warnings_header)
        
        self.warnings_layout = QVBoxLayout()
        warnings_layout.addLayout(self.warnings_layout)
        
        alerts_layout.addWidget(self.warnings_frame)
        self.warnings_frame.hide()
        
        alerts_layout.addStretch()
        content_layout.addWidget(alerts_widget)
        
        layout.addWidget(content_widget)
        
        # Setup refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(300000)  # Update every 5 minutes
        
    def setup_border_animation(self):
        """Setup rainbow border animation"""
        self.animation_group = QSequentialAnimationGroup(self)
        
        # Rainbow colors
        colors = [
            QColor("#ff0000"),  # Red
            QColor("#ff00ff"),  # Magenta
            QColor("#0000ff"),  # Blue
            QColor("#00ffff"),  # Cyan
            QColor("#00ff00"),  # Green
            QColor("#ffff00"),  # Yellow
            QColor("#ff0000")   # Back to red
        ]
        
        # Create animation for each color transition
        for i in range(len(colors) - 1):
            anim = QVariantAnimation(self)
            anim.setStartValue(colors[i])
            anim.setEndValue(colors[i + 1])
            anim.setDuration(1000)  # 1 second per color
            anim.valueChanged.connect(self.update_border_color)
            self.animation_group.addAnimation(anim)
        
        # Make the animation loop
        self.animation_group.setLoopCount(-1)
        self.animation_group.start()
    
    def update_border_color(self, color):
        """Update the border color"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Styles.BACKGROUND_COLOR};
                border: 2px solid {color.name()};
            }}
        """)
    
    def update_weather(self):
        """Update weather information"""
        city = self.city_input.text()
        if not city:
            self.show_error("Please enter a city name")
            return
        
        # Get current weather
        weather_data = self.weather_service.get_current_weather(city)
        if weather_data:
            self.current_weather = weather_data  # Store current weather
            self.update_weather_display(weather_data)
            
            # Get and display forecast
            forecast_data = self.weather_service.get_forecast(city)
            if forecast_data:
                self.forecast_data = forecast_data  # Store forecast data
                self.update_forecast_graph(forecast_data)
                self.update_forecast_cards(forecast_data)
        else:
            self.show_error("Error fetching weather data")
    
    def update_weather_display(self, weather_data):
        """Update the weather card display"""
        # Update weather card
        self.weather_card.location_label.setText(weather_data.location)
        
        # Load weather icon
        icon_data = Resources.download_icon(weather_data.icon_code)
        if icon_data:
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.weather_card.icon_label.setPixmap(pixmap)
        
        # Update temperature and description
        self.weather_card.temp_label.setText(f"{weather_data.temperature:.1f}°")
        self.weather_card.desc_label.setText(weather_data.description.title())
        
        # Update details with wind direction and pressure
        self.weather_card.feels_like.value_label.setText(f"{weather_data.feels_like:.1f}°C")
        self.weather_card.humidity.value_label.setText(f"{weather_data.humidity}%")
        self.weather_card.wind.value_label.setText(f"{weather_data.wind_speed} m/s")
        self.weather_card.wind.secondary_label.setText(f"{weather_data.get_wind_direction()}")
        self.weather_card.pressure.value_label.setText(f"{weather_data.pressure} hPa")
        self.weather_card.pressure.secondary_label.setText(f"{weather_data.get_pressure_trend()}")
        
        # Check for alerts
        alerts = self.alert_service.check_alerts(weather_data)
        if alerts:
            self.alerts_label.setText("\n".join(alerts))
            self.alerts_frame.show()
        else:
            self.alerts_frame.hide()
        
        # Check for warnings
        warnings = WeatherWarnings.check_warnings(weather_data)
        if warnings:
            # Clear previous warnings
            for i in reversed(range(self.warnings_layout.count())):
                self.warnings_layout.itemAt(i).widget().setParent(None)
            
            # Add new warnings
            for warning in warnings:
                warning_card = WarningCard(warning)
                self.warnings_layout.addWidget(warning_card)
            
            self.warnings_frame.show()
        else:
            self.warnings_frame.hide()
    
    def show_error(self, message: str):
        """Show error message"""
        self.alerts_label.setText(message)
        self.alerts_frame.show()
    
    def update_forecast_graph(self, forecast_data, selected_date=None):
        """Update the forecast graph"""
        self.figure.clear()
        
        # Set figure background color
        self.figure.patch.set_facecolor(Styles.BACKGROUND_COLOR)
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(Styles.GRAPH_BG)
        
        # Format dates for x-axis
        dates = [f.timestamp.strftime('%a\n%m-%d') for f in forecast_data.daily_forecasts]
        temps = [f.temperature for f in forecast_data.daily_forecasts]
        
        # Plot with style
        ax.plot(dates, temps, marker='o', color=Styles.PRIMARY_COLOR, 
               linewidth=2, markersize=8)
        
        # Highlight selected date if provided
        if selected_date:
            for i, date in enumerate(forecast_data.daily_forecasts):
                if date.timestamp.date() == selected_date.date():
                    ax.plot(i, date.temperature, 'o', 
                           color=Styles.PRIMARY_DARK, 
                           markersize=12, 
                           markeredgewidth=2,
                           markeredgecolor=Styles.TEXT_COLOR)
                    break
        
        # Add temperature labels above points
        for i, temp in enumerate(temps):
            ax.annotate(f'{temp:.1f}°C', 
                       (i, temp), 
                       textcoords="offset points", 
                       xytext=(0,10), 
                       ha='center',
                       color=Styles.TEXT_COLOR)
        
        # Style title and labels
        ax.set_title(f"7-Day Forecast for {forecast_data.location}", 
                    fontsize=14, pad=20, color=Styles.TEXT_COLOR)
        ax.set_xlabel("Date", fontsize=12, color=Styles.TEXT_COLOR)
        ax.set_ylabel("Temperature (°C)", fontsize=12, color=Styles.TEXT_COLOR)
        
        # Style the grid
        ax.grid(True, linestyle='--', alpha=0.3, color=Styles.GRAPH_GRID)
        
        # Style the spines
        for spine in ax.spines.values():
            spine.set_color(Styles.BORDER_COLOR)
        
        # Style tick labels
        ax.tick_params(axis='both', colors=Styles.TEXT_COLOR)
        
        # Adjust layout to prevent label cutoff
        self.figure.tight_layout()
        self.canvas.draw()

    def update_forecast_cards(self, forecast_data):
        """Update the forecast cards"""
        # Clear previous forecast cards
        if self.selected_forecast_card:
            self.selected_forecast_card = None
        
        for i in reversed(range(self.forecast_layout.count())):
            item = self.forecast_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        # Add new forecast cards in a single row
        for forecast in forecast_data.daily_forecasts:
            card = ForecastCard(forecast)
            card.clicked.connect(self.on_forecast_clicked)
            self.forecast_layout.addWidget(card)
            # Add a small stretch factor to distribute cards evenly
            self.forecast_layout.addStretch(1)
    
    def on_forecast_clicked(self, forecast_data):
        """Handle forecast card clicks"""
        # Update selection
        sender = self.sender()
        if self.selected_forecast_card:
            self.selected_forecast_card.set_selected(False)
        self.selected_forecast_card = sender
        sender.set_selected(True)
        
        # Update the main weather display with the forecast data
        self.update_weather_display(forecast_data)
        
        # Highlight the selected day in the graph
        if self.forecast_data:
            self.update_forecast_graph(self.forecast_data, selected_date=forecast_data.timestamp)
    
    def handle_icon_response(self, reply: QNetworkReply):
        """Handle the network response for weather icon"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.weather_card.icon_label.setPixmap(pixmap)
        else:
            print(f"Error loading weather icon: {reply.errorString()}")
        reply.deleteLater() 