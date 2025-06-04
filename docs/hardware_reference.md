# MiniFab Hardware Reference

## System Specifications

### Main Controller
- **Model**: Raspberry Pi 4 (recommended)
- **RAM**: 4GB minimum
- **Storage**: 16GB microSD card minimum (32GB recommended)
- **OS**: Raspberry Pi OS Lite / MainsailOS
- **Connectivity**: Ethernet/WiFi, USB 2.0/3.0

### Machine Controller
- **Model**: BigTreeTech Octopus V1.1
- **Microcontroller**: STM32F446ZET6
- **Drivers**: TMC2209 (integrated) - 6 drivers total
- **CAN UUID**: `007b91d4791b`
- **Interface**: CAN bus 500kbps, USB to Raspberry Pi
- **Power**: 24V input, provides power to CAN bus and tool heads

### Tool Heads

#### Tool Head UUID Mapping
- **Mill**: `0fbff82fd51f` (EBBCanMILL)
- **Print**: `c64b129f89d0` (EBBCanPRINT)
- **Pellet**: `38a6930ee689` (EBBCanPELLET)
- **PenPlt**: `none` (EBBCanPENPLT)

#### Common Tool Head Features
All EBB42 v1.2 boards include:
- **ADXL345**: Accelerometer for input shaping (SPI: PB12,PB10,PB11,PB2)
- **CAN Communication**: 500kbps bus with unique UUID identification
- **24V Power**: Via CAN connector

## Pin Mapping - Octopus V1.1

### Configuration Files

### Configuration Files

### Configuration Files

**Base Path**: `src/config/`

**Common configurations**:
- **`common/board_pins.cfg`**: Pin definitions (spindle PD12, vacuum PA2, LEDs PE5/PB0)
- **`common/stepper.cfg`**: Main motor configuration (X, Y, Y1, Z, Z1 axes)
- **`common/main_printer.cfg`**: Base machine configuration and includes

**B-Axis**: `b_axis/stepper.cfg` (rotation axis: 54:1 gear ratio, 360mm rotation_distance)

**Tool-specific configurations**: `toolheads/{toolhead}/`
- **`machine.cfg`**: Tool-specific pins, sensors, and extruder config
- **`probe.cfg`**: Probe configuration (print/pellet modes only)
- **`spindle.cfg`**: Spindle control and safety configuration (mill mode only)
- **`macro.cfg`**: Tool-specific G-code macros

### Main Motors

| Motor | Step Pin | Dir Pin | Enable Pin | Endstop | Notes |
|--------|----------|---------|------------|---------|-------|
| X (Driver 0) | PF13 | PF12 | !PF14 | !PG10 (DIAG2) | Main X axis |
| Y (Driver 1) | PG0 | PG1 | !PF15 | !PG9 (DIAG1) | Main Y axis |
| Y1 (Driver 2) | PF11 | PG3 | !PG5 | - | Secondary Y axis |
| Z (Driver 3) | PG4 | PC1 | !PA0 | !PG6 (DIAG0) | Main Z axis |
| Z1 (Driver 4) | PF9 | PF10 | !PG2 | - | Secondary Z axis |
| B (Driver 5) | PC13 | !PF0 | !PF1 | - | Rotation axis |

**Motor Specifications**:
- **Microstepping**: 16 microsteps
- **Rotation distance**: 
  - X,Y: 5mm (ball screws)
  - Y1: 4mm (ball screws)  
  - Z,Z1: 4mm (ball screws)
  - B: 360mm with 54:1 gear ratio (1mm = 1°)

### Spindle Control and Actuators

| Function | Pin | Type | Notes |
|----------|-----|------|-------|
| Spindle speed | PD12 (FAN2) | PWM | Hardware PWM, 0.01s cycle |
| Forward direction | PD13 (FAN3) | Digital | Clockwise rotation |
| Reverse direction | PD14 (FAN4) | Digital | Counter-clockwise rotation |
| Vacuum socket | PA2 (HE0) | Digital | Vacuum cleaner control |
| Electric box LED | PE5 (FAN1) | PWM | Electrical box lighting |
| Door detection | PG11 (DIAG3) | Input | Mill safety |

**Spindle Configuration**:
- **Max speed**: 24000 RPM
- **Control**: 0-24000 RPM via PWM 0-1.0 (PD12/FAN2)
- **Safety**: Immediate stop if door opened (PG11/DIAG3 in spindle.cfg)
- **Deceleration ramp**: 100 steps over 10 seconds

### Lighting and Signaling

| Function | Pin | Type | Specifications |
|----------|-----|------|----------------|
| Electric box LED | PE5 (FAN1) | PWM | White LED, electrical box lighting |
| NeoPixel strip | PB0 (RGB_LED) | WS2812 | 120 LEDs, GRB color order |

## Pin Mapping - EBB42 Tool Heads

### Mill Head (EBBCanMILL - `0fbff82fd51f`)

