# Smart Speed Control System 

## 1. Project Overview
This project implements a simulation of an **Intelligent Speed Adaptation (ISA)** system using Python. It models a vehicle navigating a geofenced environment where speed limits are dynamically enforced based on spatial location. The system integrates **IoT telemetry** via MQTT to broadcast real-time vehicle state, simulating a connected vehicle architecture.

## 2. Technical Architecture

The application is built upon a real-time simulation loop operating at 60 Hz.

| Subsystem | Component | Functionality |
| :--- | :--- | :--- |
| **Physics Engine**<br>(`vehicle.py`) | Kinematics | Implements 2D vector physics (`pygame.Vector2`) for position, velocity, and acceleration. |
| | Dynamics | Simulates friction, braking force, and angular velocity for steering. |
| | Control | Decouples input handling from frame rate using delta-time (`dt`) calculations. |
| **Geofencing**<br>(`world.py`) | Zone Detection | Uses Axis-Aligned Bounding Box (AABB) collision detection for real-time zone tracking. |
| | Mapping | Maps the world into `Zone` objects with metadata (Speed Limit, Name, Color). |
| **Control Logic**<br>(`speed_controller.py`) | State Machine | Manages vehicle status (`SAFE`, `WARNING`, `OVER_SPEED`) via FSM. |
| | Hysteresis | Uses warning buffers and time thresholds (0-3s) to prevent state flickering. |
| | Intervention | Directly modifies `max_speed` to enforce limits during regulation. |
| **IoT Telemetry**<br>(`mqtt_client.py`) | Async Comm | Runs MQTT client on a daemon thread to avoid blocking the simulation loop. |
| | Protocol | Uses MQTT v3.1.1 (TCP) to publish JSON telemetry to `broker.hivemq.com`. |

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
| **1. Dependencies** | Install required libraries | `pip install pygame paho-mqtt numpy` |
| **2. Launch** | Run the simulation | `python main.py` |

---
*Tech Stack: Python 3, Pygame (SDL Wrapper), Paho-MQTT, NumPy.*
