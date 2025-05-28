ESP32C3:

1. Hold down B or Boot button and connect the board to your PC using a data USB-C cable (this will put it in bootloader mode).

2. Open CMD

3. devmgmt.msc and check COM port

4. esptool --port COM_ erase_flash

5. cd to this directory (D:\Coding-Folder\Projects\Flashing Micropython)

6. esptool --port COM_ write_flash -z 0x0 ESP32_GENERIC_C3-20240602-v1.23.0.bin