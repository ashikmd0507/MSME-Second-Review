# config.py
"""
Configuration file for the simulation.
Stores constants like screen dimensions, colors, and game settings.
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Smart Speed Control Simulation"

# World dimensions
WORLD_WIDTH = SCREEN_WIDTH
WORLD_HEIGHT = SCREEN_HEIGHT * 4 # Make the world 4 screens tall

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# World colors
ROAD_GRAY = (80, 80, 80)
GRASS_GREEN = (34, 139, 34)

# Font settings
FONT_NAME = 'Arial'
FONT_SIZE_SMALL = 18
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 36

# Vehicle settings
CAR_WIDTH = 30
CAR_HEIGHT = 60

# Zone Settings
ZONE_ALPHA = 50 # Transparency of the zone colors
SPEED_LIMITS = {
    "Highway": 80,
    "City Road": 50,
    "School Zone": 30,
    "Village Area": 40
}

ZONE_COLORS = {
    "Highway": (0, 150, 0, ZONE_ALPHA),      # Dark Green
    "City Road": (100, 100, 100, ZONE_ALPHA), # Dark Gray
    "School Zone": (255, 165, 0, ZONE_ALPHA),  # Orange
    "Village Area": (139, 69, 19, ZONE_ALPHA)   # Saddle Brown
}
SPEED_CAMERA_COLOR = (255, 0, 255, 100) # Magenta with some transparency

# Speed Control Settings
WARNING_BUFFER = 5  # Show 'Approaching Limit' if within 5 km/h of the speed limit
OVERSPEED_DURATION_LIMIT = 3  # seconds before auto-regulation kicks in
DEFAULT_MAX_SPEED_KPH = 120 # The vehicle's unrestricted top speed

# MQTT Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
# It's good practice to use a unique client ID
MQTT_CLIENT_ID = "smart_speed_controller_simulation" 
MQTT_TOPIC_VEHICLE_TELEMETRY = "vehicle/telemetry"
MQTT_TOPIC_SPEED_CONTROL = "vehicle/speed_control"
