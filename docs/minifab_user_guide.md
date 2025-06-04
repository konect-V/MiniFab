# MiniFab User Guide

## Overview

MiniFab is a multi-modal manufacturing system that allows you to use a single machine for three different types of fabrication: CNC mill, 3D printer, and pen plotter. The system automatically detects the connected tool and configures the machine accordingly.

## Initial Setup

### Interface Access

After powering on the machine, you can access the following interfaces:

- **Main Mainsail Interface**: `http://[RASPBERRY_IP]:80`
- **MiniFab Dashboard**: `http://[RASPBERRY_IP]:8000`
- **KlipperScreen Interface**: Local touch screen (if installed)

> **💡 Tip**: Note your Raspberry Pi's IP address for easy access. It usually displays on the local screen at startup.

### System Verification

1. **Open the MiniFab Dashboard** (`http://[RASPBERRY_IP]:8000`)
2. **Check status**: A green checkmark indicates everything is working
3. **Verify detection**: The currently connected tool displays with its icon

## Changing Manufacturing Mode

### Automatic Change (Recommended)

The system automatically detects the connected tool:

1. **Power off the machine** or make it safe
2. **Disconnect** the current tool from the CAN connector
3. **Connect** the new tool
4. **Wait 5-10 seconds**: The system detects and automatically reconfigures
5. **Verify** in the MiniFab Dashboard that the correct tool is displayed

### Manual Change (Forced Mode)

If necessary, you can force a specific mode:

1. **Open the MiniFab Dashboard**
2. **Click the button** corresponding to the desired mode:
   - **Force : mill** - CNC Mill Mode
   - **Force : print** - 3D Printer Mode  
   - **Force : penplt** - Pen Plotter Mode
   - **Force : pellet** - Pellet Printer Mode
3. **Click "Auto"** to return to automatic mode

> ⚠️ **Warning**: In forced mode, the system will not verify if the correct tool is connected.

## CNC Mill Mode

### Preparation

1. **Check safety**:
   - Protection door closed
   - Vacuum connected and functional
   - Cutting tool properly mounted

2. **Connect the mill head**:
   - System displays "mill" in Dashboard
   - Mainsail interface shows spindle controls

### Basic Operations

#### Spindle Startup
```gcode
M3 S12000    # Start clockwise at 12000 RPM
M4 S8000     # Start counter-clockwise at 8000 RPM
M5           # Stop spindle
```

#### Tool Change (M6)
1. **Execute** `M6` in the Mainsail terminal
2. **Follow instructions**: Machine positions automatically
3. **Change tool** manually when prompted
4. **Confirm** in the dialog box
5. **Wait** for automatic resume with Z rehoming

#### Vacuum Control
```gcode
START_VACUUM_CLEANER    # Start vacuum
STOP_VACUUM_CLEANER     # Stop vacuum
```

### Specific Safety Features

- **Emergency stop**: Opening the door immediately stops the spindle
- **Temperature monitoring**: Spindle has control thermistor
- **Deceleration ramp**: Spindle slows progressively when stopping

## 3D Printer Mode

### Preparation

1. **Connect the print head**:
   - System automatically detects extruder
   - Interface displays temperature controls

2. **Initial heating**:
   - **Bed**: 60°C for PLA, 80°C for PETG
   - **Extruder**: 200°C for PLA, 230°C for PETG

### Bed Calibration

#### Automatic Calibration
```gcode
G28          # Home all axes
G29          # Automatic bed mesh
```

The system uses a servo-deployable probe for automatic calibration.

#### Manual Calibration
```gcode
G28          # Home
G0 Z10       # Safety height
ORIGIN       # Set current origin
```

### Filament Management

#### Loading
1. **Heat the extruder** (185°C minimum)
2. **Insert filament** into extruder
3. **Manually extrude** to purge old material

#### Unloading
1. **Heat the extruder**
2. **Retract** filament via Mainsail interface
3. **Physically remove** filament

### Printing

1. **Prepare G-code file** with correct parameters
2. **Upload** via Mainsail interface
3. **Verify** target temperatures
4. **Start printing**

## Pen Plotter Mode

### Preparation

1. **Connect the plotter head**:
   - System switches to "penplt" mode
   - Simplified interface for drawing

