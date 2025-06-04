# MiniFab System Overview

## Overview

MiniFab is an intelligent multi-modal manufacturing system based on Klipper that transforms a single machine into three distinct tools: CNC mill, 3D printer, and pen plotter. The system uses automatic tool detection via CAN bus to dynamically configure the machine according to the connected tool.

## System Architecture

### Main Components

#### 1. Central Controller (Raspberry Pi)
- **Role**: System orchestration, user interface, configuration management
- **OS**: Raspberry Pi OS / MainsailOS
- **Services**: Klipper, Moonraker, Mainsail, MiniFab daemon

#### 2. Machine Controller (Octopus V1.1)
- **Role**: Control of main motors (X, Y, Z, B-axis), spindle, sensors
- **Communication**: CAN bus with toolheads, USB with Raspberry Pi
- **CAN UUID**: `007b91d4791b`

#### 3. Tool Heads (EBB42 v1.2)
Each head has its own CAN UUID for identification:
- **Mill**: `0fbff82fd51f` - Mill with spindle and sensors
- **Print**: `c64b129f89d0` - 3D extruder with heating and probe
- **Pellet**: `38a6930ee689` - Pellet extruder with heating  
- **PenPlt**: `unknow` - Plotter with pen mechanism

### Data Flow

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   User          │    │  Raspberry   │    │    Octopus      │
│   Interface     │◄──►│      Pi      │◄──►│     V1.1        │
│ (Web/Mainsail)  │    │   (Klipper)  │    │   (Motors)      │
└─────────────────┘    └──────┬───────┘    └─────────────────┘
                              │                       │
                              │                       │ CAN Bus
                              ▼                       ▼
                    ┌──────────────────┐    ┌─────────────────┐
                    │  MiniFab Daemon  │    │   Tool Heads    │
                    │  (autofirmware)  │    │   (EBB42 CAN)   │
                    └──────────────────┘    └─────────────────┘
```

## Automatic Detection System

### Operating Principle

1. **CAN Bus Scan**: The `autofirmware.py` daemon periodically queries the CAN bus
2. **UUID Identification**: Each toolhead responds with its unique UUID
3. **Configuration Mapping**: UUID is associated with a specific configuration
4. **Automatic Swap**: System switches to appropriate configuration
5. **Klipper Restart**: Restart to apply new configuration

### Mode Change Process

```python
# Automatic detection cycle
while True:
    if not forced:
        uuids = get_canbus_uuid()  # CAN bus scan
        for uuid in uuids:
            toolhead = find_folder_by_uuid(uuid)  # UUID->Config mapping
            if toolhead != current_toolhead:
                firmware_change(toolhead)  # Config change + restart
    time.sleep(5)
```

## Configuration Architecture

### Modular Structure

```
konect-v-minifab/
├── docs/                     # Project documentation
│   ├── architecture.md      # Technical architecture
│   ├── computer_setup_procedure.md  # Installation guide
│   ├── pins.md              # Pin reference
│   └── assets/img/          # Documentation images
├── src/
│   ├── config/              # Klipper configurations
│   │   ├── moonraker.conf   # API server configuration
│   │   ├── octoeverywhere.conf      # Remote access
│   │   ├── octoeverywhere-system.cfg # OctoEverywhere system
│   │   ├── common/          # Shared configurations
│   │   │   ├── main_printer.cfg    # Base machine configuration
│   │   │   ├── stepper.cfg         # Main motors (X,Y,Z,B)
│   │   │   ├── board_pins.cfg      # Octopus pin definitions
│   │   │   ├── macro.cfg           # Common macros
│   │   │   └── mainsail.cfg        # Mainsail interface
│   │   ├── b_axis/          # Rotation axis (4th axis)
│   │   │   ├── main.cfg
│   │   │   ├── stepper.cfg         # Rotation motor configuration
│   │   │   └── macro.cfg           # Extended G-code (G0/G1/G2/G3 with B)
│   │   └── toolheads/       # Tool-specific configurations
│   │       ├── idle/        # Idle mode (no tool)
│   │       │   ├── KlipperScreen.conf
│   │       │   ├── machine.cfg
│   │       │   └── printer.cfg
│   │       ├── mill/        # CNC Mill
│   │       │   ├── KlipperScreen.conf
│   │       │   ├── machine.cfg
│   │       │   ├── macro.cfg
│   │       │   ├── printer.cfg
│   │       │   └── spindle.cfg
│   │       ├── print/       # 3D Printer
│   │       │   ├── KlipperScreen.conf
│   │       │   ├── machine.cfg
│   │       │   ├── macro.cfg
│   │       │   ├── printer.cfg
│   │       │   └── probe.cfg
│   │       ├── pellet/      # Pellet Printer
│   │       │   ├── KlipperScreen.conf
│   │       │   ├── machine.cfg
│   │       │   ├── macro.cfg
│   │       │   ├── printer.cfg
│   │       │   └── probe.cfg
│   │       └── penplt/      # Pen Plotter
│   │           ├── KlipperScreen.conf
│   │           ├── machine.cfg
│   │           └── printer.cfg
│   ├── klipperscreen_theme/ # Custom KlipperScreen theme
│   │   ├── style.conf
│   │   ├── style.css
│   │   └── images/
│   ├── mainsail_theme/      # Custom Mainsail theme
│   │   └── custom.css
│   └── scripts/             # Python scripts
│       ├── autofirmware.py  # Automatic tool detection
│       ├── confswap.py      # Configuration management
│       ├── setup.py         # System installation
│       ├── startup.py       # Web daemon startup
│       ├── static/          # Web resources (SVG, CSS)
│       └── templates/       # HTML templates (Flask)
│           ├── index.html
│           └── logs.html
└── .github/                 # GitHub project management
    ├── CONTRIBUTING.md
    ├── ISSUE_TEMPLATE/
    ├── workflows/
    └── ...
