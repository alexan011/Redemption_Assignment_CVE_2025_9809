#!/usr/bin/env python3
import struct

payload = b"A" * 800
payload += struct.pack("<Q", 0xDEADBEEFCAFEBABE)  # At 800
payload += b"B" * 200
payload += struct.pack("<Q", 0x1122334455667788)  # At 1008
payload += b"C" * (3000 - len(payload))

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
