# Tableau des Pins, Fonctions et Fichiers Associés

| Pin (MCU:Pin)                | Fonction / Signal                | Fichier(s) de configuration                                 |
|------------------------------|----------------------------------|------------------------------------------------------------|
| PA2                          | Chauffage lit (heater_bed)       | toolheads/print/machine.cfg, toolheads/pellet/machine.cfg  |
| PF3                          | Thermistance lit (sensor_pin)    | toolheads/print/machine.cfg, toolheads/pellet/machine.cfg  |
| EBBCanPRINT:PD0              | Extrudeur step                   | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PD1              | Extrudeur dir                    | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PD2              | Extrudeur enable                 | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PB13             | Chauffage hotend                 | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PA3              | Thermistance hotend              | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PA15             | UART TMC2209 extrudeur           | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PA0              | Ventilateur hotend               | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PB12             | ADXL345 CS                       | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PB10             | ADXL345 SCLK                     | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PB11             | ADXL345 MOSI                     | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PB2              | ADXL345 MISO                     | toolheads/print/machine.cfg                                |
| EBBCanPRINT:PB9              | Servo sonde (probe_enable)       | toolheads/print/probe.cfg                                  |
| EBBCanPRINT:PB8              | Sonde (probe)                    | toolheads/print/probe.cfg                                  |
| EBBCanPELLET:PD0             | Extrudeur step                   | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PD1             | Extrudeur dir                    | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PD2             | Extrudeur enable                 | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PB13            | Chauffage hotend                 | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PA3             | Thermistance hotend              | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PA15            | UART TMC2209 extrudeur           | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PA0             | Ventilateur hotend               | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PB12            | ADXL345 CS                       | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PB10            | ADXL345 SCLK                     | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PB11            | ADXL345 MOSI                     | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PB2             | ADXL345 MISO                     | toolheads/pellet/machine.cfg                               |
| EBBCanPELLET:PB9             | Servo sonde (probe_enable)       | toolheads/pellet/probe.cfg                                 |
| EBBCanPELLET:PB8             | Sonde (probe)                    | toolheads/pellet/probe.cfg                                 |
| PA8                          | Contrôle vitesse broche (PWM)    | board_pins.cfg                                             |
| PB0                          | Bandeau Neopixel                 | main_printer.cfg                                           |
| PF13                         | Stepper X step                   | stepper.cfg                                                |
| PF12                         | Stepper X dir                    | stepper.cfg                                                |
| PF14                         | Stepper X enable                 | stepper.cfg                                                |
| PG10                         | Endstop X                        | stepper.cfg                                                |
| PG0                          | Stepper Y step                   | stepper.cfg                                                |
| PG1                          | Stepper Y dir                    | stepper.cfg                                                |
| PF15                         | Stepper Y enable                 | stepper.cfg                                                |
| PG9                          | Endstop Y                        | stepper.cfg                                                |
| PF11                         | Stepper Y1 step                  | stepper.cfg                                                |
| PG3                          | Stepper Y1 dir                   | stepper.cfg                                                |
| PG5                          | Stepper Y1 enable                | stepper.cfg                                                |
| PG4                          | Stepper Z step                   | stepper.cfg                                                |
| PC1                          | Stepper Z dir                    | stepper.cfg                                                |
| PA0                          | Stepper Z enable                 | stepper.cfg                                                |
| PG6                          | Endstop Z                        | stepper.cfg                                                |
| PF9                          | Stepper Z1 step                  | stepper.cfg                                                |
| PF10                         | Stepper Z1 dir                   | stepper.cfg                                                |
| PG2                          | Stepper Z1 enable                | stepper.cfg                                                |
| PC13                         | Axe rotation step                 | stepper.cfg, b_axis/stepper.cfg                            |
| PF0                          | Axe rotation dir                  | stepper.cfg, b_axis/stepper.cfg                            |
| PF1                          | Axe rotation enable               | stepper.cfg, b_axis/stepper.cfg                            |
| EBBCanPENPLT:PB12            | ADXL345 CS (penplt)              | toolheads/penplt/machine.cfg                               |
| EBBCanPENPLT:PB10            | ADXL345 SCLK (penplt)            | toolheads/penplt/machine.cfg                               |
| EBBCanPENPLT:PB11            | ADXL345 MOSI (penplt)            | toolheads/penplt/machine.cfg                               |
| EBBCanPENPLT:PB2             | ADXL345 MISO (penplt)            | toolheads/penplt/machine.cfg                               |
| EBBCanPENPLT:PB6             | Bouton arrêt urgence (penplt)    | toolheads/penplt/machine.cfg                               |
| PG11                         | Bouton arrêt urgence (mill)      | toolheads/mill/spindle.cfg                                 |
