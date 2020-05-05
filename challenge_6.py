#! /usr/bin/python3
import binascii

file = open("6.txt", 'r')
lines = binascii.a2b_base64(file.read())
ascii = list(range(ord('a'), ord('z') + 1)) +list(range(ord('A'), ord('Z') + 1)) +[ord(' ')]
# print(lines)

string1 = "this is a test"
string2 = "wokka wokka!!!"
# print(bytes(string1,""))
# print(sum([abs(ord(a)-ord(b)) for (a,b) in zip(string1, string2)]))
# print(string1.encode())
# int1 = int.from_bytes(string1.encode(),'big')
# int2 = int.from_bytes(string2.encode(),'big')
# print(bin(int1).count("1"))
# print(bin(int1^int2).count("1"))
def HammingDistance(string1, string2):
    int1 = int.from_bytes(string1,'big')
    int2 = int.from_bytes(string2,'big')
    # print(bin(int1).count("1"))
    return bin(int1^int2).count("1")

# line1 = Lines[0].strip()
# print(line1)
distances = []
for keysize in range(2,41):
        # print(line1)
        string1 = lines[0:keysize]
        string2 = lines[keysize:2*keysize]
        normalizedDistance = HammingDistance(string1, string2)/keysize
        normalizedDistance2 = HammingDistance(lines[keysize*2:keysize*3], lines[keysize*3:keysize*4])/keysize
        dist = (normalizedDistance + normalizedDistance2)/2
        distances.append([dist, keysize])

# for keysize in range(len(distances)):
#     print(distances[keysize])

distances.sort(key=lambda x :x[0])

for keysize in range(len(distances)):
    print(distances[keysize])

blocks = []
for i in range(0, 6):
    print("--------")
    keysize = distances[i][1]
    # print(keysize)
    blocks.clear()
    for key in range(keysize):
        # print("key :" + str(key))
        blocks.append([])
    for lineIndex in range(len(lines)):
        # print(lines[lineIndex])
        blocks[lineIndex%keysize].append(lines[lineIndex])
    # print(len(line)/keysize)

    # for key in range(keysize):
    #     print(blocks[key])
    fullKey = ""
    for blockIndex in range(keysize):
        input = blocks[blockIndex]
        ratio = 0
        key = 0
        for letter in ascii:
            # print(letter)
            xor = bytes(letter ^ a for a in input)
            trues = sum([x in ascii for x in xor])
            if(trues/len(input) > ratio):
                # print("here")
                output = xor
                ratio = trues/len(input)
                key = letter
            # print("\n")
            # if(sum/len(xor) > ratio):
            #     ratio = sum/len(xor)
            #     result = xor
        # print(output)
        # print(chr(key))
        fullKey += chr(key)
    print(str(distances[i][1]) + " "+ fullKey)