```

### Symbolic Link System

The `confswap.py` script manages configuration switching:

```python
# Dynamic symbolic link creation
create_symlink(
    "/home/minifab/printer_data/config/toolheads/{mode}/printer.cfg",
    "/home/minifab/printer_data/config/printer.cfg"
)
```

## Operating Modes

### 1. CNC Mill Mode (`mill`)
- **Spindle control**: M3/M4 (rotation direction), M5 (stop)
- **Safety**: Emergency stop if door opened (sensor `PG11`)
- **Tool change**: Assisted M6 procedure with interactive pause
- **Vacuum**: Integrated vacuum socket control
- **Monitoring**: Spindle thermistor for temperature monitoring

### 2. 3D Print Mode (`print`)
- **Extruder**: Temperature control, extrusion, retraction
- **Heated bed**: Bed temperature management
- **Calibration**: Automatic probe for mesh bed leveling
- **Fans**: Hotend fan, part cooling, heatbreak
- **Safety**: Minimum extrusion temperature protection (180°C)

### 3. Pen Plotter Mode (`penplt`)
- **Pen mechanics**: Pen up/down control
- **Optimizations**: Movement parameters adapted for drawing
- **Safety**: Stop if pen sensor triggered
- **Interface**: Simplified UI for plotting operations

### 4. Pellet Mode (`pellet`)
- **Pellet extrusion**: Plastic pellet extrusion system
- **Temperature**: Nozzle and bed heating control
- **Calibration**: Probe system for bed calibration
- **Ventilation**: Hotend and heatbreak cooling management

## G-Code Extension

### B-Axis (Rotation)

The system extends standard G-Code commands to support rotation axis:

```gcode
G0 X100 Y50 Z10 B45    # Movement with 45° rotation
G1 X200 B90 F1000      # Linear movement with rotation
G2 X50 Y50 I25 J0 B180 # Arc with 180° rotation
```

**Implementation**: Macros intercept G0/G1/G2/G3 and add B-axis control

### Special Commands

- **M453 T[1-3]**: Manual mode forcing
  - T1: CNC Mill Mode
  - T2: 3D Printer Mode  
  - T3: Pen Plotter Mode
- **M6**: Assisted tool change (mill mode)
- **G92**: Extended origin redefinition for all axes

## Monitoring Interface

### Web Dashboard (Port 8000)

**Features**:
- Real-time system status visualization
- Current toolhead display and forced/auto status
- System logs with timestamps
- Manual mode forcing buttons
- Log download for diagnostics

**Technologies**: Flask, HTML/CSS/JavaScript
**Templates**: `src/scripts/templates/` (index.html, logs.html)
**Assets**: `src/scripts/static/` (SVG icons, CSS)

### Mainsail/Fluidd Integration

- **Port 80**: Main Klipper interface
- **Dynamic configuration**: KlipperScreen.conf adapted by mode
- **Custom theme**: 
  - Mainsail: `src/mainsail_theme/custom.css`
  - KlipperScreen: `src/klipperscreen_theme/` (style.conf, style.css, images/)
- **Status indicators**: Current mode display in interface

## Services and Daemons

### Service Configuration

**System configuration files**:
- **Moonraker**: `src/config/moonraker.conf` - Klipper API server
- **OctoEverywhere**: 
  - `src/config/octoeverywhere.conf` - Client configuration
  - `src/config/octoeverywhere-system.cfg` - System configuration
- **Mainsail**: `src/config/common/mainsail.cfg` - Web interface

### Automatic Startup

Crontab configuration for boot launch:
```bash
@reboot /usr/bin/python /home/minifab/MiniFab/src/scripts/startup.py
```

### Integrated Services

- **Klipper**: 3D controller firmware
- **Moonraker**: Klipper API server  
- **Mainsail**: Main web interface
- **Crowsnest**: Webcam management
- **OctoEverywhere**: Remote access
- **MiniFab Daemon**: Automatic toolhead management

## Safety and Monitoring

### Safety Sensors

- **Door open detection** (mill): Immediate spindle stop
- **Thermistors**: Critical temperature monitoring
- **Endstops**: All axes limit protection
- **CAN Heartbeat**: Toolhead disconnection detection

### Error Management

- **CAN Timeout**: Automatic return to idle mode if communication lost
- **Centralized logs**: Complete system event traceability
- **Automatic recovery**: Reconnection and reconfiguration attempts
- **Diagnostic interface**: Web dashboard for status monitoring

## Maintenance and Updates

### Configuration Update
```bash
python setup.py -c    # Update configs only
python setup.py -f    # Force complete setup
```

### Diagnostics
- Logs accessible via web interface
- Debug commands via SSH
- systemd service status monitoring
- Symbolic link integrity verification
