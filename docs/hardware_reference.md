# MiniFab Hardware Reference

## Configuration Sources

### Main Configuration Files
- **Common pins**: `src/config/common/board_pins.cfg`
- **Motor configuration**: `src/config/common/stepper.cfg`
- **B-axis specific**: `src/config/b_axis/stepper.cfg`
- **Tool-specific configs**: `src/config/toolheads/{toolhead}/machine.cfg`
- **Probe configurations**: `src/config/toolheads/{print,pellet}/probe.cfg`
- **Spindle configuration**: `src/config/toolheads/mill/spindle.cfg`

## Pin Mapping - Octopus V1.1

**Configuration source**: `src/config/common/board_pins.cfg` and `src/config/common/stepper.cfg`

### Main Motors

| Motor | Step Pin | Dir Pin | Enable Pin | Endstop | Notes |
|--------|----------|---------|------------|---------|-------|
| X (Driver 0) | PF13 | PF12 | !PF14 | !PG10 (DIAG2) | Main X axis |
| Y (Driver 1) | PG0 | PG1 | !PF15 | !PG9 (DIAG1) | Main Y axis |
| Y1 (Driver 2) | PF11 | PG3 | !PG5 | - | Secondary Y axis |
| Z (Driver 3) | PG4 | PC1 | !PA0 | !PG6 (DIAG0) | Main Z axis |
| Z1 (Driver 4) | PF9 | PF10 | !PG2 | - | Secondary Z axis |
| B (Driver 5) | PC13 | !PF0 | !PF1 | - | Rotation axis |

**B-axis details**: See `src/config/b_axis/stepper.cfg` - 54:1 gear ratio, 360° rotation distance

### Spindle Control and Actuators

**Configuration source**: `src/config/common/board_pins.cfg`

| Function | Pin | Type | Notes |
|----------|-----|------|-------|
| Spindle speed | PD12 (FAN2) | PWM | Hardware PWM, 0.01s cycle |
| Forward direction | PD13 (FAN3) | Digital | Clockwise rotation |
| Reverse direction | PD14 (FAN4) | Digital | Counter-clockwise rotation |
| Vacuum socket | PA2 (HE0) | Digital | Vacuum cleaner control |
| Electric box LED | PE5 (FAN1) | PWM | Electrical box lighting |
| Door detection | PG11 (DIAG3) | Input | Mill safety |

**Spindle control implementation**: See `src/config/toolheads/mill/spindle.cfg` for M3/M4/M5 macros

### Lighting and Signaling

**Configuration source**: `src/config/common/board_pins.cfg`

| Function | Pin | Type | Specifications |
|----------|-----|------|----------------|
| Electric box LED | PE5 (FAN1) | PWM | White LED, electrical box lighting |
| NeoPixel strip | PB0 (RGB_LED) | WS2812 | 120 LEDs, GRB color order |

## Pin Mapping - EBB42 Tool Heads

### Mill Head (EBBCanMILL - `0fbff82fd51f`)

**Configuration source**: `src/config/toolheads/mill/machine.cfg`

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

**Configuration source**: `src/config/toolheads/print/machine.cfg` and `src/config/toolheads/print/probe.cfg`

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

### Pellet Head (EBBCanPELLET - `38a6930ee689`)

**Configuration source**: `src/config/toolheads/pellet/machine.cfg` and `src/config/toolheads/pellet/probe.cfg`

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

### Pen Plotter Head (EBBCanPENPLT)

**Configuration source**: `src/config/toolheads/penplt/machine.cfg`

| Function | Pin | Type | Notes |
|----------|-----|------|-------|
| Pen endstop | PB6 | Input | Pen position detection |
| **ADXL345** | PB12,PB10,PB11,PB2 | SPI | Vibration calibration |

## Heated Bed and Common Sensors

### Heated Bed

**Configuration source**: `src/config/toolheads/{print,pellet}/machine.cfg`

| Function | Pin | Type | Specifications |
|----------|-----|------|----------------|
| Heater | PA2 (HE0) | PWM | 24V silicone heater |
| Thermistor | PF3 (TB) | Analog | ATC Semitec 104GT-2 |
| Max temperature | | | 130°C |

## Quick Reference Links

### For detailed configuration of specific components:
- **Spindle macros (M3/M4/M5)**: `src/config/toolheads/mill/spindle.cfg`
- **Probe macros**: `src/config/toolheads/{print,pellet}/probe.cfg`
- **B-axis macros**: `src/config/b_axis/macro.cfg`
- **Tool-specific macros**: `src/config/toolheads/{toolhead}/macro.cfg`
- **Common macros**: `src/config/common/macro.cfg`

### For system-level configuration:
- **Main printer config**: `src/config/common/main_printer.cfg`
- **Moonraker API**: `src/config/moonraker.conf`
- **OctoEverywhere**: `src/config/octoeverywhere.conf`