# main.py
"""
Main entry point for the Smart Speed Control Simulation.
Initializes Pygame, creates the game window, and runs the main game loop.
"""

import pygame
import sys
import time
from config import *
from vehicle import Vehicle
from world import World
from ui import UI
from speed_controller import SpeedController, OVER_SPEED, WARNING_1, WARNING_2
from mqtt_client import MQTTClient
from datalogger import DataLogger
from audio import generate_beep_sound

class Game:
    def __init__(self):
        """
        Initializes the game, Pygame, and sets up the screen.
        """
        pygame.mixer.pre_init(44100, -16, 2, 512) # Setup mixer
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects and sound
        self.world = World()
        self.player = Vehicle(self.world.road_rect.centerx, 150)
        self.ui = UI()
        self.speed_controller = SpeedController(OVERSPEED_DURATION_LIMIT)
        self.logger = DataLogger()
        self.beep_sound = generate_beep_sound()
        self.last_beep_time = 0
        
        # Init MQTT Client
        self.mqtt_client = MQTTClient()
        self.mqtt_client.start()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Camera offset
        self.camera = pygame.Vector2(0, 0)

        # Game state
        self.current_zone = None
        self.in_camera_zone = False
        self.speed_status = "Safe"
        self.is_regulating = False
        self.is_override_mode = False
        self.last_mqtt_publish_time = 0
        self.last_history_log_time = 0
        self.was_overspeeding = False
        self.was_regulating = False

    def run(self):
        """
        The main game loop.
        """
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update()
            self._draw()
        
        self.quit()

    def _handle_events(self):
        """
        Handles all game events, like keyboard input and window-closing.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    self.is_override_mode = not self.is_override_mode
                    self.logger.log_event("OVERRIDE_TOGGLED", self.player.get_speed_kph(), 0, "N/A", f"Override set to {self.is_override_mode}")

        self.player.handle_input(self.dt)

    def _update(self):
        """
        Updates the state of all game objects.
        """
        self.all_sprites.update(self.dt)
        
        # Update camera to follow the player
        self.camera.y = self.player.position.y - SCREEN_HEIGHT / 2
        # Clamp camera scrolling at the top and bottom of the world
        if self.camera.y < 0:
            self.camera.y = 0
        if self.camera.y > WORLD_HEIGHT - SCREEN_HEIGHT:
            self.camera.y = WORLD_HEIGHT - SCREEN_HEIGHT

        self.current_zone = self.world.get_zone_at(self.player.position)
        self.in_camera_zone = self.world.is_in_speed_camera_zone(self.player.rect)

        speed_limit = DEFAULT_MAX_SPEED_KPH
        zone_name = "Open Road"
        if self.current_zone:
            speed_limit = self.current_zone.speed_limit
            zone_name = self.current_zone.name

        self.speed_status, self.is_regulating = self.speed_controller.update(
            self.player.get_speed_kph(), speed_limit, WARNING_BUFFER, self.in_camera_zone
        )

        # Emergency override bypasses regulation
        if self.is_override_mode:
            self.is_regulating = False
            self.speed_controller.is_regulating = False

        if self.is_regulating:
            self.player.set_max_speed_kph(speed_limit)
        else:
            self.player.set_max_speed_kph(DEFAULT_MAX_SPEED_KPH)

        self._log_data(zone_name, speed_limit)
            
        if time.time() - self.last_mqtt_publish_time > 1.0:
            self._publish_telemetry(zone_name, speed_limit)
            self.last_mqtt_publish_time = time.time()

        # Audio feedback for warnings
        if self.speed_status in [WARNING_1, WARNING_2] and not self.is_override_mode:
             # Beep frequency increases with urgency (0.8s for Warning 1, 0.4s for Warning 2)
             interval = 0.8 if self.speed_status == WARNING_1 else 0.4
             if time.time() - self.last_beep_time > interval:
                 self.beep_sound.play()
                 self.last_beep_time = time.time()

    def _log_data(self, zone_name, speed_limit):
        is_overspeeding = self.speed_status == OVER_SPEED
        if is_overspeeding and not self.was_overspeeding:
            details = "Caught by speed camera" if self.in_camera_zone else ""
            self.logger.log_event("OVER_SPEED_WARNING", self.player.get_speed_kph(), speed_limit, zone_name, details)
        
        if self.is_regulating and not self.was_regulating:
            self.logger.log_event("REGULATION_ACTIVATED", self.player.get_speed_kph(), speed_limit, zone_name)

        self.was_overspeeding = is_overspeeding
        self.was_regulating = self.is_regulating

        if time.time() - self.last_history_log_time > 2.0:
            self.logger.log_speed_history(self.player.get_speed_kph(), speed_limit, zone_name)
            self.last_history_log_time = time.time()

    def _publish_telemetry(self, zone_name, speed_limit):
        """
        Constructs and publishes the vehicle telemetry data.
        """
        payload = {
            "timestamp": time.time(),
            "vehicle_id": "CAR-01",
            "location": { "x": self.player.position.x, "y": self.player.position.y },
            "speed_kph": round(self.player.get_speed_kph(), 2),
            "zone": zone_name,
            "speed_limit_kph": speed_limit,
            "speed_status": self.speed_status,
            "is_regulation_active": self.is_regulating,
            "in_camera_zone": self.in_camera_zone,
            "override_mode_active": self.is_override_mode
        }
        self.mqtt_client.publish(MQTT_TOPIC_VEHICLE_TELEMETRY, payload)

    def _draw(self):
        """
        Draws all game objects to the screen, applying the camera offset.
        """
        self.screen.fill(GRASS_GREEN)
        
        # Draw the world with the camera offset
        self.world.draw(self.screen, self.camera)
        
        # Draw sprites with the camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera))
        
        # UI elements are drawn without the camera offset, so they stay fixed
        self.ui.draw_dashboard(self.screen, self.player, self.current_zone, self.speed_status, self.is_regulating, self.in_camera_zone, self.is_override_mode)
        self.ui.draw_controls_guide(self.screen)
        
        pygame.display.flip()

    def quit(self):
        """
        Quits Pygame and exits the program.
        """
        self.mqtt_client.stop()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
