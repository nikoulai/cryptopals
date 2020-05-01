#! /usr/bin/python3

ascii = list(range(ord('a'), ord('z') + 1)) +list(range(ord('A'), ord('Z') + 1)) +[ord(' ')]
def bestInLine(input):
    # input = sys.argv[1]
# a = byteso
    input = bytes.fromhex(input)
    ratio = 0

    for letter in range(2**8):
        # print(letter)
        xor = bytes(letter ^ a for a in input)
        numOfTrues = sum([x in ascii for x in xor])
        wordRatio = numOfTrues/len(input)
        if(wordRatio > ratio):
            # print("here")
            output = xor
            ratio = wordRatio
        # print("\n")
        # if(sum/len(xor) > ratio):
        #     ratio = sum/len(xor)
        #     result = xor
    # print(output)
    return output

file = open("4.txt",'r')
Lines = file.readlines()

strings = []
ratio = 0
for line in Lines:
    # print(type(line))
    xor = bestInLine(line.strip())
    trues = sum([x in ascii for x in xor])
    if(trues/len(line.strip()) > ratio):
        # print("here")
        output = xor
        ratio = trues/len(line.strip())
print(output)
