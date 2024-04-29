import random

#Parameters of the elliptic curve
a = 0
b = 7
#Base point
G = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 
     32670510020758816978083085130507043184471273380659243275938904335757337482424)

#Modulo
myModulo = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1

#Order of curve group
orderOfCurve = 115792089237316195423570985008687907852837564279074904382605163141518161494337

#Add two points on the elliptic curve
def addPoints(point1, point2, m):
    x1, y1 = point1
    x2, y2 = point2
    
    if x1 == x2 and y1 == y2:
        beta = (3 * x1 * x2 + a) * pow(2 * y1, -1, m)
    else:
        beta = (y2 - y1) * pow(x2 - x1, -1, m)
    
    x3 = (beta**2 - x1 - x2) % m
    y3 = (beta * (x1 - x3) - y1) % m
    
    return x3, y3

#double and add points using binary method
def doubleAddMethod(G, k, m):
    targetPoint = G
    kBinary = bin(k)[2:] # Convert k to binary
    
    for bit in kBinary[1:]:  # Starting from the second bit
        targetPoint = addPoints(targetPoint, targetPoint, m)
        
        if bit == "1":
            targetPoint = addPoints(targetPoint, G, m)
    
    return targetPoint

#Private keys for both parties
privateKey1 = random.getrandbits(256)
privateKey2 = random.getrandbits(256)

#Public keys for both parties
publicKey1 = doubleAddMethod(G, privateKey1, myModulo)
publicKey2 = doubleAddMethod(G, privateKey2, myModulo)

# Shared keys for both parties
sharedKey1 = doubleAddMethod(publicKey2, privateKey1, myModulo)
sharedKey2 = doubleAddMethod(publicKey1, privateKey2, myModulo)

#Checks that both parties have the same shared key
assert sharedKey1 == sharedKey2

print("Person 1's private key:", privateKey1)
print("Person 2's private key:", privateKey2)
print("Person 1's public key:", publicKey1)
print("Person 2's public key:", publicKey2)
print("Person 1's shared key:", sharedKey1)
print("Person 2's shared key:", sharedKey2)
