#! /usr/bin/env python3
"""
Module for all gerometry tools
"""

class Point():
    """
    the class of a point in pyhack
    """
    def __init__(self, ordo, absc):
        self.absc = absc
        self.ordo = ordo
    def __eq__(self, otherPoint):
        if  not isinstance(otherPoint, Point):
            return False
        return self.absc == otherPoint.absc and self.ordo == otherPoint.ordo
    def __le__(self, otherPoint):
        return self.absc <= otherPoint.absc and self.ordo <= otherPoint.ordo
    def __ge__(self, otherPoint):
        return self.absc >= otherPoint.absc and self.ordo <= otherPoint.ordo
    def __add__(self, scalar):
        return Point(self.absc+scalar, self.ordo+scalar)
    def __mul__(self, scalar):
        return Point(self.absc*scalar, self.ordo*scalar)
    def __sub__(self, scalar):
        return Point(self.absc-scalar, self.ordo-scalar)
    def __str__(self):
        return "{"+str(self.ordo)+":"+str(self.absc)+"}\n"
    def __hash__(self):
        return hash((self.ordo, self.absc))
    def addpointx(self, scalar):
        """
        add a scalar to self.absc
        """
        return Point(self.ordo, self.absc+scalar)
    def addpointy(self, scalar):
        """
        add a scalar to self.ordo
        """
        return Point(self.ordo+scalar, self.absc)
    def addpointxy(self, scalarabsc, scalarordo):
        """
        add two scalar for absc and ordo
        """
        return Point(self.ordo+scalarordo, self.absc+scalarabsc)
    def distance_to(self, other):
        """
        return distance between self and other
        """
        assert isinstance(other, Point)
        return (self.absc-other.absc)*(self.absc-other.absc)+\
            (self.ordo-other.ordo)*(self.ordo-other.ordo)

    def is_in_voisinage(self, other):
        """
        return true if the point1 is near point2
        """
        return self.distance_to(other) == 1.0