| Function | Pin | Type | Notes |
|----------|-----|------|-------|
| Spindle thermistor | PA3 (TH0) | Analog | ATC Semitec 104GT-2 |
| Spindle endstop | PB6 | Input | Tool position detection |
| **ADXL345 (Vibration)** | | | |
| CS | PB12 | SPI | Chip Select |
| SCLK | PB10 | SPI | Clock |
| MOSI | PB11 | SPI | Master Out |
| MISO | PB2 | SPI | Master In |

### 3D Print Head (EBBCanPRINT - `c64b129f89d0`)

| Function | Pin | Type | Specifications |
|----------|-----|------|----------------|
| **Extruder** | | | |
| Step | PD0 | Digital | TMC2209 integrated |
| Dir | PD1 | Digital | |
| Enable | !PD2 | Digital | |
| UART | PA15 | UART | TMC2209 communication |
| **Heating** | | | |
| Heater | PB13 | PWM | Heating cartridge |
| Thermistor | PA3 (TH0) | Analog | Generic 3950 |
| **Ventilation** | | | |
| Hotend fan | PA0 (FAN1) | PWM | 50°C threshold |
| Heatbreak fan | PA1 (FAN2) | PWM | 50°C threshold |
| **Probe** | | | |
| Servo probe | PB9 | PWM | Probe deployment |
| Probe signal | !PB8 | Input | Contact detection |
| **ADXL345** | PB12,PB10,PB11,PB2 | SPI | Resonance calibration |

**Extruder Specifications**:
- **Microstepping**: 64 microsteps
- **Rotation distance**: 3.433mm
- **Nozzle diameter**: 0.4mm
- **Filament diameter**: 1.75mm
- **Max temperature**: 260°C
- **Min extrusion temperature**: 180°C

### Pellet Head (EBBCanPELLET - `38a6930ee689`)

| Function | Pin | Type | Specifications |
|----------|-----|------|----------------|
| **Pellet Extruder** | | | |
| Step | PD0 | Digital | TMC2209 integrated |
| Dir | PD1 | Digital | |
| Enable | !PD2 | Digital | |
| UART | PA15 | UART | TMC2209 communication |
| **Heating** | | | |
| Heater | PB13 | PWM | Heating cartridge |
| Thermistor | PA3 (TH0) | Analog | NTC 100K MGB18 |
| **Ventilation** | | | |
| Hotend fan | PA0 (FAN1) | PWM | 40°C threshold |
| Heatbreak fan | PA1 (FAN2) | PWM | 40°C threshold |
| **Probe** | PB9, !PB8 | PWM/Input | Probe system |
| **ADXL345** | PB12,PB10,PB11,PB2 | SPI | Calibration |

**Pellet Specifications**:
- **Rotation distance**: 1.7mm
- **Nozzle diameter**: 0.8mm
- **Filament diameter**: 0.8mm (pellets)
- **Max temperature**: 300°C

### Pen Plotter Head (EBBCanPENPLT - `unknow`)

| Function | Pin | Type | Notes |
|----------|-----|------|-------|
| Pen endstop | PB6 | Input | Pen position detection |
| **ADXL345** | PB12,PB10,PB11,PB2 | SPI | Vibration calibration |

**Pin Details**:
- CS: PB12, SCLK: PB10, MOSI: PB11, MISO: PB2

## B-Axis (4th Axis) Implementation

### Hardware Configuration
- **Stepper**: Manual stepper on Driver 5 (PC13, !PF0, !PF1)
- **Gear Ratio**: 54:1 reduction
- **Rotation Distance**: 360mm (1mm = 1°)
- **Microstepping**: 16 microsteps

### Software Implementation
The B-axis extends standard G-code commands through macro interception:

```gcode
G0 X100 Y50 Z10 B45    # Rapid move with 45° rotation
G1 X200 B90 F1000      # Linear move with rotation to 90°
G2 X50 Y50 I25 J0 B180 # Clockwise arc with 180° rotation
G3 X75 Y25 I10 J10 B270 # Counter-clockwise arc with 270° rotation
```

**Macro System**: 
- `SET_B_POSITION`: Core B-axis positioning with angle normalization
- Intercepted G-code: G0, G1, G2, G3 macros parse B parameter
- Position tracking: Maintains `b_position` variable for continuous rotation
- Speed calculation: Converts feedrate to angular velocity using perimeter setting

## Heated Bed and Common Sensors

### Heated Bed (Shared Print/Pellet)

| Function | Pin | Type | Specifications |
|----------|-----|------|----------------|
| Heater | PA2 (HE0) | PWM | 24V silicone heater |
| Thermistor | PF3 (TB) | Analog | ATC Semitec 104GT-2 |
| Max temperature | | | 130°C |

## CAN Bus Configuration

### Network Parameters
```bash
# /etc/network/interfaces.d/can0
allow-hotplug can0 
iface can0 can static 
    bitrate 500000 
    up ifconfig $IFACE txqueuelen 128
```

