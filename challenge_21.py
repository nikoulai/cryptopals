# Implement the MT19937 Mersenne Twister RNG
# DOI 10.1109/AHS.2009.11

class Mersenne:

    def reverse_mask(self, x):
        x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
        x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
        x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
        x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
        x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
        return x


    
    def __init__(self, seed):
        self.w = 64
        self.n = 312
        self.m = 156
        self.r = 31
        self.a  = 0xB5026F5AA96619E9
        self.u = 29
        self.d = 5555555555555555
        self.s= 17
        self.b = 0x71D67FFFEDA60000
        self.t = 37
        self.c = 0xFFF7EEE00000000016
        self.l = 43
        self.f = 1812433253
        self.MT = []
        self.index = self.n + 1
        self.LOWER_MASK = ( 1 << self.r) - 1 # That is, the binary number of r 1's
        self.UPPER_MASK = self.reverse_mask(self.LOWER_MASK) # & self.w #  const int upper_mask = lowest w bits of (not lower_mask)   f = 1812433253
        self.lower_mask = (1 << 31)-1
        self.upper_mask = 1 << 31
        print("LOWER" + str(self.LOWER_MASK))
        print("UPPER" + str(self.UPPER_MASK))
        print("lower" + str(self.lower_mask))
        print("upper" + str(self.upper_mask))
        print(bin(self.UPPER_MASK))
        print(bin(self.w))
        print(bin(self.UPPER_MASK & self.w))
        print(self.UPPER_MASK)
        print(1<<31)
        # self.upper_mask=
        
        self.seed_mt(seed)

    



    #Initialize the generator from a seed
    def seed_mt(self, seed):

        self.index = self.n
        self.MT.append(seed)

        for i in range(1,self.n):
            # MT[i] := lowest w bits of (f * (MT[i-1] xor (MT[i-1] >> (w-2))) + i)
            temp = (self.f* (self.MT[i - 1] ^ (self.MT[i-1] >> (self.w-2))) + i) & self.w
            self.MT.append(temp)

        print(self.MT)

    def extract_number(self):

        if self.index >= self.n:
            if self.index > self.n:
                raise Exception("Generator was never seeded")

            self.twist()
        
        y = self.MT[self.index]

        print(str(y) + "\n")
        y = y ^ ((y >> self.u) )#& self.d)
        print(str(y) + "\n")
        y = y ^ ((y << self.s) )#& self.b)
        print(str(y) + "\n")
        y = y ^ ((y << self.t) )#& self.c)
        print(str(y) + "\n")
        y = y ^ (y >> self.l)
        print(str(y) + "\n")

        self.index += 1
        return y  #& self.w

    # Generate the next n values from the series x_i 
    def twist(self):
        
        for i in range(self.n - 1):
            # print("i :" + str(i))
            # print(len(self.MT))
            # x = (self.MT[i] & self.UPPER_MASK) + (self.MT[i+1] % self.n & self.LOWER_MASK)
            x = (self.MT[i] ) + (self.MT[i+1] % self.n )

            xA = x >> 1
            if (x % 2) != 0:
                # xA = xA ^ 0x9908b0df 
                xA = xA ^ self.a 
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        
        self.index = 0

mers = Mersenne(1)
print(mers.extract_number())
print(bin(mers.reverse_mask(1)))