import requests
from typing import List, Dict, Optional
from ..utils.config import Config
import time

class FrigateService:
    """Service for interacting with Frigate API"""
    
    def __init__(self):
        self.base_url = Config.FRIGATE_URL
        self.api_key = Config.FRIGATE_API_KEY
        self.cache = {}  # Cache for snapshots
        self.cache_timeout = 1  # Cache timeout in seconds
        
        # Setup headers if API key is provided
        self.headers = {}
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def get_cameras(self) -> List[Dict]:
        """Get list of available cameras"""
        try:
            response = requests.get(f"{self.base_url}/api/config", headers=self.headers)
            response.raise_for_status()
            config = response.json()
            
            cameras = []
            for name, details in config.get('cameras', {}).items():
                cameras.append({
                    'name': name,
                    'width': details.get('width', 1280),
                    'height': details.get('height', 720),
                    'fps': details.get('fps', 30)
                })
            return cameras
        except Exception as e:
            print(f"Error getting camera list: {e}")
            return []
    
    def get_camera_snapshot(self, camera_name: str) -> Optional[bytes]:
        """Get latest snapshot from camera with caching"""
        current_time = time.time()
        
        # Check cache
        if camera_name in self.cache:
            cached_time, cached_data = self.cache[camera_name]
            if current_time - cached_time < self.cache_timeout:
                return cached_data
        
        try:
            response = requests.get(
                f"{self.base_url}/api/{camera_name}/latest.jpg",
                headers=self.headers,
                timeout=2  # Add timeout
            )
            response.raise_for_status()
            
            # Update cache
            self.cache[camera_name] = (current_time, response.content)
            return response.content
            
        except Exception as e:
            print(f"Error getting camera snapshot: {e}")
            # Return cached data if available
            if camera_name in self.cache:
                return self.cache[camera_name][1]
            return None
    
    def get_camera_stream_url(self, camera_name: str) -> str:
        """Get the MJPEG stream URL for a camera"""
        return f"{self.base_url}/api/{camera_name}/stream" 