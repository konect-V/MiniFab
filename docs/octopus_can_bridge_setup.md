**The following document is a revised step-by-step guide, originally
created for this video : <https://www.youtube.com/watch?v=Ho8dSqwX4-Q>
(posted by [Driver 732)]{.underline}**

**GENERATE CANBOOT FIRMWARE**

Type: '*git clone https://github.com/Arksine/CanBoot*' to download
CanBoot by Arksine

![](assets/octopus_can_bridge_setup/img/image001.png)

Type: '*cd CanBoot*' and '*make menuconfig*' to enter the CanBoot
Configuration. Note that Linux is case sensitive and typing: '*canboot*'
will throw an error.

![](assets/octopus_can_bridge_setup/img/image003.png)

There are several lines to change. Micro-controller Architecture to
'STMicroelectronics STM32', Processor model to (controller chipset), and
Clock Reference to '12 MHz crystal'. These are specifically for my
Octopus Pro F446. Screenshot of my settings:

![](assets/octopus_can_bridge_setup/img/image005.png)

The processor model is labeled on the chip.

![](assets/octopus_can_bridge_setup/img/image007.png)

Type: '*q*' then '*y*' to save.

![](assets/octopus_can_bridge_setup/img/image009.png)

Type: '*make*' which compiles the firmware into a subdirectory called
'out'.

![](assets/octopus_can_bridge_setup/img/image011.png)

Type: '*cd out*' which navigates to the subfolder and '*ls -l*' lists
the generated files. The 'canboot.bin' file is here and typing: '*pwd*'
lists the full path which can be used for file copying.

![](assets/octopus_can_bridge_setup/img/image013.png)

This entire directory gets overwritten once we re-run menuconfig, so
rename 'canboot.bin' to 'octopus_canboot.bin' or similar. Type: '*mv
canboot.bin octopus_canboot.bin'* to rename the file.

![](assets/octopus_can_bridge_setup/img/image015.png)

From your Windows machine, download and run WinSCP. Connect using your
Pi's IP address and simply move the 'octopus_canboot.bin' file over to
the Desktop. Reference the full file path from earlier to locate the
.bin file.

![](assets/octopus_can_bridge_setup/img/image017.png)

![](assets/octopus_can_bridge_setup/img/image019.png)

![](assets/octopus_can_bridge_setup/img/image021.png)

Back in CMD, make sure you are in the right directory. Type: *'cd
\~/CanBoot'*

![](/assets/octopus_can_bridge_setup/img/image023.png)

Type: *'make clean'* followed by *'make menuconfig'*

![](assets/octopus_can_bridge_setup/img/image025.png)

Repeat for the EBB42 v1.2 board. Note that I am using the default CAN
bus speed of 500000. This number should not be set lower, especially if
using ADXL input shaping. Some have had better luck increasing this to
1000000, which may resolve certain data communication issues.

![](assets/octopus_can_bridge_setup/img/image027.png)

Quit and save. Type: *'make'* to generate a new firmware which saves to
the same 'out' subdirectory.

![](assets/octopus_can_bridge_setup/img/image029.png)

Navigate to the subdirectory and rename this new 'canboot.bin' file to
'ebb42_canboot.bin' or similar. Copy this file over to Windows Desktop
using WinSCP.

![](assets/octopus_can_bridge_setup/img/image031.png)

**FLASH CANBOOT FIRMWARE**

**If you did not read the disclaimer at the beginning, please do so
before proceeding.**

Download STM32CubeProgrammer:

<https://www.st.com/en/development-tools/stm32cubeprog.html#get-software>

At this time, version 2.13.0 will *not* work and must be downgraded for
the firmware flash to work. I am using version 2.8.0. Accept all
installation defaults and dependency packages (not shown).

![](assets/octopus_can_bridge_setup/img/image033.png)

Unless the Octopus is powered by the 24V PSU, you need jumpers installed
on BOTH the 'USB-C Power' AND 'Boot0' pins on the board. Otherwise, a
USB A to C cable connected from the Windows computer is not powerful
enough. This is contrary to many guides stating to remove the 'USB-C
Power' jumper. Remove all other jumpers and motor drivers if you have
difficulty powering the board.

![](assets/octopus_can_bridge_setup/img/image035.png)
Press and hold the reset button for at least five seconds to set the
Octopus to DFU mode.

![](assets/octopus_can_bridge_setup/img/image037.png)

Start the STM32CubeProgrammer software. The following steps do not work
if the software is started before setting the board in DFU mode. Click
'Connect'. Status should change from 'Not connected' to 'Connected'
which reads the memory contents.

![](assets/octopus_can_bridge_setup/img/image039.png)

Erase by clicking the icon on the left, clicking 'Erase external memory'
and then 'Full chip erase'. I could not grab proper screenshots, so you
will see much more information. It will prompt to 'erase full chip flash
memory' and once finished, notify that 'Mass erase command correctly
executed'. Be aware of error messages that may indicate problems with
the process or a botched attempt. You may need to repeat this several
times.

![](assets/octopus_can_bridge_setup/img/image041.png)

Once successfully erased, click the write icon on the left and click
'Open File'. Choose the octopus_canboot.bin file from earlier, and click
'Download'. Again, my screenshot is slightly off since I wrote this
documentation after the fact 😊

