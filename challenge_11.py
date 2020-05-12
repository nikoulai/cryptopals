#! /usr/bin/python3

import os, binascii, random, sys
from Crypto.Cipher import AES
# from random import randrange


randomKey = os.urandom(16)
obj = AES.new(randomKey,AES.MODE_ECB)

def encrypt(stringToEncypt, key):

    a = bytes(a ^ b for (a, b) in zip(stringToEncypt, key))
    return a


def aesCBC_encrypt(plaintextBytes, iv):
    print("cbc")
    blocks = len(plaintextBytes)//16

    ciphertext = bytes()
    for i in range(blocks):

        temp = plaintextBytes[i*16:(i+1)*16]
        xorResult = encrypt(temp,iv)
        cipher = obj.encrypt(xorResult)
        ciphertext += cipher
        iv = xorResult
        return ciphertext


def aesCBC_decrypt(ciphertext, iv):
    blocks = len(ciphertext)//16
    plaintext = bytes()

    for i in range(blocks):

        temp = ciphertext[i*16:(i+1)*16]
        # print(type(temp))
        xor = obj.decrypt(temp)
        plaintext += encrypt(xor, iv)
        iv = temp
        return plaintext


def aesECB_encrypt(ciphertext, iv):
    print("ecb")
    # obj = AES.new(key, AES.MODE_ECB)
    return obj.encrypt(ciphertext)

    # print(plaintext)


def aesECB_decrypt(ciphertext, iv):
    # obj = AES.new(key, AES.MODE_ECB)
     return obj.decrypt(ciphertext)
    # print(plaintext)

def pkcs7(plaintext, blocksize):
    padding = blocksize - len(plaintext) % blocksize
    pad = chr(padding)
    return ''.join((plaintext, pad*padding))

def randomEncrypt(randomString):

    randomString = str(os.urandom(random.randint(5,10)) + randomString + os.urandom(random.randint(5,10)))
    iv = os.urandom(16)
    randomString = pkcs7(randomString, 16)
    randomString = bytes(randomString, 'utf-8')
    x = random.randint(1,2)
    ciphertext = aesCBC_encrypt(randomString,iv) if x==1 else aesECB_encrypt(randomString,iv)
    return ciphertext


def detectECB(ciphertext):
    blocksNum = len(ciphertext)//16
    blocks = []
    for i in range(blocksNum):
        blocks.append(ciphertext[i*16:(i+1)*16])

    blocks = list(dict.fromkeys(blocks))
    if(len(blocks) != blocksNum):
        print("ECB DETECTED")

# print(randomKey)
# randomString = os.urandom(16)
randomString = bytes(sys.argv[1], 'utf-8')
detectECB(randomEncrypt(randomString))
