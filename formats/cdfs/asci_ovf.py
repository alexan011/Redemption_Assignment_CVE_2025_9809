# ascii_overflow.py
with open("formats/cdfs/overflow.cue", "wb") as f:
    f.write(b'FILE "')
    f.write(b'A' * 5000)          # PURE ASCII
    f.write(b'" BINARY\n')
    f.write(b'TRACK 01 MODE1/2352\n')
    f.write(b'  INDEX 01 00:00:00\n')
