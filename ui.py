# ui.py
"""
UI class for the simulation.
Handles the drawing of the dashboard, warnings, and other on-screen information.
"""

import pygame
from config import *
from speed_controller import SAFE, APPROACHING_LIMIT, OVER_SPEED, WARNING_1, WARNING_2

class UI:
    def __init__(self):
        """
        Initializes the UI elements, fonts, etc.
        """
        self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)
        self.font_medium = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.SysFont(FONT_NAME, FONT_SIZE_LARGE)
        self.dashboard_bg = pygame.Rect(10, 10, 300, 180)

    def _draw_text(self, screen, text, font, color, position, centered=False):
        """
        Helper function to draw text on the screen.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = position
        else:
            text_rect.topleft = position
        screen.blit(text_surface, text_rect)

    def draw_dashboard(self, screen, vehicle, current_zone, speed_status, is_regulating, in_camera_zone, is_override_mode):
        """
        Draws the main dashboard with vehicle and zone information.
        """
        # Determine background color. Flash red if overspeeding.
        bg_color = (0, 0, 0, 120)
        if speed_status == OVER_SPEED and not is_override_mode and pygame.time.get_ticks() % 500 < 250:
            bg_color = (180, 0, 0, 180) # Flashing red background

        # Draw a semi-transparent background for the dashboard
        dashboard_surface = pygame.Surface((self.dashboard_bg.width, self.dashboard_bg.height), pygame.SRCALPHA)
        dashboard_surface.fill(bg_color)
        screen.blit(dashboard_surface, self.dashboard_bg.topleft)

        # Get data
        raw_speed = vehicle.get_speed_kph()
        zone_name = "N/A"
        speed_limit = 0
        
        if current_zone:
            zone_name = current_zone.name
            speed_limit = current_zone.speed_limit

        # Determine color based on status
        status_color = GREEN
        if speed_status == APPROACHING_LIMIT:
            status_color = YELLOW
        elif speed_status in [OVER_SPEED, WARNING_1, WARNING_2]:
            status_color = RED
        
        if is_override_mode:
            status_color = BLUE # Use a different color to show override is active

        # Display Speed
        self._draw_text(screen, "CURRENT SPEED", self.font_medium, WHITE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 10))
        
        if raw_speed < -1:
            self._draw_text(screen, "REVERSE", self.font_medium, status_color, (self.dashboard_bg.left + 50, self.dashboard_bg.top + 50))
        else:
            self._draw_text(screen, f"{abs(raw_speed):.0f}", self.font_large, status_color, (self.dashboard_bg.left + 50, self.dashboard_bg.top + 45))
            self._draw_text(screen, "km/h", self.font_small, WHITE, (self.dashboard_bg.left + 100, self.dashboard_bg.top + 55))

        # Display Zone Info
        self._draw_text(screen, f"Zone Name: {zone_name}", self.font_medium, WHITE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 90))
        self._draw_text(screen, f"Speed Limit: {speed_limit} km/h", self.font_medium, WHITE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 120))

        # Display Override Status
        if is_override_mode:
            self._draw_text(screen, "OVERRIDE ENABLED", self.font_medium, WHITE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 150))
        
        # Display Top-Screen Status/Warning Messages
        if not is_override_mode:
            if in_camera_zone and speed_status == OVER_SPEED:
                 self.draw_notification(screen, "SPEED CAMERA! Slow Down Immediately!", RED, blink=True)
            elif is_regulating:
                self.draw_notification(screen, "Regulating Speed According to the Speed Limit", RED)
            elif speed_status == OVER_SPEED:
                self.draw_notification(screen, "WARNING: Exceeding Speed Limit!", RED, blink=True)
            elif speed_status == WARNING_1:
                self.draw_notification(screen, "1st Warning: Slow Down!", RED, blink=True)
            elif speed_status == WARNING_2:
                self.draw_notification(screen, "2nd Warning: Slow Down!", RED, blink=True)

    def draw_controls_guide(self, screen):
        """
        Draws a guide for the game controls on the screen.
        """
        guide_text = [
            "Controls:",
            "  1. Arrow Keys to Move",
            "  2. 'O' to Toggle Override",
            "  3. 'R' to Reset Position"
        ]
        
        # Create a background for the guide
        guide_bg = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 110, 240, 100)
        guide_surface = pygame.Surface((guide_bg.width, guide_bg.height), pygame.SRCALPHA)
        guide_surface.fill((0, 0, 0, 120))
        screen.blit(guide_surface, guide_bg.topleft)
        
        # Draw each line of text
        for i, line in enumerate(guide_text):
            self._draw_text(screen, line, self.font_small, WHITE, (guide_bg.left + 10, guide_bg.top + 5 + i * 22))

    def draw_notification(self, screen, text, color, blink=False):
        """
        Draws a prominent notification message at the top of the screen.
        """
        if blink and pygame.time.get_ticks() % 1000 < 500:
            return # Blink effect

        bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        pygame.draw.rect(screen, color, bg_rect)
        self._draw_text(screen, text, self.font_medium, WHITE, bg_rect.center, centered=True)

    def draw_minimap(self, screen, vehicle, world):
        """
        Draws a small square minimap in the top-right corner (Whole World View).
        """
        map_size = 150
        margin = 20
        map_x = SCREEN_WIDTH - map_size - margin
        map_y = margin
        map_rect = pygame.Rect(map_x, map_y, map_size, map_size)
        
        # Draw Background
        pygame.draw.rect(screen, (30, 30, 30), map_rect)
        
        # Calculate scale to fit the whole world into the square
        scale_w = map_size / WORLD_WIDTH
        scale_h = map_size / WORLD_HEIGHT
        scale = min(scale_w, scale_h)
        
        # Calculate offsets to center the map content
        content_width = WORLD_WIDTH * scale
        content_height = WORLD_HEIGHT * scale
        offset_x = map_rect.left + (map_size - content_width) / 2
        offset_y = map_rect.top + (map_size - content_height) / 2
        
        # Draw Zones
        for zone in world.zones:
            z_x = offset_x + zone.rect.x * scale
            z_y = offset_y + zone.rect.y * scale
            z_w = zone.rect.width * scale
            z_h = zone.rect.height * scale
            pygame.draw.rect(screen, zone.color, (z_x, z_y, z_w, z_h))

        # Draw Player
        p_x = offset_x + vehicle.position.x * scale
        p_y = offset_y + vehicle.position.y * scale
        pygame.draw.circle(screen, RED, (int(p_x), int(p_y)), 3)
        
        # Draw Border
        pygame.draw.rect(screen, WHITE, map_rect, 2)
        
        # Draw Label
        self._draw_text(screen, "Aerial View", self.font_small, WHITE, (map_rect.centerx, map_rect.bottom + 15), centered=True)

    def draw_trip_info(self, screen, driver_name, source, destination, timestamp):
        """
        Draws the driver and trip details at the bottom-left corner.
        """
        # Background box
        bg_rect = pygame.Rect(10, SCREEN_HEIGHT - 90, 320, 80)
        s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        screen.blit(s, bg_rect.topleft)
        
        self._draw_text(screen, f"Trip Details: {source} to {destination}", self.font_small, WHITE, (bg_rect.left + 10, bg_rect.top + 30))
        self._draw_text(screen, f"Driver Name: {driver_name}", self.font_small, WHITE, (bg_rect.left + 10, bg_rect.top + 10))
        self._draw_text(screen, f"Time: {timestamp}", self.font_small, WHITE, (bg_rect.left + 10, bg_rect.top + 50))
