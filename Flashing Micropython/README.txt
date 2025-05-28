ESP32C3:

1. Hold down B or Boot button and connect the board to your PC using a data USB-C cable (this will put it in bootloader mode).

2. Open CMD

3. devmgmt.msc and check COM port

4. esptool --port COM_ erase_flash

5. If you cloned the repo, cd to this directory of the directory where you downloaded your flash binary

6. esptool --port COM_ write_flash -z 0x0 
