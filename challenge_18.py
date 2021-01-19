# key=YELLOW SUBMARINE
#       nonce=0
#       format=64 bit unsigned little endian nonce,
#              64 bit little endian block count (byte count / 16)
import binascii
import os
from Crypto.Cipher import AES


def xor(stringToEncypt, key):

    a = bytes(a ^ b for (a, b) in zip(stringToEncypt, key))
    return a

message = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
decMessage = binascii.a2b_base64(message)

key="YELLOW SUBMARINE"
obj = AES.new(key,AES.MODE_ECB)
# AES.new()

x = 0

def ctrMode(text):
    l = len(text)//16 + 1
    nonce = x.to_bytes(length=(64 + (x).bit_length()) // 8, byteorder='little', signed=False)
    c = b""
    for i in range(l+1):
        arg = nonce + i.to_bytes(length=8, byteorder='little')
        c += obj.encrypt(arg)
    print(xor(text,c))

print(decMessage)
ctrMode(decMessage)
# print(decMessage)