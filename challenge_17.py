import os, binascii, random, sys, base64, string
from Crypto.Cipher import AES
from functools import reduce

possibleStrigs = [
"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=" ,
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ28va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]
randomKey = os.urandom(16)
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

blocksize = 16

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
    print("padding : " + str(padding))
    # if padding == 16:
    #     return plaintext
    pad = chr(padding % 16)
    return ''.join((plaintext, pad*padding))


def firstFunction():
    randomNumber = random.randint(0,len(possibleStrigs) - 1)
    # randomNumber = 1
    randomString = possibleStrigs[randomNumber]
    string = binascii.a2b_base64(randomString)
    print(string)
    print(len(string))
    string = pkcs7(string.decode(),16)
    print(string)
    iv = os.urandom(16)
    ciphertext = aesCBC_encrypt(string.encode(),iv)
    return (ciphertext, iv)

def secondFunction(ciphertext):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:len(ciphertext)]
    plain = aesCBC_decrypt(ciphertext, iv)
    # print(plain)
    try:
        valid_pkcs(plain)
        print("plain")
        print(plain)
        print("plain")
        return True
    except:
        return False

def oracleAttack():
    ciphertext, iv = firstFunction()
    ciphertext = iv + ciphertext
    # for i in range(len(ciphertext)):
    cipher = list(ciphertext)
    # Not by reference
    c = ciphertext[:]
    print(c)
    plaintext  = []
    count = 0
    for l in range (len(ciphertext) // 16 - 1):
        # lst = lst[:len(lst)-n]
        ciphertext = cipher[:len(cipher) - 16 * l]
        c = ciphertext[:]
        for i in range(0,256):
                # print(c) 
                c[-17] = i 
                # print(c)
                result = secondFunction(bytes(c))
                if(result):
                    # print("i = " + str(i))
                    count += 1
                    if i == ciphertext[-17]:
                        continue
                    # print(i)
                    # print(c[-1])
                    # print(bytearray(ciphertext)[-1])
                    # print(ciphertext[-17])
                    # print(c[-17])
                    interm = list(xor([c[-17]],[1]))
                    res = xor([ciphertext[-17]],interm)
                    # print(res)
                    plaintext.append(res)

        print(plaintext)
        print(interm)
        for pad in range(2,17):
            for j in range(1,pad): 
                c[-j - 16] = int.from_bytes(xor([interm[j - 1]], [pad]), "little")
                # print([interm[j-1]])
            for i in range(256):
                c[-pad-16] = i
                # print(c)
                # i = xor([ciphertext[-pad:]],plaintext[-pad:])
                    # c[-j] = xor(xor(bytearray(bytes([pad])),[plaintext[-j]]),[c[-j]])
                result = secondFunction(bytes(c))
                if(result):
                    interm.append(int.from_bytes(xor([c[-pad -16]],[pad]),"little"))
                    res = xor([ciphertext[-pad - 16]],[interm[-1]])
                    # print(res)
                    plaintext.append(res)
    
    print("plaintext")
    plaintext.reverse()
    print(plaintext)
    print(b''.join(plaintext).decode('utf-8'))

oracleAttack()