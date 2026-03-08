# vehicle.py
"""
Vehicle class for the simulation.
Handles the vehicle's state, movement, and rendering.
"""

import pygame
from config import *
from math import sin, cos, radians, copysign

class Vehicle(pygame.sprite.Sprite):
    # This constant converts a speed in km/h to the number of pixels to move per frame.
    # A lower value makes the car appear slower on screen for the same kph value.
    # (km/h -> m/h -> pixels/h -> pixels/s -> pixels/frame)
    KPH_TO_PIXEL_PER_FRAME = (1000 * 15 / 3600) / FPS 

    def __init__(self, x, y, max_speed_kph=DEFAULT_MAX_SPEED_KPH):
        """
        Initializes the vehicle object.
        :param x: Initial x-coordinate.
        :param y: Initial y-coordinate.
        """
        super().__init__()
        # The visual representation of the car is created once on a transparent surface.
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        
        # --- Draw a more detailed car ---
        # Car Body
        pygame.draw.rect(self.image, RED, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=4)
        # Windshield
        pygame.draw.rect(self.image, (173, 216, 230), (2, 5, CAR_WIDTH - 4, 12), border_radius=3)
        # Headlights
        pygame.draw.rect(self.image, YELLOW, (2, 2, 4, 4))
        pygame.draw.rect(self.image, YELLOW, (CAR_WIDTH - 6, 2, 4, 4))
        # Wheels (as simple black rectangles on the side)
        wheel_width, wheel_height = 4, 10
        pygame.draw.rect(self.image, BLACK, (-2, 8, wheel_width, wheel_height), border_radius=2)
        pygame.draw.rect(self.image, BLACK, (CAR_WIDTH - 2, 8, wheel_width, wheel_height), border_radius=2)
        pygame.draw.rect(self.image, BLACK, (-2, CAR_HEIGHT - 18, wheel_width, wheel_height), border_radius=2)
        pygame.draw.rect(self.image, BLACK, (CAR_WIDTH - 2, CAR_HEIGHT - 18, wheel_width, wheel_height), border_radius=2)

        self.original_image = self.image # Store the un-rotated image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Physics state
        self.start_position = pygame.Vector2(x, y)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0) # This vector is used for final movement on screen
        self.angle = 0
        self.speed_kph = 0.0 # The "real" speed of the car, used for all physics calculations

        # Vehicle physics properties (rates are in km/h per second)
        self.max_speed_kph = max_speed_kph      # The current maximum speed allowed
        self.max_reverse_speed_kph = -15.0      # The maximum reverse speed
        self.acceleration_rate = 8.0            # Slower acceleration
        self.brake_power_rate = 25.0            # Slower braking
        self.friction_rate = 4.0                # Lower friction
        self.turn_speed = 0.8                   # Slower turning
        
        # UI Elements
        self.reset_btn_rect = pygame.Rect(SCREEN_WIDTH - 120, 20, 100, 40)
        self.ui_font = pygame.font.SysFont("Arial", 20, bold=True)

    def handle_input(self, dt):
        """
        Handles keyboard input for controlling the vehicle.
        Delta time (dt) is used to make movement frame-rate independent.
        """
        keys = pygame.key.get_pressed()
        
        # Check for mouse click on Reset Button
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.reset_btn_rect.collidepoint(mouse_pos):
            self.reset()
            return

        if keys[pygame.K_r]:
            self.reset()
            return
        
        # Acceleration and Braking
        if keys[pygame.K_UP]:
            self.accelerate(dt)
        elif keys[pygame.K_DOWN]:
            self.brake_and_reverse(dt)
        else:
            self.apply_friction(dt)

        # Turning is allowed when moving, forwards or backwards
        if abs(self.speed_kph) > 1:
            if keys[pygame.K_LEFT]:
                self.turn(-1)
            if keys[pygame.K_RIGHT]:
                self.turn(1)

    def accelerate(self, dt):
        """
        Increases the vehicle's speed, respecting the max speed limit.
        """
        # Only accelerate if we are below the limit. If we are over (due to regulation), don't snap down.
        if self.speed_kph < self.max_speed_kph:
            self.speed_kph += self.acceleration_rate * dt
            self.speed_kph = min(self.speed_kph, self.max_speed_kph)

    def brake_and_reverse(self, dt):
        """
        Decreases the vehicle's speed (brakes) or engages reverse.
        """
        self.speed_kph -= self.brake_power_rate * dt
        self.speed_kph = max(self.speed_kph, self.max_reverse_speed_kph) # Clamp to max reverse speed

    def apply_friction(self, dt):
        """
        Applies natural deceleration when no input is given.
        Brings the car to a stop from either forward or reverse motion.
        """
        if self.speed_kph > 0:
            self.speed_kph -= self.friction_rate * dt
            self.speed_kph = max(0, self.speed_kph)
        elif self.speed_kph < 0:
            self.speed_kph += self.friction_rate * dt
            self.speed_kph = min(0, self.speed_kph)

    def turn(self, direction):
        """
        Turns the vehicle left or right.
        :param direction: -1 for left, 1 for right.
        """
        # Invert turning direction when reversing for more intuitive control
        turn_direction = direction if self.speed_kph >= 0 else -direction
        
        # Turning is faster at higher speeds for a more arcade-like feel
        turn_rate = self.turn_speed * (abs(self.speed_kph) / 50) 
        self.angle += turn_rate * turn_direction
        self.angle %= 360 # Keep angle between 0 and 360

    def reset(self):
        """
        Resets the vehicle to its starting position and state.
        """
        self.position = pygame.Vector2(self.start_position)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.speed_kph = 0.0
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        """
        Updates the vehicle's position and rotation based on its current speed and angle.
        :param dt: Delta time (time since last frame).
        """
        # Smoothly reduce speed if over the limit (Step-by-step reduction)
        if self.speed_kph > self.max_speed_kph:
            self.speed_kph -= self.brake_power_rate * dt * 0.3 # Gentle braking for regulation
            if self.speed_kph < self.max_speed_kph:
                self.speed_kph = self.max_speed_kph

        # 1. Convert the abstract speed (km/h) into a 2D velocity vector for the screen.
        pixel_speed_per_frame = self.speed_kph * self.KPH_TO_PIXEL_PER_FRAME
        # `from_polar` creates a vector from an angle and length.
        # Angle is adjusted for Pygame's coordinate system (0 degrees is up).
        self.velocity.from_polar((pixel_speed_per_frame, -self.angle + 90))

        # 2. Update the vehicle's position on the screen.
        self.position += self.velocity
        
        # 4. Keep the car within the world boundaries
        half_width = self.rect.width / 2
        half_height = self.rect.height / 2
        
        if self.position.x < half_width:
            self.position.x = half_width
            self.speed_kph = 0 # Stop the car on collision
        elif self.position.x > WORLD_WIDTH - half_width:
            self.position.x = WORLD_WIDTH - half_width
            self.speed_kph = 0
            
        if self.position.y < half_height:
            self.position.y = half_height
            self.speed_kph = 0
        elif self.position.y > WORLD_HEIGHT - half_height:
            self.position.y = WORLD_HEIGHT - half_height
            self.speed_kph = 0
        
        # 5. Rotate the car's image and update its screen rectangle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        """
        Draws the vehicle on the screen.
        """
        screen.blit(self.image, self.rect)
        
        # Draw Reset Button
        # Change color on hover
        btn_color = (200, 50, 50) if self.reset_btn_rect.collidepoint(pygame.mouse.get_pos()) else (150, 0, 0)
        pygame.draw.rect(screen, btn_color, self.reset_btn_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.reset_btn_rect, 2, border_radius=5) # Border
        text_surf = self.ui_font.render("RESET", True, WHITE)
        text_rect = text_surf.get_rect(center=self.reset_btn_rect.center)
        screen.blit(text_surf, text_rect)

    def get_speed_kph(self):
        """
        Returns the vehicle's current speed in km/h.
        """
        return self.speed_kph

    def set_max_speed_kph(self, new_limit):
        """
        Sets a new maximum speed limit for the vehicle, often enforced by the speed controller.
        """
        self.max_speed_kph = new_limit
        # We do NOT clamp instantly here anymore, to allow for smooth "step-by-step" reduction in update().
