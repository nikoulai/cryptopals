#! /usr/bin/python3

import sys
from Crypto.Cipher import AES
import string

obj = AES.new("\"provide\" that to the \"attacker\"", AES.MODE_ECB)

def pkcs7(plaintext, blocksize):
    padding = blocksize - len(plaintext) % blocksize
    pad = chr(padding)
    # print(bytes(''.join((plaintext, pad*padding)),'utf-8'))
    return ''.join((plaintext, pad*padding))


def parsing(pars):
    dict = {}
    dict = {b[0]:b[1] for b in (a.split("=") for a in pars.split("&"))}
    print(dict)

def profile_for(email):
    parsedEmail = email.split("&")[0].split("=")[0]
    assert("@" in parsedEmail)
    dict = { "email": parsedEmail, "uid": 10, "role": "user"}
    print(parsedEmail)
    encoded = ""
    encoded = "&".join([key + "=" + str(value) for key,value in dict.items()])
    print(encoded)
    return encoded


parsing("foo=bar&baz=qux&zap=zazzle")
encoded = profile_for("nikos@fds.com&sffsd=fs")
cipher = obj.encrypt(pkcs7(encoded,32))
plaintext = obj.decrypt(cipher)
parsing(plaintext.decode('utf-8'))
print(cipher)

allChars = string.ascii_letters + string.digits + string.punctuation + string.whitespace + string.printable + string.hexdigits + string.whitespace
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
