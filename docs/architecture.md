# MiniFab Architecture Documentation

## Overview

This document describes the proposed architecture for the MiniFab project, a multi-function machine that supports milling, 3D printing, and pen plotting through a toolhead-swapping system.

## Directory Structure

```
minifab/                         # Project root directory
│
├── src/                        # Main source code
│   ├── config/                 # Configuration files
│   │   ├── main_printer.cfg    # Main configuration containing: machine size, steppers, etc.
│   │   │
│   │   ├── system/             # System services configuration
│   │   │   ├── moonraker.conf      # Moonraker API server configuration
│   │   │   ├── crowsnest.conf      # Webcam configuration
│   │   │   ├── sonar.conf          # WiFi keepalive configuration
│   │   │   ├── timelapse.cfg       # Timelapse configuration
│   │   │   ├── mainsail.cfg        # Mainsail interface configuration
│   │   │   ├── octoeverywhere.conf # OctoEverywhere configuration
│   │   │   ├── octoeverywhere-system.cfg # OctoEverywhere system configuration
│   │   │   └── print_area_bed_mesh.cfg # Print area bed mesh configuration
│   │   │
│   │   ├── common/             # Configurations common to all modes
│   │   │   ├── board_pins.cfg  # Pins configuration
│   │   │   ├── change.cfg      # Tool change mechanism configuration
│   │   │   ├── stepper.cfg     # Common stepper motor configuration
│   │   │   ├── spindle.cfg     # Spindle configuration
│   │   │   │
│   │   │   └── b_axis/         # B-axis configuration
│   │   │       ├── main.cfg    # Main B-axis configuration
│   │   │       ├── macro.cfg   # B-axis macros
│   │   │       └── stepper.cfg # B-axis stepper configuration
│   │   │
│   │   └── toolhead/           # Toolhead configurations
│   │       ├── mill/           # Mill toolhead specific configuration
│   │       │   ├── machine.cfg     # Mill-specific parameters
│   │       │   ├── macros.cfg      # G-code macros for milling
│   │       │   └── KlipperScreen.conf # KlipperScreen configuration for mill mode
│   │       │
│   │       ├── print/          # Print toolhead specific configuration
│   │       │   ├── machine.cfg     # Printer-specific parameters
│   │       │   ├── fan.cfg         # Fan configuration
│   │       │   ├── probe.cfg       # Probe configuration
│   │       │   ├── macros.cfg      # G-code macros for printing
│   │       │   └── KlipperScreen.conf # KlipperScreen configuration for print mode
│   │       │
│   │       ├── penplt/         # Pen plotter toolhead specific configuration
│   │       │   ├── machine.cfg     # Plotter-specific parameters
│   │       │   ├── macros.cfg      # G-code macros for plotting
│   │       │   └── KlipperScreen.conf # KlipperScreen configuration for plotter mode
│   │       │
│   │       └── idle/          # Idle mode
│   │           ├── machine.cfg     # Idle mode specific parameters
│   │           ├── printer.cfg     # Idle mode printer configuration
│   │           └── KlipperScreen.conf # KlipperScreen configuration for idle mode
│   │
│   └── scripts/                # Scripts
│       ├── autofirmware.py     # Toolhead detection and management
│       ├── confswap.py         # Configuration management
│       ├── setup.py            # Installation and initial setup
│       ├── startup.py          # Web server and daemon startup
│       │
│       ├── static/             # Static files for web interface
│       │   ├── mill.svg
│       │   ├── print.svg
│       │   └── ...
│       │
│       └── templates/          # Web interface templates
│           ├── index.html
│           └── logs.html
│
└── docs/                       # Documentation
    └── ...
```

## Main Components

### Configuration Structure

The configuration system is organized into three main categories:

1. **Root Configuration**
   - `main_printer.cfg`: Contains the base machine configuration including dimensions, steppers, and other shared settings.

2. **System Configuration**
   - Contains configurations for services and utilities that support the operation of the machine.
   - Includes web interfaces, camera systems, remote access, and other supporting services.

3. **Common Configuration**
   - Contains configurations that are shared across multiple toolheads.
   - Includes pin definitions, stepper configurations, spindle control, and the B-axis rotation system.

4. **Toolhead Configuration**
   - Contains specific configurations for each mode of operation (mill, print, pen plotter, idle).
   - Each toolhead includes its own specialized machine configuration, macros, and UI settings.

### Scripts

The `scripts` directory contains the Python scripts that manage the operation of the MiniFab system:

- `autofirmware.py`: Handles automatic detection of connected toolheads and firmware switching.
- `confswap.py`: Manages the swapping between different configuration files.
- `setup.py`: Handles initial installation and setup of the system.
- `startup.py`: Controls the web interface and daemon startup process.

## Implementation Considerations

### Configuration Symlinks

The system uses symbolic links to swap between different configurations. When a toolhead is changed, the appropriate configuration files are linked from the toolhead directory to the Klipper configuration directory.

### Toolhead Detection

Toolheads are detected via CAN bus UUIDs. The `autofirmware.py` script monitors the CAN bus and identifies connected toolheads based on their unique identifiers.

### Web Interface

The MiniFab includes a web interface for monitoring and control, with status pages, logs, and toolhead management.

## Notes

- The "idle" mode is included in the toolhead directory for consistency, even though it represents a state rather than a physical toolhead.
- The B-axis configuration is considered common as it may be used by multiple toolheads.
- System services configurations are grouped separately as they are independent of the specific toolhead in use.