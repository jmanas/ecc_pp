
ECC - Elliptic Curves
---------------------
Simple implementation.

C= ECC(p, a, b)
	creates a curve, y^2 = x^3 + ax + b (Fp)

P= Point(x, y)
	creates a point

C.valid(P)
	checks whether P belongs to curve C

C.y(x)
	given x, calculate y

C.add(P, Q)
	P + Q

C.mul(k, P)
	k * P

C.neg(P)
	-P

C.npoints()
	number of points in the curve

C.order(P)
	order of P

C.random()
	a random point in the curve

