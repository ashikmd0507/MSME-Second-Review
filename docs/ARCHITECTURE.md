# System Architecture

The system is designed as a monolithic simulation application but simulates a distributed IoT architecture. The core components interact as follows:

- **Vehicle Simulation (Pygame)**: Represents the physical car. It has properties like position, speed, and angle and is controlled by the user. It acts as the primary data source.
- **GPS (Simulated)**: The vehicle's (x, y) coordinates on the 2D map are used as a stand-in for real-world GPS coordinates.
- **Speed Controller**: This is the "brain" of the system. It takes data from the vehicle and the map, applies the speed limit rules, and decides when to issue warnings or enforce regulation.
- **MQTT Client**: This component is responsible for packaging the vehicle's telemetry data into a JSON payload and publishing it over the MQTT protocol. This simulates the action of an onboard IoT device sending data to the cloud.
- **MQTT Broker**: An external, public broker (`broker.hivemq.com`) that receives the data. In a real-world scenario, a dedicated cloud service (like AWS IoT Core or Azure IoT Hub) would be used.
- **Dashboard / UI**: The Pygame interface that subscribes to all the internal state changes and visualizes the data for the user, showing speed, warnings, and system status.

## Architecture Diagram (Mermaid)

```mermaid
graph TD
    subgraph Vehicle Simulation
        A[User Input (W,A,S,D)] --> B{Vehicle Physics};
        B --> C[Vehicle State (Speed, Position)];
    end

    subgraph Map & Rules
        D[World Zones (Speed Limits)];
    end

    subgraph Control & Logic
        E[Speed Controller];
    end

    subgraph IoT & Data
        F[MQTT Client];
        G((MQTT Broker));
        H[Data Logger];
    end
    
    subgraph User Interface
        I[Dashboard (HUD)];
    end

    C -- Position --> D;
    C -- Speed --> E;
    D -- Current Speed Limit --> E;
    
    E -- Regulation Action --> B;
    E -- Status (Warning, Regulation) --> I;
    E -- Events --> H;

    C -- Telemetry Data --> F;
    F -- Publishes --> G;
    
    C -- Speed & Position --> I;
    D -- Zone Name & Limit --> I;
```