![](assets/octopus_can_bridge_setup/img/image043.png)

If everything goes well, you should see success messages. If this is the
case, click the 'Disconnect' button and unplug the board from computer.

![](assets/octopus_can_bridge_setup/img/image049.png)

Be aware of errors such as this. You may have to re-attempt or
investigate why it is happening. In this scenario, it was due to the
buggy 2.13 version of software, and the reason I rolled back to 2.8

![](assets/octopus_can_bridge_setup/img/image051.png)

**REMOVE** BOTH JUMPERS FROM 5V USB C AND BOOT0 PINS ON THE MCU

![](assets/octopus_can_bridge_setup/img/image053.png)

Repeat for the EBB42 board. Start by placing a jumper on the VBUS (near
usb-c socket) header pins and plug in the same USB cable for power.
Press and hold BOOT0, press and release RESET, release BOOT0 to enter
DFU mode.

Start STM32CubeProgrammer as before and follow the exact same steps of
erasing and re-writing the memory, only this time using the
ebb42_canboot.bin file. Once completed, remove the jumper from VBUS and
place it on the 120R pins.

**SET UP KLIPPER FIRMWARE**

Return to CMD and navigate to the Klipper directory, type: *'cd
\~/klipper'* and *'make menuconfig'*

![](assets/octopus_can_bridge_setup/img/image055.png)

Here are the configuration settings for the F446 Octopus Pro. Note the
CAN bus speed must match what was specified earlier. Some other settings
are copied over from earlier.

![](assets/octopus_can_bridge_setup/img/image057.png)

Type: *'make'* to compile the Klipper firmware

![](assets/octopus_can_bridge_setup/img/image059.png)

As before, rename the Klipper file to prevent overwriting in the next
step. Type: *'cd out'* followed by *'mv klipper.bin
octopus_klipper.bin'*. Move the file by typing: *'mv octopus_klipper.bin
\~\klipper'*

![](assets/octopus_can_bridge_setup/img/image061.png)

Type: *'cd ..'* and *'ls -l'* to make sure renamed file exists in the
parent Klipper directory.

![](assets/octopus_can_bridge_setup/img/image063.png)

Type: *'make clean'* and *'make menuconfig'* to repeat for the EBB36
board

![](assets/octopus_can_bridge_setup/img/image065.png)

![](assets/octopus_can_bridge_setup/img/image067.png)

Quit, Save, and type: *'make'* to generate another firmware for the
EBB42 board.

![](assets/octopus_can_bridge_setup/img/image069.png)

Repeat previous steps to rename and move ebb_klipper .bin file to parent
Klipper directory.

![](assets/octopus_can_bridge_setup/img/image071.png)

Type: *'make clean'*

![](assets/octopus_can_bridge_setup/img/image073.png)

Plug in Octopus to Pi via USB A to C cable and power printer on. Use a
proper cable with data capability, some USB cables only provide power.
From CMD, type: *'ls /dev/serial/by-id/\*'* which returns the serial
device ID of the Octopus board. Copy this down.

![](assets/octopus_can_bridge_setup/img/image075.png)

Type: *'cd CanBoot/scripts'* then *'pip3 install pyserial'*

![](assets/octopus_can_bridge_setup/img/image079.png)

Type: '*python3 flash_can.py -f \~/octopus_klipper.bin -d (serial
number)*' to flash Octopus over serial.

![](assets/octopus_can_bridge_setup/img/image081.png)

Type: *'cd'* then *'sudo nano /etc/network/interfaces.d/can0'*

Paste the following, once again noting that bitrate matches the speed
specified earlier if y.

allow-hotplug can0

iface can0 can static

bitrate 500000

up ifconfig \$IFACE txqueuelen 128

![](assets/octopus_can_bridge_setup/img/image083.png)

Press CTRL X to save and quit.

From CMD, type: 'sudo reboot'

Connect octopus with Ebb42 via RJ11 cable, you can power the ebb42 via
USB or via 24v pins.

From CMD, type: '*ifconfig'*. Look for the can0 entry.

![](assets/octopus_can_bridge_setup/img/image085.png)
Type: *'cd CanBoot/scripts'* and *'python3 flash_can.py -i can0 -q'*
which now lists the UUID for both the Octopus and EBB42. The Klipper
label references Octopus, and CanBoot references the EBB42. Copy both
down.

![](assets/octopus_can_bridge_setup/img/image087.png)

Type: '*python3 flash_can.py -f \~/klipper/ebb_klipper.bin -u (ebbID
canboot)'* to flash Klipper to the EBB36 board via CAN.

![](assets/octopus_can_bridge_setup/img/image042.png)

Load Mainsail, which may still show errors. Add both UUID from previous
step into the printer.cfg for each cfg file where you find
"canbus_uuid:". Click 'Save and Restart'. You may also need to do a
firmware restart.

![](assets/octopus_can_bridge_setup/img/image043.png)

Click 'Machine', check that both CAN UUIDs are present and you are done!
As with non-CAN installs, time to configure printer.cfg and continue
with set up/tuning. Best of luck!

![](assets/octopus_can_bridge_setup/img/image044.png)
