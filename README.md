# EBEAM System Dashboard Software

## Detailed Design Document

### 1. Architecture

- **Language & Libraries**: Python, using Tkinter for the GUI, Matplotlib for plotting, and PySerial for serial communication.
- **High-level Design**: The application is divided into several modules:
  - **main.py**: Manages the main application startup and configuration.
  - **dashboard.py**: Handles the main user interface and dashboard setup.
  - **subsystem.py**: Contains classes and methods to manage individual subsystems (e.g., VTRXSubsystem, EnvironmentalSubsystem).
  - **instrumentctl.py**: Instrument specific command libraries.
  - **utils.py**: Utility functions and classes that support the main application (Logging, data parsing, etc.).

### 2. Components

- **Main Application (main.py)**:
  - **Configuration Loader**: Responsible for initial configurations, setting up COM ports, and starting the main dashboard.
  - **COM Port Configuration**: Dynamically detects and assigns COM ports for various hardware interfaces. TODO: Write dropdowns for additional subsystems.

- **Instrument Control (instrumentctl.py)**:
  - **Equipment specific driver libraries**:
    - Agilent 33120A
    - Quantum 9530
    - G9SP serial option (status door, e-stops, vac, levels, timer)
    - VTRX system
    - Temp monitor
    - A655sc
    - BOP-100-2ML

### 3. Dashboard (dashboard.py)

- **EBEAMSystemDashboard Class**: The main class that sets up the dashboard interface.
  - **setup_main_pane**: Initializes the main layout pane and its rows.
  - **create_frames**: Creates frames for different systems and controls within the dashboard.
  - **create_messages_frame**: Creates a frame for displaying messages and errors.
  - **create_subsystems**: Initializes subsystems in their designated frames using component settings.

### 4. Subsystems (subsystem.py)

- **VTRXSubsystem Class**:
  - Manages the VTRX system, including serial communication and GUI updates.
  - Handles pressure data and switch states, updating the GUI in real-time.
  - Logs messages and errors to the messages frame.

- **EnvironmentalSubsystem Class**:
  - Monitors and displays temperature data from various thermometers.
  - Uses Matplotlib to create bar charts for temperature visualization.

- **ArgonBleedControlSubsystem Class**:
  - Controls the Argon bleed system via serial communication.
  - Provides GUI buttons for taring flow and absolute pressure.

- **InterlocksSubsystem Class**:
  - Manages the status of various interlocks (e.g., Vacuum, Water, Door).
  - Updates GUI indicators based on interlock status.

- **OilSystem Class**:
  - Monitors and displays oil temperature and pressure.
  - Uses a vertical temperature gauge and a dial meter for pressure visualization.

### 5. Utilities (utils.py)

- **ApexMassFlowController Class**:
  - Manages the serial communication with the Apex Mass Flow Controller.
  - Provides methods for configuring unit ID, taring flow, and taring absolute pressure.

- **MessagesFrame Class**:
  - A custom Tkinter frame for displaying messages and errors.
  - Supports logging messages with timestamps and trimming old messages to maintain a maximum number of lines.

- **TextRedirector Class**:
  - Redirects stdout to a Tkinter Text widget.
  - Ensures that all print statements in the application are displayed in the messages frame.

- **SetupScripts Class**:
  - Manages the selection and execution of configuration scripts.
  - Provides a GUI for selecting scripts from a dropdown menu and executing them.

![Application architecture](https://github.com/mslaffin/EBEAM_dashboard/blob/main/media/Topology.png)