from random import randint
from collections import namedtuple

def inv(x, p):
    """ inverse of x """
    return pow(x, p - 2, p)

Point = namedtuple("Point", "x y")

# The point at infinity 
O = 'Origin'

class ECC:
    def __init__(self, _p, _a, _b):
        assert (4 * _a**3 + 27 * _b**2) % _p != 0
        self.p= _p;
        self.a= _a;
        self.b= _b;

    def valid(self, P):
        """ If P is on the curve """
        if P == O:
            return True

        p= self.p
        a= self.a
        b= self.b

        left = (P.y * P.y) % p
        right = (P.x ** 3 + a * P.x + b) % p
        return left == right

    def neg(self, P):
        """ inverse of point P """
        if P == O:
            return O
        return Point(P.x, (-P.y) % self.p)

    def add(self, P, Q):
        """ P + Q """
        assert self.valid(P) and self.valid(Q)

        # Deal with the special cases where either P, Q, or P + Q is
        # the origin
        if P == O:
            return Q
        if Q == O:
            return P
        if Q == self.neg(P):
            return O

        p= self.p
        a= self.a
    
        # Cases not involving the origin
        if P.x == Q.x:
            dydx = (3 * P.x ** 2 + a) * inv(2 * P.y, p)
        else:
            dydx = (Q.y - P.y) * inv(Q.x - P.x, p)
        x = (dydx ** 2 - P.x - Q.x) % p
        y = (dydx * (P.x - x) - P.y) % p
        return Point(x, y)

    def mul(self, k, P):
        """ k * P """
        assert self.valid(P)

        if P == O:
            return O

        if k < 0:
            # k * P = -k * (-P)
            return self.mul(-k, self.neg(P))

        result = O
        part = P
        while k:
            if k & 1:
                result = self.add(result, part)
            part = self.add(part, part)
            k >>= 1
        return result

    def y(self, x):
        """ y coordinate for x """
        p= self.p
        a= self.a
        b= self.b
        yy= self._sqrt((x ** 3 + a * x + b) % p)
        if yy == 0: assert self.valid(Point(x, yy))
        return yy

# https://eli.thegreenplace.net/2009/03/07/computing-modular-square-roots-in-python
    def _sqrt(self, a):
        """ a quadratic residue (mod p) of a """

        p= self.p

        if self._legendre_symbol(a) != 1:
            return 0
        if a == 0:
            return 0
        if p == 2:
            return 0
        if p % 4 == 3:
            return pow(a, (p + 1) // 4, p)

        s = p - 1
        e = 0
        while s % 2 == 0:
            s //= 2
            e += 1

        n = 2
        while self._legendre_symbol(n) != -1:
            n += 1

        x = pow(a, (s + 1) // 2, p)
        b = pow(a, s, p)
        g = pow(n, s, p)
        r = e

        while True:
            t = b
            m = 0
            for m in range(r):
                if t == 1:
                    break
                t = pow(t, 2, p)

            if m == 0:
                return x

            gs = pow(g, 2 ** (r - m - 1), p)
            g = (gs * gs) % p
            x = (x * gs) % p
            b = (b * g) % p
            r = m


    def _legendre_symbol(self, a):
        """ Legendre symbol """
        p= self.p
        ls = pow(a, (p - 1) // 2, p)
        if ls == p - 1:
            return -1 
        return ls

    def random(self):
        """ a random point in the curve """
        try:
            x = randint(1, self.p - 1)
            y = self.y(x)
            p= self.p
            if randint(0, 1) == 0:
                y = (p - y) % p
            return Point(x, y)
        except AssertionError:
            return self.random()

    # naive
    def order(self, P):
        """ order of P """
        assert self.valid(P)
        k= 1
        kP= P
        while kP != O:
            k+= 1
            kP = self.add(kP, P)
        return k

    # naive
    def npoints(self):
        """ number of points in the curve """
        total= 1;   # O
        for x in range(self.p):
            try:
                y = self.y(x)
                if y == 0:
                    total+= 1
                else:
                    total+= 2
            except:
                pass
        return total

