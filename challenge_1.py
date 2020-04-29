#!usr/bin/python

# Convert hex to base64
# The string:
#
# 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
# Should produce:
#
# SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
import sys, binascii

arg = sys.argv[1]
# decoded = arg.decode('hex')
decoded = bytes.fromhex(arg)
# print decoded + '\n'
# print base64.b64decode(arg)
print ( binascii.b2a_base64(decoded))
