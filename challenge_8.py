#! /usr/bin/python3
import binascii

file = open("8.txt", 'r')
lines = [bytes.fromhex(line.strip()) for line in file]


for line in lines:
    blocksNum = len(line)//16
    # print(blocks)
    blocks = []
    for i in range(blocksNum):
        blocks.append(line[i*16:(i+1)*16])
    blocks = list(dict.fromkeys(blocks))
    if(len(blocks)!=blocksNum):
        print(line)
