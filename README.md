# TRW450-Unlock
This repository provides locations and instructions to enable indirect TPMS and ACC (Adaptive Cruise Control) functionality on VAG group TRW450 ABS modules.

This project was created to address the limited availability of TRW450 units that support ACC, allowing enthusiasts and modders to repair and retrofit older VAG vehicles, keeping them functional.


## trw450_sgo_patcher.py

A Python tool to apply pre-made patches based on known file versions.

### Features
- Patches firmware based on a binary diff database
- Checksum verification, before and after patching
- Does not modify original files
- Support for multiple firmware versions
- External patch and checksum databases

## Prerequisites

- Python 3.6 or higher
- pip 

## Usage

Basic usage:
```bash
python trw450_sgo_patcher.py <sgo_file>
```

Advanced options:
```bash
python trw450_sgo_patcher.py <sgo_file> --checksums custom_checksums.txt --patches custom_patches.txt
```
Use these arguments to specify custom checksum or patch files if you maintain your own databases.
The tool creates a new file with "_patched" suffix in the same directory as the input file. The original file is never modified.

### Command Line Arguments

- `firmware_file`: Path to the SGO file to patch
- `--checksums`: Path to custom checksums file (default: checksums.txt)
- `--patches`: Path to custom patches file (default: patches.txt)


#### checksums.txt
```
ORIGINAL <sha256_checksum> <identifier>
UPDATED <sha256_checksum> <identifier>
```
#### patches.txt
```
<identifier> <hex_address> <original_bytes> <new_bytes>
```

## Contributing

If you'd like to contribute or request support for additional firmware versions:
1. Open an issue on GitHub
2. Provide your firmware version and details
3. Follow the contribution guidelines

## Support

For support or to request new firmware version support:
- Open an issue on the GitHub repository
- Contact MIGINC directly through GitHub
## Recovery

If something goes wrong during or after flashing:

1. If flashing fails for any reason, the unit will automatically reboot into bootloader mode
   - In this mode, the unit will identify itself as **BLV: 7.4**
   - The module has limited functionality in bootloader mode
   - **IMPORTANT:** In bootloader mode, the unit can only accept another SGO flash file
   - This is a safety feature to prevent permanent bricking
2. Always keep your original firmware file for recovery
3. Have a replacement module available as a last resort


## Acknowledgments

Thanks to all contributors and testers who helped make this tool possible.

## Tested Firmware Versions
- Coming soon
## Tested Hardware Versions
- Coming soon
## Important Notes ⚠️
FOR OFF-ROAD OR TEST USE ONLY

Modifications to your ABS module are intended for off-road or testing purposes only. Using modified firmware on public roads may violate local regulations and is done entirely at your own risk.
- **No original firmware files are included.** You must obtain these yourself.
- **Use at your own risk!** Modifying ABS firmware can have safety implications. Ensure patches are tested before applying them to your car.
- **Checksum Mismatch Recovery** If the checksum does not match after flashing, the ABS module will typically fall back to bootloader mode, allowing recovery. However, there is still a small risk of bricking the device. Be prepared to replace the module if needed.

# License 📄
This project is licensed under the MIT License for scripts and tools. Documentation is licensed under CC BY-NC 4.0.

# Disclaimer
These modifications are intended for educational purposes and off-road use only. Using them on public roads may pose significant safety risks and could violate local laws or regulations.

By proceeding, you accept all responsibility for any consequences, including damage to your ABS module, vehicle, or other components. Ensure you are equipped to recover the module from bootloader mode or replace it if necessary.
