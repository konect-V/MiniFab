<div align="center">

![MiniFab Logo](docs\assets\img\logo.png)

# MiniFab

</div>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red.svg)
![Klipper](https://img.shields.io/badge/firmware-Klipper-green.svg)
![CAN Bus](https://img.shields.io/badge/communication-CAN%20Bus-orange.svg)

> **One machine, three functions: the future of multimodal digital manufacturing**

MiniFab rework digital manufacturing by transforming a single machine into **three specialized tools**: CNC mill, 3D printer, and pen plotter. Based on Klipper and powered by intelligent automatic detection via CAN bus, MiniFab dynamically configures your machine according to the connected tool.

---

## ✨ Why MiniFab?

### 🔄 **Revolutionary Versatility**
- **3 machines in 1**: CNC, 3D printing, plotting
- **Automatic switching**: Intelligent toolhead detection
- **Unified interface**: Single interface for all modes

### 🧠 **Embedded Intelligence**
- **Automatic CAN detection**: Instant tool recognition
- **Dynamic configuration**: Automatic parameter adaptation
- **Integrated safety**: Mode-specific protections

### 🎯 **Optimized Performance**
- **Klipper firmware**: Precise and performant control
- **Rotary B-axis**: Integrated 4-axis manufacturing
- **Real-time monitoring**: Dedicated web interface

---

## 🏗️ Manufacturing Modes

| Mode | Capabilities | Specifics |
|------|-------------|-----------|
| **🔧 CNC Mill** | Precision machining, spindle control M3/M4/M5 | Assisted tool change M6, integrated vacuum |
| **🖨️ 3D Print** | FDM printing, heated bed, auto calibration | Deployable probe, multi-material management |
| **✏️ Pen Plotter** | Vector plotting, optimized movements | Simplified interface, precise pen control |
| **🔩 Pellet** | Pellet extrusion, large nozzle | Economic manufacturing, recycled materials |

---

## 🚀 Quick Start

### Rapid Installation

```bash
# 1. Clone the project
git clone https://github.com/DeVinci-FabLab/MiniFab

# 2. Automatic installation
cd MiniFab/src/scripts && python setup.py
```

### Interface Access

- **🌐 Main Interface**: `http://[IP]:80` (Mainsail)
- **📊 MiniFab Dashboard**: `http://[IP]:8000` (Monitoring)

---

## 📚 Technical Documentation

### 🏛️ **System Architecture**
- **[Complete architecture](docs/architecture.md)**: Detailed technical structure
- **[System overview](docs/minifab_system_overview.md)**: Global system operation

### ⚙️ **Configuration & Hardware**
- **[Hardware reference](docs/hardware_reference.md)**: Complete technical specifications
- **[Pin table](docs/pins.md)**: Pin/function correspondence

### 👤 **Usage**
- **[User guide](docs/minifab_user_guide.md)**: Complete user manual
- **[Installation procedure](docs/computer_setup_procedure.md)**: Step-by-step installation

---

## 🔧 Technical Architecture

### Main Components

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Web Interface │◄──►│ Raspberry Pi │◄──►│  Octopus V1.1   │
│    (Mainsail)   │    │  (Klipper)   │    │   (Motors)      │
└─────────────────┘    └──────┬───────┘    └─────────────────┘
                              │                       │
                              │ MiniFab Scripts       │ CAN Bus
                              ▼                       ▼
                    ┌──────────────────┐    ┌─────────────────┐
                    │  autofirmware.py │    │   Toolheads     │
                    │   (Detection)    │    │  (EBB42 CAN)    │
                    └──────────────────┘    └─────────────────┘
```

### Key Files
- **`src/scripts/autofirmware.py`**: Automatic tool detection
- **`src/scripts/confswap.py`**: Configuration management
- **`src/config/toolheads/`**: Specialized configurations per mode
- **`src/config/common/`**: Shared configurations

---

## 🤝 Contribution & Support

### 📖 **Documentation**
All technical documentation is located in the [`docs/`](docs/) folder with detailed guides for installation, usage, and maintenance.

### 🐛 **Report an Issue**
Use [GitHub Issues](../../issues) to report bugs or suggest improvements.

---

## 📄 License & Credits

**License**: MIT - See [LICENSE](LICENSE) for details

**Developed by**: [DeVinci Fablab](mailto:fablab@devinci.fr)

---

<div align="center">

**⭐ If MiniFab helps you in your projects, don't hesitate to give it a star!**

[🚀 Get Started](docs/computer_setup_procedure.md) • [📚 Documentation](docs/) • [🤝 Contribute](../../issues)

</div>