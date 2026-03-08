# Smart Speed Control System

## Overview
This project simulates an **Intelligent Speed Adaptation (ISA)** system. It demonstrates how a smart vehicle can automatically detect speed limits based on its location and slow down to ensure safety, using **IoT technology** to report data in real-time.

## How It Works (The Logic)
The system operates on a continuous loop of **See, Think, and Act**:

1.  **See (GPS & Sensors)**
    *   The system tracks the car's **(x, y) position** on the map.
    *   It identifies which **Zone** the car is in (e.g., School Zone, Highway).
2.  **Think (Control Logic)**
    *   It compares **Current Speed** vs. **Speed Limit**.
    *   *Logic*: `If Speed > Limit`, start a timer.
3.  **Act (Intervention)**
    *   **Warning Phase (0-3s)**: Flashes red warnings and beeps to alert the driver.
    *   **Regulation Phase (>3s)**: If warnings are ignored, the system **automatically limits the engine power**, forcing the car to slow down to the limit.

## Project Structure
Here is a simple breakdown of the code modules:

| File | Description |
| :--- | :--- |
| `main.py` | **The Manager**. Runs the game loop, handles inputs, and updates the screen. |
| `vehicle.py` | **The Car**. Handles physics (acceleration, friction, steering) and speed limiting. |
| `world.py` | **The Map**. Defines roads, zones, and speed limits. |
| `speed_controller.py` | **The Brain**. Decides if the car is safe, warning, or needs regulation. |
| `ui.py` | **The Display**. Draws the dashboard, speedometer, and minimap. |
| `mqtt_client.py` | **The IoT Link**. Sends live vehicle data to the cloud (HiveMQ). |
| `datalogger.py` | **The Recorder**. Saves trip history to CSV files for analysis. |

## Key Features
*   **Real Physics**: Acceleration, braking, and drifting mechanics using vector math.
*   **Zone Detection**: Automatically detects 4 types of zones (Highway, City, School, Village).
*   **Smart Braking**: Smoothly slows the car down if the driver ignores warnings.
*   **IoT Connectivity**: Publishes live telemetry (Speed, Location, Status) to an MQTT broker.
*   **Data Logging**: Saves all trip details locally.

## Controls
*   **Arrow Keys**: Drive (Accelerate, Brake, Turn).
*   **O**: Toggle **Override Mode** (Emergency bypass of speed limiter).
*   **R**: Reset car position.
*   **F**: Toggle Fullscreen.

## How to Run
1.  **Install Dependencies**:
    ```bash
    pip install pygame paho-mqtt
    ```
2.  **Run the Simulation**:
    ```bash
    python main.py
    ```
3.  **Follow On-Screen Prompts**: Enter driver name and destination to start.

---
*Built with Python, Pygame, and Paho-MQTT.*
