# encoding: utf-8


class Util(object):


    @classmethod
    def isclose(cls, x, y, tol=0.001):
        return abs(x-y) <= tol  
