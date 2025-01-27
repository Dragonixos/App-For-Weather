class Styles:
    """Application-wide styles"""
    
    # Colors - Dark Theme with Purple
    PRIMARY_COLOR = "#6200EA"
    PRIMARY_DARK = "#3700B3"
    ACCENT_COLOR = "#E1BEE7"   # Light Purple
    BACKGROUND_COLOR = "#121212"  # Dark background
    CARD_COLOR = "#1E1E1E"    # Slightly lighter than background
    ERROR_COLOR = "#EF5350"   # Lighter red for dark theme
    ERROR_BG = "#311B1B"      # Dark red background
    TEXT_COLOR = "#FFFFFF"    # Light gray text
    BORDER_COLOR = "#2C2C2C"  # Dark gray borders
    SECONDARY_TEXT = "#B0B0B0"
    GRAPH_BG = "#1A1A1A"      # Dark background for graph
    GRAPH_GRID = "#2C2C2C"    # Dark grid lines
    
    # Font families with fallbacks
    FONT_FAMILY = "Noto Sans, Arial, Helvetica, sans-serif"
    MONOSPACE_FONT = "Hack, Consolas, Monaco, monospace"
    
    # Dimensions
    BORDER_RADIUS = "10px"
    PADDING = "20px"
    SPACING = "15px"
    
    # Styles
    RAINBOW_ANIMATION = """
        @keyframes rainbow {
            0% { border-color: #ff0000; }
            17% { border-color: #ff00ff; }
            33% { border-color: #0000ff; }
            50% { border-color: #00ffff; }
            67% { border-color: #00ff00; }
            83% { border-color: #ffff00; }
            100% { border-color: #ff0000; }
        }
    """
    
    MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
            border: 2px solid {PRIMARY_COLOR};
        }}
    """
    
    WEATHER_CARD = f"""
        QFrame {{
            background-color: {CARD_COLOR};
            border-radius: {BORDER_RADIUS};
            padding: {PADDING};
            margin: 10px;
            border: 1px solid {BORDER_COLOR};
        }}
        QLabel {{
            color: {TEXT_COLOR};
            margin: 5px;
        }}
        QLabel#locationLabel {{
            font-size: 24px;
            font-weight: bold;
            color: {PRIMARY_COLOR};
            font-family: {FONT_FAMILY};
        }}
        QLabel#temperatureLabel {{
            font-size: 48px;
            font-weight: bold;
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
        }}
        QLabel#descriptionLabel {{
            font-size: 18px;
            color: {SECONDARY_TEXT};
            font-family: {FONT_FAMILY};
        }}
    """
    
    SEARCH_BAR = f"""
        QLineEdit {{
            padding: 10px;
            border: 1px solid {BORDER_COLOR};
            border-radius: 5px;
            font-size: 14px;
            background-color: {CARD_COLOR};
            color: {TEXT_COLOR};
        }}
        QLineEdit:focus {{
            border-color: {PRIMARY_COLOR};
        }}
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: {BACKGROUND_COLOR};
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY_DARK};
        }}
    """
    
    ALERTS_FRAME = f"""
        QFrame {{
            background-color: {ERROR_BG};
            border-radius: 5px;
            padding: {PADDING};
            border: 1px solid {ERROR_COLOR};
        }}
        QLabel {{
            color: {ERROR_COLOR};
        }}
    """
    
    DETAILS_WIDGET = f"""
        QFrame {{
            background-color: {CARD_COLOR};
            border-radius: 5px;
            padding: 10px;
            border: 1px solid {BORDER_COLOR};
        }}
        QLabel {{
            color: {TEXT_COLOR};
            font-size: 14px;
        }}
    """
    
    WARNING_CARD = f"""
        QFrame {{
            border-radius: 5px;
            padding: 10px;
            margin: 5px;
            border: 1px solid;
        }}
        QLabel {{
            color: inherit;
        }}
        QLabel#warningTitle {{
            font-size: 14px;
            font-weight: bold;
        }}
        QLabel#warningMessage {{
            font-size: 12px;
        }}
        QLabel#warningIcon {{
            font-size: 20px;
        }}
    """
    
    FORECAST_CARD = f"""
        QFrame {{
            background-color: {CARD_COLOR};
            border-radius: 5px;
            padding: 5px;
            margin: 2px;
            border: 1px solid {BORDER_COLOR};
        }}
        QFrame:hover {{
            border-color: {PRIMARY_COLOR};
            background-color: {CARD_COLOR};
        }}
        QLabel {{
            color: {TEXT_COLOR};
        }}
        QLabel#forecastDate {{
            font-size: 12px;
            font-weight: bold;
        }}
        QLabel#forecastTemp {{
            font-size: 16px;
            font-weight: bold;
        }}
        QLabel#forecastDesc {{
            font-size: 11px;
            color: {SECONDARY_TEXT};
        }}
        QLabel#forecastDetailLabel {{
            font-size: 10px;
            color: {SECONDARY_TEXT};
        }}
        QLabel#forecastDetailValue {{
            font-size: 10px;
        }}
        QLabel#forecastDetailSecondary {{
            font-size: 10px;
            color: {SECONDARY_TEXT};
        }}
    """
    
    CAMERA_VIEWER = f"""
        QFrame {{
            background-color: {CARD_COLOR};
            border-radius: {BORDER_RADIUS};
            padding: 10px;
            margin: 0px;
            border: 1px solid {BORDER_COLOR};
        }}
        QComboBox {{
            background-color: {CARD_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: 3px;
            padding: 3px;
        }}
        QComboBox:hover {{
            border-color: {PRIMARY_COLOR};
        }}
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY_DARK};
        }}
    """ 