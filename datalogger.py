# datalogger.py
"""
Handles logging of vehicle data, such as speed history and events.
"""

import csv
import time
from pathlib import Path

class DataLogger:
    def __init__(self, log_dir="data_logs"):
        """
        Initializes the logger and creates the log files with headers.
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.events_log_path = self.log_dir / "overspeed_events.csv"
        self.history_log_path = self.log_dir / "speed_history.csv"
        
        self._init_log_files()

    def _init_log_files(self):
        """
        Creates log files and writes headers if they don't exist.
        """
        if not self.events_log_path.exists():
            with open(self.events_log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "EventType", "VehicleSpeedKPH", "SpeedLimitKPH", "Zone", "Details"])

        if not self.history_log_path.exists():
            with open(self.history_log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "VehicleSpeedKPH", "SpeedLimitKPH", "Zone"])

    def log_event(self, event_type, speed, limit, zone, details=""):
        """
        Logs a specific event (e.g., overspeeding, regulation).
        :param event_type: A string describing the event (e.g., 'OVER_SPEED_WARNING').
        :param speed: Current vehicle speed in km/h.
        :param limit: Current speed limit in km/h.
        :param zone: The name of the current zone.
        :param details: Any additional details about the event.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.events_log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, event_type, f"{speed:.2f}", limit, zone, details])

    def log_speed_history(self, speed, limit, zone):
        """
        Logs a snapshot of the vehicle's current speed and context.
        :param speed: Current vehicle speed in km/h.
        :param limit: Current speed limit in km/h.
        :param zone: The name of the current zone.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.history_log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, f"{speed:.2f}", limit, zone])
