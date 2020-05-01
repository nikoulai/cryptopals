#! /usr/bin/python3

# Single-byte XOR cipher
# The hex encoded string:
#
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# ... has been XOR'd against a single character. Find the key, decrypt the message.
#
# You can do this by hand. But don't: write code to do it for you.
#
# How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

import sys, binascii

input = sys.argv[1]
# a = byteso
input = bytes.fromhex(input)
ascii = list(range(ord('a'), ord('z') + 1)) +list(range(ord('A'), ord('Z') + 1)) +[ord(' ')]
ratio = 0

for letter in ascii:
    # print(letter)
    xor = bytes(letter ^ a for a in input)
    trues = sum([x in ascii for x in xor])
    if(trues/len(input) > ratio):
        # print("here")
        output = xor
        ratio = trues/len(input)
    # print("\n")
    # if(sum/len(xor) > ratio):
    #     ratio = sum/len(xor)
    #     result = xor
print(output)
# "Cooking MC's like a pound of bacon"
