#! /usr/bin/python3

stringToEncypt = "Burning 'em, if you ain't quick and nimble \
I go crazy when I hear a cymbal"

key = "ICE"

def encrypt(stringToEncypt, key):

    result = ""
    times = len(stringToEncypt) // len(key)
    bigKey = (times + 1)*key
    print(bigKey)
    print(bytes.hex(bytes(ord(a)^ord(b) for (a,b) in zip(stringToEncypt,bigKey))))

    # mod  = len(stringToEncypt) % len(key)

encrypt(stringToEncypt, key)
