import general

# polynum - polynomial number

def degree_polynomial_math(polynomial):
    return polynomial.bit_length() - 1

def polynum2bits(num, length=None):
    if not length is None and num.bit_length() < length:
        bits = [0] * (length - num.bit_length)
    else:
        bits = []
    bits += list(map(int, bin(num)[2::]))
    return bits

def bits2num(bits):
    two_pow = 1
    num = 0
    for i in range(len(bits) - 1, -1, -1):
        if bits[i]:
            num += two_pow
        two_pow = two_pow << 1
    return num

def multiply_polynum(multipliable, multiplier):
    result = 0; shift = 0
    while multiplier != 0:
        if multiplier & 1:
            result ^= multipliable << shift

        multiplier = multiplier >> 1
        shift += 1
    return result

def remainder_polynum(divisible, divider):
    if divider == 0:
        raise ValueError("Деление на ноль запрещено")
    while divisible.bit_length() > divider.bit_length():
        shift = divisible.bit_length() - divider.bit_length()
        divisible = divisible ^ (divider << shift)
    return divisible



if __name__ == "__main__":
    print(polynum2bits(multiply_polynum(8, 3)))

    print(general.remainder_polynomials([1, 0, 0, 1, 0, 1, 1, 1, 1], [0, 1, 1]))
    print(remainder_polynum(459, 0))
