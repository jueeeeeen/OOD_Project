def prime_formula(plane, ship, train, car, guest): # with all args being 2 : 2278 empty rooms 7-8-9-10-11=55440:11486657580417003599944560
    return (2**guest) * (3**car) * (5**train) * (7**ship) * (11**plane)

def cantor_pairing_formula(plane: int, ship: int, train: int, car: int, guest: int) -> int: # with all args being 2 : 120059 empty rooms
    def cantor_pairing(a: int, b: int) -> int:
        return ((a + b) * (a + b + 1)) // 2 + b
    result = cantor_pairing(plane, ship)
    result = cantor_pairing(result, train)
    result = cantor_pairing(result, car)
    return cantor_pairing(result, guest)

def hilbert_curve(p, s, t, c, g): #32 : no empty room, 7-8-9-10-11=55440:984939
    hilbert_curve = HilbertCurve(p=5, n=5)
    distance = hilbert_curve.distance_from_point([p, s, t, c, g])

    return distance

def gray_code(p, s, t, c, g): # 1082401 rooms
    def _gray_code(n):
        return n ^ (n >> 1)
    return _gray_code(p) | (_gray_code(s) << 5) | (_gray_code(t) << 10) | (_gray_code(c) << 15) | (_gray_code(g) << 20)

def morton_curve(p, s, t, c, g): #32 : none, 7-8-9-10-11=55440:865754
    args = (p, s, t, c, g)
    result = 0
    for i in range(max(x.bit_length() for x in args)):
        for j, num in enumerate(args):
            result |= ((num >> i) & 1) << (i * len(args) + j)
    return result