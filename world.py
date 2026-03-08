# world.py
"""
World class for the simulation.
Manages the map layout, speed zones, and their properties.
"""

import pygame
from config import *

class Zone:
    """
    Represents a single speed limit zone.
    """
    def __init__(self, rect, name, speed_limit, color):
        self.rect = rect
        self.name = name
        self.speed_limit = speed_limit
        self.color = color
        # The surface for the colored overlay
        self.surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.surface.fill(color)

class World:
    def __init__(self):
        """
        Initializes the game world, defines the zones, and sets up fonts.
        """
        self.zones = []
        self.speed_camera_zones = []
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_LARGE, bold=True)
        self.road_rect = None # Single rectangle for the entire road
        
        self._create_long_road()
        self._create_speed_cameras()

    def _create_long_road(self):
        """
        Creates one long vertical road and the zones along it.
        """
        road_width = 400
        self.road_rect = pygame.Rect((WORLD_WIDTH - road_width) / 2, 0, road_width, WORLD_HEIGHT)

        # Define zone segments along the long road
        zone_height = WORLD_HEIGHT / 4
        highway_rect = pygame.Rect(self.road_rect.left, 0, road_width, zone_height)
        city_rect = pygame.Rect(self.road_rect.left, zone_height, road_width, zone_height)
        school_rect = pygame.Rect(self.road_rect.left, zone_height * 2, road_width, zone_height)
        village_rect = pygame.Rect(self.road_rect.left, zone_height * 3, road_width, zone_height)

        self.zones.append(Zone(highway_rect, "Highway", SPEED_LIMITS["Highway"], ZONE_COLORS["Highway"]))
        self.zones.append(Zone(city_rect, "City Road", SPEED_LIMITS["City Road"], ZONE_COLORS["City Road"]))
        self.zones.append(Zone(school_rect, "School Zone", SPEED_LIMITS["School Zone"], ZONE_COLORS["School Zone"]))
        self.zones.append(Zone(village_rect, "Village Area", SPEED_LIMITS["Village Area"], ZONE_COLORS["Village Area"]))

    def _create_speed_cameras(self):
        """
        Creates the speed camera zones on the new long road.
        """
        # A camera in the city zone
        camera1 = pygame.Rect(self.road_rect.centerx - 10, WORLD_HEIGHT * 0.4, 20, 100)
        self.speed_camera_zones.append(camera1)
        # A camera in the school zone
        camera2 = pygame.Rect(self.road_rect.left, WORLD_HEIGHT * 0.6, self.road_rect.width, 20)
        self.speed_camera_zones.append(camera2)

    def get_zone_at(self, position):
        """
        Finds the zone at a given position.
        """
        for zone in self.zones:
            if zone.rect.collidepoint(position):
                return zone
        return None

    def is_in_speed_camera_zone(self, vehicle_rect):
        """
        Checks if the vehicle is currently inside any speed camera zone.
        """
        for cam_zone in self.speed_camera_zones:
            if cam_zone.colliderect(vehicle_rect):
                return True
        return False

    def draw(self, screen, camera_offset):
        """
        Draws the visible portion of the world map based on the camera offset.
        :param screen: The Pygame screen surface.
        :param camera_offset: A pygame.Vector2 representing the camera's position.
        """
        # Draw the main road with a border
        bordered_road = self.road_rect.inflate(20, 0)
        pygame.draw.rect(screen, (20, 20, 20), bordered_road.move(-camera_offset))
        pygame.draw.rect(screen, ROAD_GRAY, self.road_rect.move(-camera_offset))
        self._draw_lane_lines(screen, self.road_rect.move(-camera_offset))

        # Draw the zones and their labels
        for zone in self.zones:
            # Apply camera offset to the zone's drawing position
            offset_rect = zone.rect.move(-camera_offset)
            screen.blit(zone.surface, offset_rect)
            
            # Draw the zone name and speed limit text, also offset
            label_text = f"{zone.name} ({zone.speed_limit} km/h)"
            label_surface = self.font.render(label_text, True, WHITE)
            label_rect = label_surface.get_rect(center=offset_rect.center)
            screen.blit(label_surface, label_rect)
        
        # Draw the speed camera zones
        for cam_zone in self.speed_camera_zones:
            offset_cam_rect = cam_zone.move(-camera_offset)
            cam_surface = pygame.Surface((offset_cam_rect.width, offset_cam_rect.height), pygame.SRCALPHA)
            cam_surface.fill(SPEED_CAMERA_COLOR)
            screen.blit(cam_surface, offset_cam_rect.topleft)

    def _draw_lane_lines(self, screen, road_draw_rect):
        """
        Draws dashed lane lines in the center of the visible road area.
        """
        center_x = road_draw_rect.centerx
        for y in range(road_draw_rect.top, road_draw_rect.bottom, 40):
            # Only draw lines that are visible on screen
            if y > -40 and y < SCREEN_HEIGHT:
                start_pos = (center_x, y)
                end_pos = (center_x, y + 20)
                pygame.draw.line(screen, YELLOW, start_pos, end_pos, 4)

