# Smart Speed Control and Warning System in Vehicles using GPS-based dynamic speed regulation 

## 1. Project Overview
This project implements a simulation of an **Intelligent Speed Adaptation (ISA)** system using Python. It models a vehicle navigating a geofenced environment where speed limits are dynamically enforced based on spatial location. The system integrates IoT telemetry via MQTT to broadcast real-time vehicle state, simulating a connected vehicle architecture.

## 2. Technical Architecture

The application is built upon a real-time simulation loop operating at 60 Hz.

| Subsystem | Core Functionality |
| :--- | :--- |
| **Physics Engine**<br>(`vehicle.py`) | **Kinematics**: 2D vector physics (`pygame.Vector2`) for movement.<br>**Dynamics**: Simulates friction, braking, and steering.<br>**Control**: Decoupled input handling via delta-time (`dt`). |
| **Geofencing**<br>(`world.py`) | **Zone Detection**: Real-time AABB collision detection.<br>**Mapping**: Manages `Zone` objects with metadata (Limit, Name). |
| **Control Logic**<br>(`speed_controller.py`) | **State Machine**: Manages vehicle status (`SAFE`, `WARNING`, `OVER_SPEED`).<br>**Hysteresis**: Uses time thresholds (0-3s) to prevent flickering.<br>**Intervention**: Enforces speed limits during regulation. |
| **IoT Telemetry**<br>(`mqtt_client.py`) | **Async Comm**: Runs on a daemon thread to avoid blocking.<br>**Protocol**: Publishes JSON telemetry via MQTT v3.1.1. |

## 3. Module Breakdown

| File | Description |
| :--- | :--- |
| `main.py` | **Entry Point & Orchestrator**. Manages the main event loop, delta-time calculation, and subsystem coordination. |
| `vehicle.py` | **Physics Model**. Handles vector math for movement, rotation matrices for steering, and speed clamping. |
| `world.py` | **Spatial Manager**. Defines the coordinate system and manages the list of `Zone` entities. |
| `speed_controller.py` | **Logic Core**. Pure logic class implementing the ISA rules and timing mechanisms. |
| `ui.py` | **Renderer**. Handles blitting of HUD elements, text rendering, and coordinate transformation for the minimap. |
| `mqtt_client.py` | **Network Interface**. Wraps the `paho-mqtt` library for threaded publish/subscribe operations. |
| `datalogger.py` | **Persistence Layer**. Writes structured CSV data for post-simulation analysis. |

## 4. Key Features

| Feature | Description |
| :--- | :--- |
| **Vector-Based Movement** | Realistic acceleration and drift mechanics. |
| **Dynamic Speed Limiting** | Real-time modification of vehicle constraints based on geospatial data. |
| **Event-Driven Logging** | Captures state transitions (e.g., Regulation Activation) with timestamps. |
| **Remote Monitoring** | Live data stream via MQTT topic `vehicle/telemetry`. |

## 5. Controls & Configuration

| Category | Details |
| :--- | :--- |
| **Input Controls** | Arrow Keys (Movement), `O` (Override), `R` (Reset), `F` (Fullscreen). |
| **Configuration** | Constants for physics, network, and display centralized in `config.py`. |

## 6. Execution

| Step | Action | Command |
| :--- | :--- | :--- |
| **1. Dependencies** | Install required libraries | `pip install pygame paho-mqtt numpy geopy` or `pip install -r requirements.txt` |
| **2. Launch** | Run the simulation | `python main.py` |

---
*Tech Stack: Python 3, Pygame (SDL Wrapper), Paho-MQTT, NumPy.*
