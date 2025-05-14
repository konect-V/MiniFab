# Tableau des Pins, Fonctions et Fichiers Associés

| Pin (MCU/Pin)                | Fonction / Signal                | Fichier(s) de configuration                                 |
|------------------------------|----------------------------------|------------------------------------------------------------|
| OctopusV1.1_HE0/PA2                               | Chauffage lit                    | toolheads/print/machine.cfg, toolheads/pellet/machine.cfg  |
| OctopusV1.1_TB/PF3                                | Thermistance lit                 | toolheads/print/machine.cfg, toolheads/pellet/machine.cfg  |
| EBB42v1.2_Internal/EBBCanPRINT:PD0                | Extrudeur step                   | toolheads/print/machine.cfg                                |
| EBB42v1.2_Internal/EBBCanPRINT:PD1                | Extrudeur dir                    | toolheads/print/machine.cfg                                |
| EBB42v1.2_Internal/EBBCanPRINT:PD2                | Extrudeur enable                 | toolheads/print/machine.cfg                                |
| EBB42v1.2_Hotend0/EBBCanPRINT:PB13                | Chauffage hotend                 | toolheads/print/machine.cfg                                |
| EBB42v1.2_TH0/EBBCanPRINT:PA3                     | Thermistance hotend              | toolheads/print/machine.cfg                                |
| EBB42v1.2_Internal/EBBCanPRINT:PA15               | UART TMC2209 extrudeur           | toolheads/print/machine.cfg                                |
| EBB42v1.2_FAN1/EBBCanPRINT:PA0                    | Ventilateur hotend               | toolheads/print/machine.cfg                                |
| EBB42v1.2_Internal/EBBCanPRINT:PB12               | ADXL345 CS                       | toolheads/print/machine.cfg                                |
| EBB42v1.2_Internal/EBBCanPRINT:PB10               | ADXL345 SCLK                     | toolheads/print/machine.cfg                                |
| EBB42v1.2_Internal/EBBCanPRINT:PB11               | ADXL345 MOSI                     | toolheads/print/machine.cfg                                |
| EBB42v1.2_Internal/EBBCanPRINT:PB2                | ADXL345 MISO                     | toolheads/print/machine.cfg                                |
| EBB42v1.2_Servo/EBBCanPRINT:PB9                   | Servo                            | toolheads/print/probe.cfg                                  |
| EBB42v1.2_Probe/EBBCanPRINT:PB8                   | Probe                            | toolheads/print/probe.cfg                                  |
| EBB42v1.2_Internal/EBBCanPELLET:PD0               | Extrudeur step                   | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PD1               | Extrudeur dir                    | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PD2               | Extrudeur enable                 | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PB13              | Chauffage hotend                 | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_TH0/EBBCanPELLET:PA3                    | Thermistance hotend              | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PA15              | UART TMC2209 extrudeur           | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_FAN1/EBBCanPELLET:PA0                   | Ventilateur hotend               | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PB12              | ADXL345 CS                       | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PB10              | ADXL345 SCLK                     | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PB11              | ADXL345 MOSI                     | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPELLET:PB2               | ADXL345 MISO                     | toolheads/pellet/machine.cfg                               |
| EBB42v1.2_Servo/EBBCanPELLET:PB9                  | Servo                            | toolheads/pellet/probe.cfg                                 |
| EBB42v1.2_Probe/EBBCanPELLET:PB8                  | Probe                            | toolheads/pellet/probe.cfg                                 |
| EBB42v1.2_Probe/PA8                               | Contrôle vitesse broche          | board_pins.cfg                                             |
| OctopusV1.1_RGB_LED/PB0                           | Bandeau Neopixel                 | main_printer.cfg                                           |
| OctopusV1.1_Internal_Driver0/PF13                 | Stepper X step                   | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver0/PF12                 | Stepper X dir                    | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver0/PF14                 | Stepper X enable                 | stepper.cfg                                                |
| OctopusV1.1_DIAG2/PG10                            | Endstop X                        | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver1/PG0                  | Stepper Y step                   | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver1/PG1                  | Stepper Y dir                    | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver1/PF15                 | Stepper Y enable                 | stepper.cfg                                                |
| OctopusV1.1_DIAG1/PG9                             | Endstop Y                        | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver2/PF11                 | Stepper Y1 step                  | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver2/PG3                  | Stepper Y1 dir                   | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver2/PG5                  | Stepper Y1 enable                | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver3/PG4                  | Stepper Z step                   | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver3/PC1                  | Stepper Z dir                    | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver3/PA0                  | Stepper Z enable                 | stepper.cfg                                                |
| OctopusV1.1_DIAG0/PG6                             | Endstop Z                        | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver4/PF9                  | Stepper Z1 step                  | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver4/PF10                 | Stepper Z1 dir                   | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver4/PG2                  | Stepper Z1 enable                | stepper.cfg                                                |
| OctopusV1.1_Internal_Driver5/PC13                 | Axe rotation step                | stepper.cfg, b_axis/stepper.cfg                            |
| OctopusV1.1_Internal_Driver5/PF0                  | Axe rotation dir                 | stepper.cfg, b_axis/stepper.cfg                            |
| OctopusV1.1_Internal_Driver5/PF1                  | Axe rotation enable              | stepper.cfg, b_axis/stepper.cfg                            |
| EBB42v1.2_Internal/EBBCanPENPLT:PB12              | ADXL345 CS                       | toolheads/penplt/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPENPLT:PB10              | ADXL345 SCLK                     | toolheads/penplt/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPENPLT:PB11              | ADXL345 MOSI                     | toolheads/penplt/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPENPLT:PB2               | ADXL345 MISO                     | toolheads/penplt/machine.cfg                               |
| EBB42v1.2_Internal/EBBCanPENPLT:PB6               | Endstop du stylo                 | toolheads/penplt/machine.cfg                               |
| OctopusV1.1_DIAG3/PG11                            | Ouverture de la porte            | toolheads/mill/spindle.cfg                                 |
| EBB42v1.2_Internal/EBBCanMILL:PB12                | ADXL345 CS                       | toolheads/mill/machine.cfg                                 |
| EBB42v1.2_Internal/EBBCanMILL:PB10                | ADXL345 SCLK                     | toolheads/mill/machine.cfg                                 |
| EBB42v1.2_Internal/EBBCanMILL:PB11                | ADXL345 MOSI                     | toolheads/mill/machine.cfg                                 |
| EBB42v1.2_Internal/EBBCanMILL:PB2                 | ADXL345 MISO                     | toolheads/mill/machine.cfg                                 |
| EBB42v1.2_Internal/EBBCanMILL:PB6                 | Endstop de la broche             | toolheads/mill/machine.cfg                                 |
| EBB42v1.2_TH0/EBBCanMILL:PA3                      | Thermistance de la broche        | toolheads/mill/machine.cfg                                 |
| OctopusV1.1_HE1/PA3                               | Prise aspirateur                 | board_pins.cfg                                             |

