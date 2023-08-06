# encoding: utf-8

from util     import Util
from integral import Integral



class IntegralDiff(object):



    @classmethod
    def area_up(cls, x, y, z, base=0, tol=0.001):

        x = base if x < base else x
        y = base if y < base else y
        z = base if z < base else z

        x, y = min(x, y), max(x, y)

        if Util.isclose(x, y, tol):

            if Util.isclose(z, x, tol):
                return 0
            elif z < x:
                return x-z
            elif z > x:
                return 0

        else:

            if Util.isclose(z, y, tol):
                return 0
            elif Util.isclose(z, x, tol):
                return (y-z) / 2.
            elif z < x:
                return ((x-z) + (y-z)) / 2.
            elif z > x and z < y:
                return (y-z) * ((y-z)/float(y-x)) / 2.
            elif z > y:
                return 0



    @classmethod
    def area_down(cls, x, y, z, base=0, tol=0.001):

        x = base if x < base else x
        y = base if y < base else y
        z = base if z < base else z

        x, y = min(x, y), max(x, y)


        if Util.isclose(x, y, tol):

            if Util.isclose(z, x, tol):
                return 0
            elif z < x:
                return 0
            elif z > x:
                return z-x 

        else:

            if Util.isclose(z, x, tol):
                return 0
            elif Util.isclose(z, y, tol):
                return (z-x) / 2.
            elif z < x:
                return 0
            elif z > x and z < y:
                return (z-x) * ((z-x)/float(y-x)) / 2.
            elif z > y:
                return ((z-x) + (z-y)) / 2.



    @classmethod
    def area_diff(cls, x, y, z, base=0, tol=0.001):
        """ area diff = area up - area down
        """

        return cls.area_up(x, y, z, base, tol) - cls.area_down(x, y, z, tol, base)
        


    @classmethod
    def area_union(cls, x, y, z, base=0, tol=0.001):
        """ area union = area + lost gross
        """

        return Integral.area(x, y, base, tol) + cls.area_down(x, y, z, base, tol)



    @classmethod
    def area_ratio(cls, x, y, z, base=0, tol=0.001):

        pass
