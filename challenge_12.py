#! /usr/bin/python3

import os, binascii, random, sys, base64, string
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
    # print("ecb")
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
    # print(bytes(''.join((plaintext, pad*padding)),'utf-8'))
    return ''.join((plaintext, pad*padding))

def randomEncrypt(randomString):

    randomString = str(randomString)
    iv = os.urandom(16)
    randomString = pkcs7(randomString, 16)
    randomString = bytes(randomString, 'utf-8')
    x = random.randint(2,2)
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


def find_block_size():
    current_ctxt = None
    for i in range(2, 20):
        previous_ctxt = current_ctxt or aesECB_encrypt(pkcs7("A"*1,16),21)
        current_ctxt = aesECB_encrypt(pkcs7("A"*i,16),12)
        if previous_ctxt[:16] == current_ctxt[:16]:
            # print("length::::" + str(i-1))
            return i-1
# print(randomKey)
# randomString = os.urandom(16)
# input = sys.argv[1]
input = "AAAAAAAAAAAAAAAA"
# inputLen = len(sys.argv[1])
randomString = bytes(input, 'utf-8')
find_block_size()
decoded = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
# print(obj.block_size)
randomString += decoded
decoded = decoded.decode('utf-8')
# print(randomString)
# cipher = randomEncrypt(randomString)
# print(cipher[:16])
# print(cipher[16:32])
cipher = aesECB_encrypt(pkcs7(input,16),None)
# print(cipher[:16])
# print(cipher[16:32])
# ascii = list(range(ord('a'), ord('z') + 1)) +list(range(ord('A'), ord('Z') + 1)) +[ord(' ')]

paddings = ""
for blocksize in range(16):
    paddings += str(blocksize)

allChars = string.ascii_letters + string.digits + string.punctuation + string.whitespace + string.printable + string.hexdigits + string.whitespace + string.
# allChars = [chr(i) for i in range(127)]
foundChars = ""
for j in range(len(pkcs7(decoded,16))//16):

    for i in range(16):
        dict = {}
        trancatedInput = input[i:len(input) - 1]
        # print("trancatedInput: " + trancatedInput)
        cipher =  aesECB_encrypt(pkcs7(trancatedInput + decoded,16), None)
        ccc = (pkcs7(trancatedInput+decoded,16)[(j*16):(j*16 +16)])
        # print("--------")
        # print(ccc)
        # print(bytes(ccc[len(ccc)-1],'utf-8'))
        # for ch in ccc:
        #     print(ch in allChars)
        for c in allChars:
            # print(c)
            candidate = trancatedInput + foundChars + c
            candidate = candidate[len(candidate) - 16: len(candidate)]
            # print(candidate)
            dict[aesECB_encrypt(candidate, None)] = candidate
        # print(dict)
        # print(dict[cipher[:16]][15])
        # if(len(dict[cipher[(j*16):(j*16 +16)]]) == 16):
        try:
            key = cipher[(j*16):(j*16 +16)]
            foundChars += dict[key][15]
        except:
            print()
print("found text: " + foundChars)
