# Logic Flowchart

This flowchart details the step-by-step logic the system follows during each update cycle to detect and handle overspeeding conditions.

## Overspeed Detection and Regulation Flowchart (Mermaid)

```mermaid
graph TD
    A[Start Frame] --> B{Get Vehicle State};
    B --> C{Get Current Zone & Speed Limit};
    
    C --> D{Is vehicle_speed > speed_limit?};
    D -- No --> E[Set Status: SAFE];
    E --> Z[End Frame];
    
    D -- Yes --> F{Is vehicle in Speed Camera Zone?};
    F -- Yes --> G[Trigger INSTANT Regulation];
    G --> H[Set Status: OVER_SPEED];
    H --> I[Enforce Speed Limit on Vehicle];
    I --> Z;

    F -- No --> J{Start/Continue Overspeed Timer};
    J --> K{Has timer exceeded limit (e.g., 3s)?};
    K -- No --> L[Set Status: OVER_SPEED];
    L --> M[Display Flashing Warning];
    M --> Z;
    
    K -- Yes --> N[Trigger TIMED Regulation];
    N --> O[Set Status: OVER_SPEED];
    O --> P[Display Regulation Notification];
    P --> Q[Enforce Speed Limit on Vehicle];
    Q --> Z;

```

### Explanation of the Flow

1.  **Get State**: At the beginning of each frame, the system gets the vehicle's current speed and its position on the map.
2.  **Get Zone**: Using the vehicle's position, it determines which zone it's in and fetches the corresponding speed limit.
3.  **Check Speed**: It compares the vehicle's speed to the zone's speed limit.
    - If the speed is within the limit, the status is set to `SAFE`, and the loop for this check ends.
4.  **Overspeeding Detected**: If the speed is over the limit:
    - **Speed Camera Check**: The system first checks if the vehicle is in a specially-marked speed camera zone. If so, regulation is triggered *immediately*.
    - **Normal Overspeeding**: If not in a camera zone, the system starts a timer.
    - **Warning Stage**: As long as the timer has not exceeded the pre-defined limit (e.g., 3 seconds), the system sets the status to `OVER_SPEED` and displays a flashing warning on the UI.
    - **Regulation Stage**: If the timer exceeds the limit, the system activates automatic regulation, enforcing the speed limit on the vehicle and updating the UI with a notification.
5.  **Enforce Limit**: When regulation is active (either from a camera or the timer), the vehicle's maximum possible speed is programmatically lowered to match the zone's speed limit.
