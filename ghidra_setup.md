## Ghidra Setup
Import the file as ARMv4T BE
Setup your memory map as below
![image](https://github.com/user-attachments/assets/d387d053-c9a0-4295-a0b1-8933ce5b0169)

Import the tms470r1x_symbols.txt


## Firmware Structure

1. 0x0000000 - 0x0004000 - BootLoader - Not accessible via update files
2. 0x0004000 - 0x007FFFF - TMS470R1 Main 
3. 0x0020000 - 0x00207CF - TMS470R1 Main RAM
4. 0x0084000 - TMS470R1  - Co-Processor