### UUID by Tool Head
- **Mill**: `0fbff82fd51f` (EBBCanMILL)
- **Print**: `c64b129f89d0` (EBBCanPRINT)  
- **Pellet**: `38a6930ee689` (EBBCanPELLET)
- **PenPlt**: `unknow` (EBBCanPENPLT) - needs configuration

## Electrical Specifications

### Power Supply
- **Main voltage**: 24V DC
- **Max consumption**: 
  - Octopus V1.1: ~5A
  - EBB42: ~2A per head
  - Spindle: ~8A max
  - Heated bed: ~10A max

### Connectors and Wiring

#### CAN Bus
- **Topology**: Linear bus with 120Ω terminations
- **Max length**: 40m at 500kbps
- **Connectors**: JST-XH 4 pins (CAN_H, CAN_L, 24V, GND)

#### Tool Head Power
- **Voltage**: 24V via CAN bus
- **Protection**: Individual fuses recommended
- **Consumption**: 1-2A per head depending on mode

## Dimensions and Kinematics

### Machine Limits
- **X travel**: 220mm (position_max)
- **Y travel**: 300mm (position_max)
- **Z travel**: 250mm (position_max, position_min -25mm)
- **B rotation**: 360° continuous

### Speeds and Accelerations
```ini
max_velocity = 150          # mm/s
max_accel = 750            # mm/s²
max_z_velocity = 20        # mm/s
max_z_accel = 100          # mm/s²
```

### Homing
- **X, Y**: Homing towards 0 (min endstops)
- **Z**: Homing towards maximum (position_endstop = 250)
- **Homing speed**: 10 mm/s
- **Second speed**: 2 mm/s (precision)

## Sensors and Feedback

### ADXL345 (All Heads)
- **Interface**: SPI software
- **Axes**: x,y,z mapping
- **Usage**: Resonance calibration, vibration detection
- **Frequency**: Configurable per mode

### Thermistors
- **Print**: Generic 3950 (hotend), 50°C fan thresholds
- **Pellet**: NTC 100K MGB18-104F39050L32 (hotend), 40°C fan thresholds
- **Mill**: ATC Semitec 104GT-2 (spindle)
- **Bed**: ATC Semitec 104GT-2 (shared print/pellet modes)

### Contact Probes
- **Type**: Servo-deployable with microswitch (PB9 servo, !PB8 signal)
- **Precision**: ±0.05mm (samples_tolerance)
- **Repeatability**: 2 samples minimum
- **Offsets**: 
  - Print mode: X=-40, Y=-35, Z=0.8
  - Pellet mode: X=0, Y=0, Z=0.3

## Extended G-Code Implementation

### Tool-Specific Commands

#### Mill Mode (M3/M4/M5/M6)
```gcode
M3 S12000      # Spindle clockwise at 12000 RPM
M4 S8000       # Spindle counter-clockwise at 8000 RPM  
M5             # Spindle stop with deceleration ramp
M6             # Manual tool change procedure
```

#### Print/Pellet Modes
```gcode
G29            # Automatic bed mesh calibration
PROBE_DOWN     # Deploy servo probe
PROBE_UP       # Retract servo probe
```

#### Common Macros
```gcode
G92 X0 Y0 Z0   # Extended origin setting (overridden)
ORIGIN         # Set current position as origin
MANUAL_HOME    # Set kinematic position without homing
```

### Safety Features
- **Mill**: Door switch (PG11) triggers M112 emergency stop
- **Print**: Temperature monitoring prevents cold extrusion
- **Pen Plotter**: End-effector sensor (PB6) stops on contact
- **All modes**: CAN heartbeat monitoring for tool head connection

## Maintenance and Diagnostics

### Regular Check Points
1. **CAN bus voltages**: Verify 24V and differential signals
2. **Temperatures**: Monitoring via thermistors
3. **Vibrations**: ADXL345 analysis for mechanical wear
4. **Endstops**: Safety function testing
5. **Connectors**: Seal and contact verification

### Diagnostic Tools
```bash
# CAN bus test
python /home/minifab/klipper/scripts/canbus_query.py can0

# System logs
journalctl -u klipper
tail -f /tmp/klippy.log

# MiniFab interface
curl localhost:8000/toolhead
curl localhost:8000/last_error
```

### Interface Customization

#### Available Themes
- **Mainsail**: `src/mainsail_theme/custom.css`
- **KlipperScreen**: `src/klipperscreen_theme/`
  - `style.conf`: Theme configuration
  - `style.css`: Custom styles
  - `images/`: Icons and images

#### Theme Installation
Themes are automatically installed via `setup.py`:
- Mainsail theme → `~/.theme/`
- KlipperScreen theme → `~/KlipperScreen/styles/minifab/`

### Component Replacement

#### Tool Heads
1. Configure new UUID in corresponding printer.cfg
2. Flash Klipper firmware on new board
3. Test automatic detection via web interface

#### Sensors
- Thermistors: Verify resistance at room temperature
- Endstops: Test open/closed circuit continuity
- ADXL345: Verify SPI communication and axes
