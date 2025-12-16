#!/usr/bin/env python3
import struct

# Use simple ASCII to avoid parsing issues
long_path = b"A" * 3000

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(long_path)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
