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
        speed_kph = abs(vehicle.get_speed_kph()) # Show absolute speed
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
        speed_text = f"{speed_kph:.0f}"
        self._draw_text(screen, "SPEED", self.font_medium, WHITE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 10))
        self._draw_text(screen, speed_text, self.font_large, status_color, (self.dashboard_bg.left + 50, self.dashboard_bg.top + 45))
        self._draw_text(screen, "km/h", self.font_small, WHITE, (self.dashboard_bg.left + 100, self.dashboard_bg.top + 55))

        # Display Zone Info
        self._draw_text(screen, f"Zone: {zone_name}", self.font_medium, WHITE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 90))
        self._draw_text(screen, f"Limit: {speed_limit} km/h", self.font_medium, WHITE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 120))

        # Display Override Status
        if is_override_mode:
            self._draw_text(screen, "OVERRIDE ENABLED", self.font_medium, BLUE, (self.dashboard_bg.left + 20, self.dashboard_bg.top + 150))
        
        # Display Top-Screen Status/Warning Messages
        if not is_override_mode:
            if in_camera_zone and speed_status == OVER_SPEED:
                 self.draw_notification(screen, "SPEED CAMERA! Slow Down Immediately!", RED, blink=True)
            elif is_regulating:
                self.draw_notification(screen, "Reducing Speed Step-by-Step...", RED)
            elif speed_status == OVER_SPEED:
                self.draw_notification(screen, "WARNING: Exceeding Speed Limit!", RED, blink=True)
            elif speed_status == WARNING_1:
                self.draw_notification(screen, "1st Warning: Slow Down!", RED, blink=True)
            elif speed_status == WARNING_2:
                self.draw_notification(screen, "2nd Warning: Risk of Regulation!", RED, blink=True)

    def draw_controls_guide(self, screen):
        """
        Draws a guide for the game controls on the screen.
        """
        guide_text = [
            "Controls:",
            "  - Arrow Keys to Move",
            "  - 'O' to Toggle Override"
        ]
        
        # Create a background for the guide
        guide_bg = pygame.Rect(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 90, 210, 80)
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
