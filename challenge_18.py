# key=YELLOW SUBMARINE
#       nonce=0
#       format=64 bit unsigned little endian nonce,
#              64 bit little endian block count (byte count / 16)
import binascii
from Crypto.Cipher import AES

def xor(stringToEncypt, key):

    a = bytes(a ^ b for (a, b) in zip(stringToEncypt, key))
    return a

message = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
decMessage = binascii.a2b_base64(message)

# randomKey = os.urandom(16)
key="YELLOW SUBMARINE"
obj = AES.new(key,AES.MODE_ECB)
# AES.new()

x = 0
nonce = x.to_bytes(length=(64 + (x).bit_length()) // 8, byteorder='little', signed=False)

def ctrMode(text):
    l = len(text)//16 + 1
    print(l)
    c = b""
    for i in range(l+1):
        # counter = (hex(i).to_bytes(((i).bit_length() + 64) // 8, 'little',signed=True))
        arg = nonce + i.to_bytes(length=8, byteorder='little')
        print(arg)
        # print(nonce+counter)
        # print(hex(i))
        # print(bytearray.fromhex(hex(i)))
        # print((hex(i),"utf-8"))
        # print(bytes(hex(i),"utf-8"))
        c += obj.encrypt(arg)
    print(xor(text,c))

    bytesText = bytes(text)
print(decMessage)
ctrMode(decMessage)
# print(decMessage)