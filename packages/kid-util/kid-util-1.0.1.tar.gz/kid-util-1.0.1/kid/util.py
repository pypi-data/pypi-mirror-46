# Based on https://no.wikipedia.org/wiki/KID-nummer
# Length 2 to 25, using either MOD10 or MOD11


def make(value, mode='MOD10'):
    if mode.upper() == 'MOD10':
        return make_mod10(value)
    elif mode.upper() == 'MOD11':
        return make_mod11(value)


def make_mod10(value):
    return str(value) + str(make_mod10_control_digit(value))


def make_mod11(value):
    return str(value) + str(make_mod11_control_digit(value))


# While this could be made more dense, maybe this has some hope of being readable
def make_mod10_control_digit(value):
    validate_length(value)
    number = int(value)
    digits = list(str(number))
    multiplicands = [2, 1]
    index = 0
    total = 0

    for digit in reversed(digits):
        multiplicand = multiplicands[index % len(multiplicands)]
        result = int(digit) * multiplicand
        total += sum_of_digits(result)
        index += 1

    control = 10 - (total % 10)

    if control == 10:
        return 0
    return control


# While this could be made more dense, maybe this has some hope of being readable
def make_mod11_control_digit(value):
    validate_length(value)
    number = int(value)
    digits = list(str(number))
    multiplicands = [2, 3, 4, 5, 6, 7]
    index = 0
    total = 0

    for digit in reversed(digits):
        multiplicand = multiplicands[index % len(multiplicands)]
        result = int(digit) * multiplicand
        total += result
        index += 1

    control = 11 - (total % 11)

    if control == 11:
        return 0
    if control == 10:
        return '-'
    return control


def verify(value, mode='MOD10'):
    if mode.upper() == 'MOD10':
        return verify_mod10(value)
    elif mode.upper() == 'MOD11':
        return verify_mod11(value)


def verify_mod10(value):
    generated = make_mod10(value[:-1])
    return value == generated


def verify_mod11(value):
    generated = make_mod11(value[:-1])
    return value == generated


def validate_length(value):
    if len(value) < 1 or len(value) > 24:
        raise ValueError('Invalid KID length. Must be from 2 to 25 characters, with control digit.')


# https://stackoverflow.com/a/14940026
def sum_of_digits(n):
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r
