import math
import boto3

class TempClass():
    def __init__(self):
        self.var = 10

    def exp(self, ctr):
        self.var += math.exp(ctr)

    def ret_var(self):
        return self.var