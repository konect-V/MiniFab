# Computer Setup Procedure

## Motherboard Setup Procedure

Install the software from <https://www.raspberrypi.com/software/>.

Then launch it.

Select the correct Raspberry Pi model, then choose Mainsail as the OS and the SD card as the storage.

Click Next, then adjust the settings with the correct Wi-Fi parameters.

Note: It is important that the user is named "minifab" if you want to follow the tutorial exactly

Then validate the settings, click Continue, and wait.

Once finished, insert the SD card into the Raspberry Pi.

Install an application like MobaXterm to connect via SSH. Use the parameters that were already set during the OS flashing onto the SD card.

Next, execute:  
`git clone https://github.com/DeVinci-FabLab/MiniFab`  

Then run:  
`cd Minifab && python setup.py`  

Install OctoPrint (this should be included in the `setup.py` script).  

Install OctoEverywhere and activate the shared connection: <https://octoeverywhere.com/> (this should also be included in the `setup.py` script).  

Then refer to **octopus_can_bridge_setup.md** for further instructions.  

Finally, enable the automatic firmware update system by running the command:  
`sudo crontab -e`  
and adding the following line:  
`@reboot /usr/bin/python /home/minifab/MiniFab/scripts/startup.py`

To finish the configuration, run:  
`sudo reboot`
