# ------- MAIN --------
from tinyec import registry
from elliptic_curve import *

curr = registry.get_curve('secp192r1')        

curve = Curve(curr.a, curr.b, curr.field.p)
curve.set_generator(curr.g.x, curr.g.y)
print("-- CYCLIC GROUP --")
for it in range(10):
    print(it, curve.G*it)