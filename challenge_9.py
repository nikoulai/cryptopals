#! /usr/bin/python3

blocksize = 20

stringToPad = "YELLOW SUBMARINE"

pads = blocksize - len(stringToPad)%blocksize
if pads==0:
    pads=blocksize
padding = pads*("\\x"+("0"if pads<10 else "")+str(pads))
paddedString = stringToPad + padding
print(paddedString)
