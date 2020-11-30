blocksize = 16
import os
from Crypto.Cipher import AES
from functools import reduce

randomKey = os.urandom(16)
r = randomKey
obj = AES.new(randomKey,AES.MODE_ECB)

def xor(stringToEncypt, key):

    a = bytes(a ^ b for (a, b) in zip(stringToEncypt, key))
    return a

def aesCBC_encrypt(plaintextBytes, iv):
    blocks = len(plaintextBytes)//16
    ciphertext = bytes()
    for i in range(blocks):

        temp = plaintextBytes[i*16:(i+1)*16]
        xorResult = xor(temp,iv)
        cipher = obj.encrypt(xorResult)
        ciphertext += cipher
        # iv = xorResult
        iv = cipher
    return ciphertext


def aesCBC_decrypt(ciphertext, iv):
    blocks = len(ciphertext)//16
    plaintext = bytes()
    for i in range(blocks):

        temp = ciphertext[i*16:(i+1)*16]
        xorOb = obj.decrypt(temp)
        plaintext += xor(xorOb, iv)
        iv = temp
    return plaintext


def valid_pkcs(text):
    possiblePadding = int.from_bytes(text[-1:],'little')
    if possiblePadding == 0:
        possiblePadding = 16
    val = int.from_bytes(text[-1:], "little")
    if all(elem == val  for elem in text[-possiblePadding:]):
        print(len(text))
        return text[:len(text) - possiblePadding]
    raise Exception("Sorry, invalid padding")

def pkcs7(plaintext, blocksize):
    padding = blocksize - len(plaintext) % blocksize
    pad = chr(padding)
    return ''.join((plaintext, pad*padding))

iv = os.urandom(16)
def encrypt(text):
    text = text.replace(';','').replace(':','')
    prep = "comment1=cooking%20MCs;userdata="
    ap = ";comment2=%20like%20a%20pound%20of%20bacon"

    fullInput = prep + text + ap
    print(fullInput)
    padded = pkcs7(fullInput, blocksize)
    c = aesCBC_encrypt(padded.encode(),iv)
    obj2 = AES.new(randomKey,AES.MODE_CBC,iv)
    c2 = obj2.encrypt(padded.encode())
    print(c)
    print(c2)
    return c2

def decrypt(c):
    plaintext = (aesCBC_decrypt(c,iv))
    if("admin=true".encode() in bytearray(plaintext)):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(plaintext)
    # validatedPlain = valid_pkcs(plaintext)
    validatedPlain = plaintext
    # print(validatedPlain.decode())
    validatedPlain = validatedPlain.decode().replace("%20", " ")
    dict = {}
    # print(validatedPlain)
    dict = {b[0]:b[1] for b in (a.split("=") for a in validatedPlain.split(";"))}
    # print(dict)
    if("admin" in dict and dict["admin"]):
        return True
    return False
    
ciphertext = encrypt("zadminxtrue")
# print()
print("blcoks: " + str(len(ciphertext)//16))
ciphertext = bytearray(ciphertext)
for i in range(256):
    ciphertext[22] = i
    for j in range(256):
        ciphertext[16] = j
        ciphertext = bytes(ciphertext)
        try:
            print(decrypt(ciphertext))
        except Exception as e:
            print(str(e))
            
        ciphertext = bytearray(ciphertext)