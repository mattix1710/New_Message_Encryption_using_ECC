from elliptic_curve import *

#Selecting parameters of encryption (y^2 = x^3 + x + 37 mod 1286081)
curve = Curve(a = 1, b = 37, p = 1286081)
#curve = Curve(a = 7, b = 3, p = 1286081)

#Selecting genration point
curve.set_generator(3, 54588)

# A Private key
na = 11
Pa = na * curve.G

# B Private key
nb = 23 # this is stored in secret
Pb = nb * curve.G

# exchanging Pb, Pa in unsecured network, calculating common key
commonA = na * Pb
commonB = nb * Pa
print(commonA, commonB, commonA == commonB)


def enc(ascii_text, key, p):
  C =[]
  for c in ascii_text:
    m1,m2 = map(lambda x: int(x, 16), list(f'{ord(c):x}'))
    c1 = (m1 + key.x + key.y) % p 
    c2 = m2 + m1 % p
    C.append([c1,c2])
  return C

def dec(encrypted_text, key, p):
  M = []
  for C in encrypted_text:
    c1, c2 = C
    p1 = (c1 - key.x - key.y) % p
    p2 = format((c2 - p1), 'x')
    p1 = format(p1, 'x')
    char = p1+p2
    m = chr(int(char, 16))
    M.append(m)
  return ''.join(M)
  
encoded_message = enc('Hello == Hi', commonA, curve.p)
print(encoded_message)
decoded_message = dec(encoded_message, commonB, curve.p)
print(decoded_message)