#! /usr/bin/python3
import binascii
from Crypto.Cipher import AES


def encrypt(stringToEncypt, key):

    result = ""
    times = len(stringToEncypt) // len(key)
    print(key)
    a =  bytes(a^b for (a,b) in zip(stringToEncypt,key))
    print('\n')
    return a

file = open("10.txt")
lines = binascii.a2b_base64(file.read())
print(lines)
iv = bytes("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",'ascii')
print("iv: " + str(len(iv)))
key = "YELLOW SUBMARINE"
plaintext = bytes()
obj = AES.new(key, AES.MODE_ECB)
# check valid lenth
blocks = len(lines)//16

for i in range(blocks):

    temp = lines[i*16:(i+1)*16]
    # print(type(temp))
    xor = obj.decrypt(temp)
    print(xor)
    plaintext += encrypt(xor, iv)
    iv = temp

print(str(plaintext))
