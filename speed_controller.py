# speed_controller.py
"""
Contains the core logic for monitoring and controlling the vehicle's speed.
"""

import time

# Speed Status Constants
SAFE = "Safe"
APPROACHING_LIMIT = "Approaching Limit"
OVER_SPEED = "Over Speed"

class SpeedController:
    def __init__(self, regulation_time_limit):
        """
        Initializes the speed controller.
        :param regulation_time_limit: Seconds the vehicle can overspeed before regulation.
        """
        self.overspeed_start_time = None
        self.regulation_time_limit = regulation_time_limit
        self.is_regulating = False

    def check_speed_status(self, vehicle_speed, speed_limit, warning_buffer):
        """
        Determines the current speed status of the vehicle.
        :param vehicle_speed: Current speed of the vehicle in km/h.
        :param speed_limit: The speed limit of the current zone in km/h.
        :param warning_buffer: The buffer to trigger the 'Approaching Limit' warning.
        :return: A status string (SAFE, APPROACHING_LIMIT, OVER_SPEED).
        """
        if vehicle_speed > speed_limit:
            return OVER_SPEED
        elif vehicle_speed > speed_limit - warning_buffer:
            return APPROACHING_LIMIT
        else:
            return SAFE

    def update(self, vehicle_speed, speed_limit, warning_buffer, in_camera_zone=False):
        """
        Updates the controller's state based on the vehicle's speed.
        :param vehicle_speed: Current speed of the vehicle in km/h.
        :param speed_limit: The speed limit of the current zone in km/h.
        :param warning_buffer: The buffer for the 'Approaching' warning.
        :param in_camera_zone: Boolean indicating if the vehicle is in a speed camera zone.
        :return: A tuple containing (current_speed_status, is_regulation_active).
        """
        status = self.check_speed_status(vehicle_speed, speed_limit, warning_buffer)

        if status == OVER_SPEED:
            if in_camera_zone:
                # Instant regulation in a speed camera zone
                self.is_regulating = True
            else:
                if self.overspeed_start_time is None:
                    # Start the overspeed timer
                    self.overspeed_start_time = time.time()
                
                # Check if regulation should be activated
                if (time.time() - self.overspeed_start_time) > self.regulation_time_limit:
                    self.is_regulating = True
        else:
            # Reset timer and regulation if not overspeeding
            self.overspeed_start_time = None
            self.is_regulating = False
        
        return status, self.is_regulating
