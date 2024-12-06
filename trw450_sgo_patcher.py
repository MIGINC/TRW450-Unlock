#!/usr/bin/env python3
"""
TRW450-Unlock Patch Tool
------------------------

This script applies patches to TRW450 ABS module firmware to enable indirect TPMS and ACC on HW V4, V5, and VE.

Use at your own risk. Intended for testing/off-road use only.
No firmware is provided. You must supply your own.

For more info, please visit:
https://github.com/MIGINC/TRW450-Unlock

To submit a patching request or ask questions:
- Open an issue on the GitHub repo
- Contact MIGINC at: https://github.com/MIGINC
"""

import os
import sys
import hashlib
import tempfile
import shutil
import logging
import argparse

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
    COLOR_ERROR = Fore.RED + Style.BRIGHT
    COLOR_WARNING = Fore.YELLOW + Style.BRIGHT
    COLOR_INFO = Fore.GREEN + Style.BRIGHT
    COLOR_RESET = Style.RESET_ALL
except ImportError:
    COLOR_ERROR = ""
    COLOR_WARNING = ""
    COLOR_INFO = ""
    COLOR_RESET = ""

CHECKSUMS_FILE = "checksums.txt"
PATCHES_FILE = "patches.txt"
VERSION = "1.0"

def log_error(msg):
    logging.error(COLOR_ERROR + msg + COLOR_RESET)

def log_warning(msg):
    logging.warning(COLOR_WARNING + msg + COLOR_RESET)

def log_info(msg):
    logging.info(COLOR_INFO + msg + COLOR_RESET)

def load_checksums(file_path):
    if not os.path.isfile(file_path):
        log_error(f"Checksums file missing: {file_path}")
        sys.exit(1)


    originals, updated = {}, {}
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                state, chksum, ident = parts
                chksum = chksum.upper()
                if state.upper() == "ORIGINAL":
                    originals[chksum] = ident
                elif state.upper() == "UPDATED":
                    updated[ident] = chksum
    return originals, updated

def print_logo():
    logo = f"""
{COLOR_ERROR}
██████   ██████  ██ ███████  █████  
██   ██ ██    ██ ██ ██      ██   ██ 
██████  ██    ██ ██ ███████ ███████ 
██      ██ ▄▄ ██ ██      ██ ██   ██ 
██       ██████  ██ ███████ ██   ██ 
            ▀▀   
Thanks for the help everyone                                                     
{COLOR_RESET}

{COLOR_INFO}TRW450-Unlock Patch Tool{COLOR_WARNING} Version {VERSION} {COLOR_RESET} 🚗
----------------------------------------------------
"""
    print(logo)



def load_patches(file_path):
    if not os.path.isfile(file_path):
        log_error(f"Patch file missing: {file_path}")
        sys.exit(1)

    patch_map = {}
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                ident, addr_str, orig_hex, new_hex = parts
                try:
                    addr = int(addr_str, 16)
                    orig_bytes = bytes.fromhex(orig_hex)
                    new_bytes = bytes.fromhex(new_hex)
                    patch_map.setdefault(ident, []).append((addr, orig_bytes, new_bytes))
                except ValueError:
                    log_warning(f"Invalid patch: {line}")
    return patch_map

def compute_checksum(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest().upper()

def apply_patches(file_path, checksums_file, patches_file, force=False):
    originals, updated = load_checksums(checksums_file)
    patches = load_patches(patches_file)

    input_checksum = compute_checksum(file_path)
    log_info(f"Input file checksum (sha256): {input_checksum}")

    if input_checksum not in originals:
        log_error("Unsupported SGO, contact repo with request.")
        return False

    identifier = originals[input_checksum]
    log_info(f"Matched identifier: {identifier}")

    patch_list = patches.get(identifier, [])
    if not patch_list:
        log_error("No patch found for this identifier. Check patch db for update.")
        return False

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name

    shutil.copy2(file_path, temp_path)

    def cleanup_temp():
        if not force:
            os.unlink(temp_path)

    with open(temp_path, "rb+") as f:
        data = bytearray(f.read())
        for addr, orig, new in patch_list:
            current = data[addr:addr+len(orig)]
            if current != orig:
                log_error(f"Byte mismatch at {hex(addr)}. Expected {orig.hex().upper()}, got {current.hex().upper()}.")
                cleanup_temp()
                return False
            data[addr:addr+len(new)] = new

        f.seek(0)
        f.write(data)
        f.truncate()

    expected = updated.get(identifier)
    if not expected:
        log_error("No patched checksum found for this identifier, though original was known. Check checksum db.")
        cleanup_temp()
        return False

    final = compute_checksum(temp_path)
    log_info(f"Patched checksum: {final}")

    if final != expected:
        log_error("Patching failed due to checksum mismatch.")
        cleanup_temp()
        return False

    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_patched{ext}"
    shutil.move(temp_path, output_path)
    log_info(f"Success! New file created: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Apply TRW450-Unlock patch to a provided SGO file."
    )
    parser.add_argument("firmware_file", help="Path to the SGO file to patch.")
    parser.add_argument("--checksums", default=CHECKSUMS_FILE, help="Path to the checksums file.")
    parser.add_argument("--patches", default=PATCHES_FILE, help="Path to the patches file.")
    parser.add_argument("--force", action="store_true", help="Keep the bad file")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    print_logo()
    log_warning("Off-road and test use only. Proceed at your own risk.")

    if args.force:
        log_error("DANGER: Force command used, be very careful with output")
        log_warning("Partially patched file will not be removed if patching fails.")

    if not os.path.isfile(args.firmware_file):
        log_error(f"Firmware file not found: {args.firmware_file}")
        sys.exit(1)

    success = apply_patches(
        args.firmware_file,
        checksums_file=args.checksums,
        patches_file=args.patches,
        force=args.force
    )
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
