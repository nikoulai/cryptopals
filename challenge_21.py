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
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908B0DF
        self.u = 11
        self.s = 7
        self.b = 0x9D2C5680
        # self.d = 5555555555555555
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.f = 1812433253
        self.d = 0xFFFFFFFF
        self.MT = [0 for i in range (self.n)]
        self.index = self.n + 1
        self.seed = seed
        self.lower_mask = 0xFFFFFFFF
        self.upper_mask = 0x00000000
        self.seed_mt(seed)

    #Initialize the generator from a seed
    def seed_mt(self, seed):

        # self.index = self.n
        self.MT[0] = seed

        for i in range(1,self.n):
            # MT[i] := lowest w bits of (f * (MT[i-1] xor (MT[i-1] >> (w-2))) + i)
            temp = (self.f* (self.MT[i - 1] ^ (self.MT[i-1] >> (self.w-2))) + i) & self.lower_mask

            self.MT[i] = temp
        print(self.MT)

    def extract_number(self):

        if self.index >= self.n:
            # if self.index > self.n:
                # raise Exception("Generator was never seeded")

            self.twist()
        
        print(self.MT) 
        y = self.MT[self.index]

        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ (y >> self.l)

        self.index = (self.index + 1) 
        return y  & self.lower_mask

    # Generate the next n values from the series x_i 
    def twist(self):
        print("inside twist")
        
        print(len(self.MT))
        for i in range(self.n-1):
            # print("i :" + str(i))
            # print(len(self.MT))
            # x = (self.MT[i] & self.UPPER_MASK) + (self.MT[i+1] % self.n & self.LOWER_MASK)
            x = (self.MT[i] & self.w) + ((self.MT[i+1] % self.n ) & (self.w-1))
            # self.MT[i] = self.MT[(i + 397) % n] ^ ()

            xA = x >> 1
            if (x % 2) != 0:
                # xA = xA ^ 0x9908b0df 
                xA = xA ^ self.a 
        
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

mers = Mersenne(123)
print(mers.extract_number())