2. **Install pen**:
   - Secure pen in mechanism
   - Adjust contact height

### Plotting

#### Drawing Preparation
```gcode
G28          # Home
G0 X0 Y0     # Origin position
```

#### Special Commands
- **Lift pen**: Positive Z movement
- **Lower pen**: Negative Z movement
- **Rapid moves**: G0 with pen lifted
- **Drawing**: G1 with pen in contact

### Optimizations

- **Reduced speed**: Movements adapted for line quality
- **Smooth acceleration**: Avoid jerks that degrade drawing

## Pellet Mode

### Preparation

1. **Connect the pellet head**:
   - System similar to 3D printing
   - Extruder adapted for pellets

2. **Loading pellets**:
   - Fill pellet reservoir
   - Heat extruder (temperature per material)

### Extrusion

- **Nozzle diameter**: 0.8mm (larger than standard print)
- **Temperatures**: Generally higher than filament
- **Flow rate**: Adjusted for pellet density

## Using B-Axis (Rotation)

All modes support the rotation B-axis for 4-axis operations:

```gcode
G0 X100 Y50 B45      # Position with 45° rotation
G1 X200 B90 F1000    # Movement with progressive rotation
G2 X50 Y50 I25 J0 B180  # Arc with 180° rotation
```

### Applications
- **Mill**: Machining cylindrical parts
- **Print**: Printing on curved forms
- **Plotter**: Drawing on cylindrical objects

## User Maintenance

### Daily Checks

1. **Check Dashboard**: No errors displayed
2. **Test endstops**: Manual press and release
3. **Verify temperatures**: Consistent values when cold
4. **Check connections**: CAN bus properly secured

### Cleaning

#### Mill Head
- **Chip extraction** after each use
- **Spindle cleaning**: Compressed air blow-out
- **Tool verification**: Cutting edge condition

#### Print Head
- **Nozzle cleaning**: Hot purge between materials
- **Bed**: Isopropyl alcohol cleaning
- **Extruder**: Check for jams

#### General
- **Rails**: Light lubrication if needed
- **Connectors**: Contact cleanliness verification
- **Wiring**: Visual wear inspection

## Troubleshooting

### Detection Problems

**Symptom**: Connected tool not detected
**Solutions**:
1. Check CAN bus connection
2. Restart the machine
3. Check logs via MiniFab Dashboard
4. Temporarily force correct mode

### Communication Errors

**Symptom**: "Printer not ready" or CAN errors
**Solutions**:
1. Check 24V power supply
2. Verify CAN cable integrity
3. Restart Klipper via Mainsail
4. Check system logs

### Temperature Problems

**Symptom**: Erratic temperatures or not reaching target
**Solutions**:
1. Check thermistor connections
2. Verify heating cartridge condition
3. Check ventilation
4. Review PID curves

### Web Interface Inaccessible

**Solutions**:
1. Check network connection
2. Restart services: `sudo systemctl restart klipper moonraker`
3. Restart Raspberry Pi
4. Check IP address (may have changed)

## Emergency Procedures

### Emergency Stop
- **M112**: Immediate stop via G-code
- **Emergency Stop**: Mainsail interface button
- **Power cut**: As last resort

### Recovery After Emergency Stop
1. **Identify cause** of stop
2. **Secure work area**
3. **Restart Klipper** via interface
4. **Complete homing** before resuming
5. **Function tests** before use

## Support and Assistance

### Available Documentation

In the project's `docs/` folder:
- **`architecture.md`**: Detailed technical architecture
- **`computer_setup_procedure.md`**: Complete installation guide
- **`pins.md`**: Complete connection reference
- **`assets/img/`**: Images and diagrams

### Logs and Diagnostics
- **MiniFab Dashboard**: System status overview
- **Detailed logs**: Downloadable from web interface
- **Klipper logs**: Via Mainsail interface

### Support Contact
- **Email**: fablab@devinci.fr
- **Documentation**: Project GitHub repository
- **Logs**: Always attach when requesting assistance

### System Update
```bash
cd MiniFab/src/scripts
python setup.py    # Configuration update
```

> **Note**: Major updates require qualified technical intervention.
