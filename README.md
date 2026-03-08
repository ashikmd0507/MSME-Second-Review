# Smart Speed Control and Warning System Simulation

## 1. Project Objective

This project is a fully functional, interactive simulation of an IoT-based intelligent vehicle speed monitoring and control system. It dynamically regulates a vehicle's speed based on its geographical location (simulated as zones on a map) and the corresponding speed limit. The primary goal is to demonstrate a system that can warn a driver about overspeeding and, if necessary, automatically intervene to enforce the speed limit.

## 2. How The System Works

The simulation places you in control of a visually distinct car on a 2D map designed to look like a road network. The world is divided into several zones, each clearly labeled with its name and speed limit.

- **GPS Simulation**: The system continuously tracks your vehicle's (x, y) position on the map to determine which speed zone it is in.
- **Speed Monitoring**: Your vehicle's real-time speed is constantly monitored. The physics have been tuned for a more controllable driving experience.
- **Warning Stage**: If you exceed the speed limit of your current zone, the system will issue a visual (flashing on-screen banner) and audible (beep) warning. The dashboard speed indicator will also turn red.
- **Automatic Regulation Stage**: If you ignore the warnings and continue to overspeed for more than 3 seconds, the system automatically activates its speed regulation protocol. It smoothly reduces your vehicle's maximum speed to the zone's limit, preventing you from accelerating further.
- **IoT Simulation**: All vehicle data location, speed, zone, and system status is serialized into a JSON format and published to a public MQTT broker every second, simulating how a real-world IoT device would transmit telemetry data.

## 3. Core Features

### Simulation & Gameplay
- **Interactive Vehicle**: Control a custom-drawn, top-down car sprite with `W` (Accelerate), `S` (Brake), `A` (Turn Left), and `D` (Turn Right).
- **Virtual Map**: Drive on a map with a clear road network, grass background, and labeled zones: Highway (80 km/h), City Road (50 km/h), School Zone (30 km/h), and Village Area (40 km/h).
- **Game-like UI**: A clean, colorful interface with a dashboard HUD that flashes red when overspeeding. It displays your speed, the current zone's name and speed limit, and system status. A permanent on-screen guide reminds you of the controls.

### Smart System
- **Dynamic Speed Limit Detection**: The system instantly recognizes the speed limit of the zone the vehicle enters.
- **Multi-stage Warnings**: The UI provides color-coded feedback:
    - **Green**: Safe speed.
    - **Yellow**: Approaching the speed limit.
    - **Red**: Overspeeding.
- **Automatic Speed Reduction**: Enforces the speed limit after a configurable delay.

### Additional Features
- **Speed Camera Zones**: Two marked zones where overspeeding triggers immediate warnings and speed regulation.
- **Data Logging**: The system logs all significant events (overspeeding, regulation) and a periodic history of the vehicle's speed into `.csv` files in the `data_logs/` directory.
- **Emergency Override**: Press the `O` key to toggle an override mode that disables automatic speed regulation. The UI clearly indicates when this mode is active.
- **MQTT Data Transmission**: Simulates real-world IoT architecture by publishing vehicle telemetry to the `vehicle/telemetry` topic on a public broker.

## 4. Technologies Used

- **Simulation & UI**: Python 3 and the `Pygame` library.
- **IoT Communication**: `paho-mqtt` library for MQTT protocol simulation.
- **GPS Simulation**: Vehicle's (x, y) coordinates on the Pygame screen are used to simulate GPS data.

## 5. Installation

1.  **Clone the repository or download the source code.**
2.  **Ensure you have Python 3 installed.**
3.  **Install the required libraries** by running the following command in your terminal in the project directory:
    ```bash
    pip install -r requirements.txt
    ```

## 6. How to Run the Simulation

1.  **Navigate to the project directory** in your terminal.
2.  **Run the main script**:
    ```bash
    python main.py
    ```
3.  A Pygame window will open, and the simulation will start.

### Controls
- **Up Arrow**: Accelerate
- **Down Arrow**: Brake/Reverse
- **Left Arrow**: Turn Left
- **Right Arrow**: Turn Right
- **O**: Toggle Emergency Override Mode
- **Close Window**: Quit the simulation.

## 7. MQTT and Data Logs

- **MQTT Broker**: The simulation publishes to the public broker `broker.hivemq.com` on port `1883`.
- **Topic**: All data is published to the topic `vehicle/telemetry`. You can use an MQTT client like MQTTX or MQTT Explorer to subscribe to this topic and see the live JSON data.
- **Data Logs**: All event and speed history logs are saved in the `data_logs/` folder. You can open these `.csv` files with any spreadsheet program to review the session's data.
