#!/use/bin/python

# Fixed XOR
# Write a function that takes two equal-length buffers and produces their XOR combination.
#
# If your function works properly, then when you feed it the string:
#
# 1c0111001f010100061a024b53535009181c
# ... after hex decoding, and when XOR'd against:
#
# 686974207468652062756c6c277320657965
# ... should produce:
#
# 746865206b696420646f6e277420706c6179

import sys,base64, binascii

a = sys.argv[1]
b = sys.argv[2]
# print(a.decode('hex'))
print(b)
# a = a.decode('hex')
a = bytes.fromhex(a)
b = bytes.fromhex(b)
# b = bytes(b)
result = bytes(c^d for (c,d) in zip(a,b))
# for (c,d) in zip(a,b):
    # print(bytes(ord(c)^ord(d)))
print(binascii.hexlify(result))
