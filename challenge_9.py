#! /usr/bin/python3

blocksize = 20

stringToPad = "YELLOW SUBMARINE"

pads = blocksize - len(stringToPad)%blocksize
if pads==0:
    pads=blocksize

paddingLength = blocksize - len(stringToPad) % blocksize
pad = chr(paddingLength)
print(''.join((plaintext, pad*paddingLength)))
