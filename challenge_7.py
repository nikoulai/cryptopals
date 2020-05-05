#! /usr/bin/python3
import binascii
from Crypto.Cipher import AES

file = open("7.txt", 'r')
lines = binascii.a2b_base64(file.read())
key = "YELLOW SUBMARINE"
obj = AES.new(key, AES.MODE_ECB)
plaintext = obj.decrypt(lines).decode("utf-8")
print(plaintext)
