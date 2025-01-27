from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QComboBox, QSizeGrip,
                           QMainWindow)
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from ..api.frigate_service import FrigateService
from ..utils.styles import Styles

class ResizableLabel(QFrame):
    """A resizable and movable label for camera display"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            background-color: {Styles.BACKGROUND_COLOR};
            border: 1px solid {Styles.BORDER_COLOR};
            border-radius: 5px;
            padding: 5px;
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        
        # Size grip in bottom-right corner
        self.size_grip = QSizeGrip(self)
        self.size_grip.setStyleSheet(f"""
            background-color: {Styles.PRIMARY_COLOR};
            border-radius: 2px;
        """)
        
        # Position size grip
        self.size_grip.setFixedSize(16, 16)
        self.size_grip.move(self.width() - 16, self.height() - 16)
    
    def setPixmap(self, pixmap):
        """Set the image pixmap"""
        if pixmap:
            scaled = pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
    
    def resizeEvent(self, event: QResizeEvent):
        """Handle resize events"""
        super().resizeEvent(event)
        # Update size grip position
        self.size_grip.move(self.width() - 16, self.height() - 16)
        # Rescale image if exists
        if self.image_label.pixmap():
            self.setPixmap(self.image_label.pixmap().copy())

class FullscreenCameraWindow(QMainWindow):
    """A window for displaying a camera feed in larger size"""
    
    def __init__(self, camera_name, frigate_service, parent=None):
        super().__init__(parent)
        self.camera_name = camera_name
        self.frigate_service = frigate_service
        
        # Set window icon
        self.setWindowIcon(parent.windowIcon())
        
        # Setup window properties
        self.setWindowTitle(f"Camera: {camera_name}")
        self.setMinimumSize(800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Camera display
        self.camera_view = QLabel()
        self.camera_view.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_view)
        
        # Controls
        controls = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_camera)
        controls.addWidget(self.refresh_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        controls.addWidget(self.close_btn)
        
        layout.addLayout(controls)
        
        # Faster refresh rate for fullscreen
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_camera)
        self.timer.start(1000)  # Refresh every 1 second
        
        # Cache the last image to prevent flickering
        self.last_image = None
        
        # Initial refresh
        self.refresh_camera()
    
    def refresh_camera(self):
        """Refresh the camera view"""
        try:
            image_data = self.frigate_service.get_camera_snapshot(self.camera_name)
            if image_data:
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                if not pixmap.isNull():
                    self.last_image = pixmap
                    scaled = pixmap.scaled(
                        self.camera_view.size(),
                        Qt.KeepAspectRatio,
                        Qt.FastTransformation  # Faster scaling
                    )
                    self.camera_view.setPixmap(scaled)
        except Exception as e:
            print(f"Error refreshing camera: {e}")
    
    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        if self.camera_view.pixmap():
            self.refresh_camera()

class CameraViewer(QFrame):
    """Widget to display Frigate cameras"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.CAMERA_VIEWER)
        
        self.frigate_service = FrigateService()
        self.current_camera = None
        self.fullscreen_window = None  # Store reference to fullscreen window
        
        # Setup UI
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Header with controls
        header = QHBoxLayout()
        
        # Title
        title = QLabel("Security Camera")
        title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
        """)
        header.addWidget(title)
        
        # Camera selector
        self.camera_selector = QComboBox()
        self.camera_selector.setMaximumWidth(150)
        self.camera_selector.currentTextChanged.connect(self.on_camera_changed)
        header.addWidget(self.camera_selector)
        
        # Refresh button
        self.refresh_btn = QPushButton("⟳")
        self.refresh_btn.setFixedSize(24, 24)
        self.refresh_btn.clicked.connect(self.refresh_camera)
        header.addWidget(self.refresh_btn)
        
        # Fullscreen button
        self.fullscreen_btn = QPushButton("⛶")  # Unicode symbol for fullscreen
        self.fullscreen_btn.setFixedSize(24, 24)
        self.fullscreen_btn.clicked.connect(self.show_fullscreen)
        header.addWidget(self.fullscreen_btn)
        
        layout.addLayout(header)
        
        # Camera display
        self.camera_view = ResizableLabel()
        self.camera_view.setMinimumSize(320, 240)
        self.camera_view.mouseDoubleClickEvent = self.on_double_click
        layout.addWidget(self.camera_view)
        
        # Load cameras
        self.load_cameras()
        
        # Faster refresh for thumbnail
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_camera)
        self.timer.start(2000)  # Refresh every 2 seconds
        
        # Cache the last image
        self.last_image = None
    
    def load_cameras(self):
        """Load available cameras"""
        cameras = self.frigate_service.get_cameras()
        self.camera_selector.clear()
        for camera in cameras:
            self.camera_selector.addItem(camera['name'])
    
    def on_camera_changed(self, camera_name):
        """Handle camera selection change"""
        self.current_camera = camera_name
        self.refresh_camera()
    
    def refresh_camera(self):
        """Refresh the camera view"""
        if not self.current_camera:
            return
            
        try:
            image_data = self.frigate_service.get_camera_snapshot(self.current_camera)
            if image_data:
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                if not pixmap.isNull():
                    self.last_image = pixmap
                    self.camera_view.setPixmap(pixmap)
        except Exception as e:
            if self.last_image:  # Use cached image if refresh fails
                self.camera_view.setPixmap(self.last_image)
            print(f"Error refreshing camera: {e}")
    
    def show_fullscreen(self):
        """Show the current camera in a fullscreen window"""
        if self.current_camera:
            if self.fullscreen_window:
                self.fullscreen_window.close()
            self.fullscreen_window = FullscreenCameraWindow(
                self.current_camera,
                self.frigate_service
            )
            self.fullscreen_window.show()
    
    def on_double_click(self, event):
        """Handle double click events on the camera view"""
        if event.button() == Qt.LeftButton:
            self.show_fullscreen()
    
    def resizeEvent(self, event):
        """Handle widget resize events"""
        super().resizeEvent(event)
        self.refresh_camera() 