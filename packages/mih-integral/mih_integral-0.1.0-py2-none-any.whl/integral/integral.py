# encoding: utf-8

from util import Util


class Integral(object):


    @classmethod
    def area(cls, x, y, base=0, tol=0.001):

        x = base if x < base else x
        y = base if y < base else y

        x, y = min(x, y), max(x, y)


        if Util.isclose(x, y, tol):

            if Util.isclose(x, base):
                return 0
            else:
                return x-base
        
        else:

            if Util.isclose(x, base):
                return (y-x) / 2.
            else:
                return (x-base) + ((y-x)/2.)
