from pwn import cyclic

# Generate a cyclic pattern without bad characters
pattern = cyclic(5000, n=4, alphabet=b"ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz0123456789")

open("formats/cdfs/pattern.txt","wb").write(pattern)
