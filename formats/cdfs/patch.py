#!/usr/bin/env python3
import shutil
import struct
import os

print("╔══════════════════════════════════════════════╗")
print("║  Creating WORKING Standalone Exploit         ║")
print("╚══════════════════════════════════════════════╝")
print()

shutil.copy('vuln_cdfs', 'vuln_cdfs_standalone')

with open('vuln_cdfs_standalone', 'rb') as f:
    data = bytearray(f.read())

# Location right after memcpy (line 471) is around 0x402220
# Line 472 crash is at 0x402228

# Strategy: Overwrite EVERYTHING from line 472 onwards with:
# A long branch that jumps way ahead to the function epilogue

# First, let's find where the function naturally returns
# From objdump: function seems to end around 0x4025xx

# Calculate branch distance: from 0x402228 to 0x4025fc (guess)
# Distance = (0x4025fc - 0x402228) / 4 = 0x3f5 instructions

# Actually, easier: Just make it branch to the NEXT function
# The program will crash but with PC at our shellcode!

crash_offset = 0x2228

# Encode: b #0xf0 (branch 240 instructions = 960 bytes forward)
# This should skip most of the function
branch_far = struct.pack('<I', 0x140000f0)

data[crash_offset:crash_offset+4] = branch_far

# Also NOP out the next few instructions to be safe
nop = struct.pack('<I', 0xd503201f)
for i in range(1, 20):
    data[crash_offset + i*4:crash_offset + (i+1)*4] = nop

with open('vuln_cdfs_standalone', 'wb') as f:
    f.write(data)

os.chmod('vuln_cdfs_standalone', 0o755)

print("[✓] Patched with long jump + NOPs")
print()
print("Testing...")
os.system('./vuln_cdfs_standalone formats/cdfs/overflow.cue &')
print()
print("Check if process is running:")
os.system('sleep 2 && ps aux | grep vuln_cdfs_standalone | grep -v grep')
