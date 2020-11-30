from functools import reduce

def pkcs7(plaintext, blocksize):
    padding = blocksize - len(plaintext) % blocksize
    pad = chr(padding)
    # print(bytes(''.join((plaintext, pad*padding)),'utf-8'))
    return ''.join((plaintext, pad*padding))



text = pkcs7("ICE ICE BABY",16).encode()
text2 = b"ICE ICE BABY\x05\x05\x05\x05"
text3 = b"ICE ICE BABY\x01\x03\x02\x03"

# candidatePadding = 0
# count  = 0
blocksize = 16
# for c in text:
#     print(c)
#     if c < blocksize - 1:
#         if count == 0:
#             candidatePadding = c
#             count+=1
#         elif c == candidatePadding:
#             count +=1
#         else:
#             break
#             # raise Exception("Sorry, invalid padding")
# if(count == candidatePadding):
#     print(text[0:len(text) - count])
# else:
#     print("count: " + str(count) + " candidate: " + str(candidatePadding))
#     raise Exception("Sorry, invalid padding")
def valid_pkcs(text):
    possiblePadding = int.from_bytes(text[-1:],'little')
    if possiblePadding == 0:
        possiblePadding = 16
    val = int.from_bytes(text[-1:], "little")
    if all(elem == val  for elem in text[-possiblePadding:]):
        print(len(text))
        return text[:len(text) - possiblePadding]
    raise Exception("Sorry, invalid padding")
    

print(valid_pkcs(text3))