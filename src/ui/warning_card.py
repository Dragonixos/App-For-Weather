from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ..utils.styles import Styles
from ..utils.weather_warnings import WeatherWarning, WeatherWarnings

class WarningCard(QFrame):
    """Widget to display a weather warning"""
    def __init__(self, warning: WeatherWarning, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.WARNING_CARD)
        
        # Set color based on severity
        color = WeatherWarnings.SEVERITY_COLORS[warning.severity]
        self.setStyleSheet(f"""
            {Styles.WARNING_CARD}
            QFrame {{
                background-color: {color}22;
                border-color: {color};
            }}
        """)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        
        # Warning icon
        icon = QLabel(warning.icon)
        icon.setObjectName("warningIcon")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)
        
        # Warning text
        text_layout = QVBoxLayout()
        
        title = QLabel(warning.title)
        title.setObjectName("warningTitle")
        text_layout.addWidget(title)
        
        message = QLabel(warning.message)
        message.setObjectName("warningMessage")
        message.setWordWrap(True)
        text_layout.addWidget(message)
        
        layout.addLayout(text_layout)
        layout.addStretch() 