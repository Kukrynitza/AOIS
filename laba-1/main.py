import math


def binary_to_decimal(binary_list):
    list = binary_list[1:]
    decimal = 0
    length = len(list)

    for i in range(length):
        decimal += list[i] * (2 ** (length - 1 - i))
    if(binary_list[0] == 1):
        decimal = -decimal
    return decimal


def twos_complement_to_decimal(bits):
    BIT_LENGTH = 8
    ORIGIN_BIT_LENGTH = 7
    if len(bits) != BIT_LENGTH:
        raise ValueError("Массив должен содержать ровно 8 элементов")

    if bits[0] == 1:
        inverted_bits = [1 - bit for bit in bits]
        carry = 1
        for i in range(ORIGIN_BIT_LENGTH, -1, -1):
            if inverted_bits[i] == 1 and carry == 1:
                inverted_bits[i] = 0
            elif inverted_bits[i] == 0 and carry == 1:
                inverted_bits[i] = 1
                carry = 0
        value = -sum(inverted_bits[i] * (2 ** (ORIGIN_BIT_LENGTH - i)) for i in range(BIT_LENGTH))
    else:
        value = sum(bits[i] * (2 ** (ORIGIN_BIT_LENGTH - i)) for i in range(BIT_LENGTH))

    return value

def binary_to_decimal_str(binary_str):
    integer_part, fractional_part = binary_str.split('.')

    integer_value = sum(int(bit) * (2 ** (len(integer_part) - 1 - i)) for i, bit in enumerate(integer_part))

    fractional_value = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(fractional_part))

    return integer_value + fractional_value

def addition_bin(first, second):
    result = []
    next = 0
    MAX_LENGTH = 8
    for i in range(MAX_LENGTH - 1, -1, -1):
        count = first[i] + second[i] + next
        next = 0 if count < 2 else 1
        result.append(count % 2)
    result.reverse()
    return result
def to_bin(num, choise):
    direct = []
    if(num >= 0):
        direct.append(0)
    else:
        direct.append(1)
    while num != 0:
        direct.insert(-1, num % 2)
        num = math.trunc(num / 2)
    direct.reverse()
    if len(direct) < 8:
            direct = direct[:1] + [0] * (8 - len(direct)) + direct[1:]
    print('В прямом коде:', direct)
    inverse = []
    additionally = []
    if(direct[0] == 0):
        inverse = direct
        additionally = direct
    else:
        inverse.append(1)
        for element in direct[1:]:
            inverse.append(0 if element == 1 else 1)
        additionally = addition_bin(inverse, [0, 0, 0, 0, 0, 0, 0, 1])
    print('В обратном', inverse)
    print('В дополнителльном', additionally)
    if(choise == 'direct'):
        return direct
    if(choise == 'inverse'):
        return inverse
    if(choise == 'additionally'):
        return additionally

def to_bin_for_subtraction(num):
    BIN_SIZE = 8
    direct = []
    if(num >= 0):
        direct.append(0)
    else:
        direct.append(1)
    while num != 0:
        direct.insert(-1, num % 2)
        num = math.trunc(num / 2)
    direct.reverse()
    if len(direct) < BIN_SIZE:
            direct = direct[:1] + [0] * (BIN_SIZE - len(direct)) + direct[1:]
    inverse = []
    additionally = []
    if(direct[0] == 0):
        inverse = direct
        additionally = direct
    else:
        inverse.append(1)
        for element in direct[1:]:
            inverse.append(0 if element == 1 else 1)
        additionally = addition_bin(inverse, [0, 0, 0, 0, 0, 0, 0, 1])
    return additionally
def compare_binary(a, b):
    while len(a) > 1 and a[0] == 0:
        a.pop(0)
    while len(b) > 1 and b[0] == 0:
        b.pop(0)

    if len(a) != len(b):
        return len(a) > len(b)
    return a >= b

def subtract_binary(a, b):
    a = a[:]
    b = [0] * (len(a) - len(b)) + b
    borrow = 0

    for i in range(len(a) - 1, -1, -1):
        a[i] = a[i] - b[i] - borrow
        if a[i] < 0:
            a[i] += 2
            borrow = 1
        else:
            borrow = 0

    while len(a) > 1 and a[0] == 0:
        a.pop(0)

    return a if a else [0]

def division_bin(dividend, divisor):
    FIVE_RANGE = 5
    if all(bit == 0 for bit in divisor):
        return "Ошибка: Деление на ноль"

    sign = '-' if (dividend[0] != divisor[0]) else ''

    abs_dividend = dividend[1:]
    abs_divisor = divisor[1:]

    quotient = []
    remainder = []

    for bit in abs_dividend:
        remainder.append(bit)
        if compare_binary(remainder, abs_divisor):
            quotient.append(1)
            remainder = subtract_binary(remainder, abs_divisor)
        else:
            quotient.append(0)

    while len(quotient) > 1 and quotient[0] == 0:
        quotient.pop(0)

    quotient.append('.')
    fractional_part = []

    for _ in range(FIVE_RANGE):
        remainder.append(0)
        if compare_binary(remainder, abs_divisor):
            fractional_part.append(1)
            remainder = subtract_binary(remainder, abs_divisor)
        else:
            fractional_part.append(0)

    result = sign + ''.join(map(str, quotient)) + ''.join(map(str, fractional_part))
    return result
def multiplication_bin(first_num, second_num):
    TRUE_BIT_SIZE = 7
    sign = 0 if first_num[0] == second_num[0] else 1
    result = [0,0,0,0,0,0,0,0]
    for i in range(TRUE_BIT_SIZE, 0, -1):
        if(second_num[i] == 0):
            continue
        first = [0] + first_num[1:]
        first = first[(TRUE_BIT_SIZE - i):] + [0] * (TRUE_BIT_SIZE - i)
        result = addition_bin(result, first)
    return [sign] + result[1:]
def float_to_ieee754(num):
    SQUARE_ROOT = 2
    TRUE_BIT_SIZE = 7
    MANTIS_BIT_LENGTH = 23
    MAX_BIT_SIZE = 127
    result = [0]

    integer_part = int(num)
    fractional_part = num - integer_part

    binary = []
    if integer_part == 0:
        binary = ['0']
    while integer_part > 0:
        binary.insert(0, str(integer_part % SQUARE_ROOT))
        integer_part //= SQUARE_ROOT

    binary.append('.')
    for _ in range(MANTIS_BIT_LENGTH):
        fractional_part *= SQUARE_ROOT
        bit = int(fractional_part)
        binary.append(str(bit))
        fractional_part -= bit

    point_pos = binary.index('.')
    first_one_pos = ''.join(binary).replace('.', '').index('1')
    exponent = point_pos - first_one_pos - 1 + MAX_BIT_SIZE

    for i in range(TRUE_BIT_SIZE, -1, -1):
        result.append(1 if exponent & (1 << i) else 0)

    binary_str = ''.join(binary).replace('.', '')
    mantissa_start = first_one_pos + 1
    mantissa = binary_str[mantissa_start:mantissa_start + MANTIS_BIT_LENGTH]
    mantissa = mantissa.ljust(MANTIS_BIT_LENGTH, '0')
    result.extend([int(x) for x in mantissa])

    return result


def ieee754_to_float(ieee):
    MAX_BIT_SIZE = 127
    EXPONENT_SIZE = 9
    BIT_LENGTH = 32
    TWO = 2
    exponent = 0
    for i in range(1, EXPONENT_SIZE):
        exponent = exponent * TWO + ieee[i]
    exponent -= MAX_BIT_SIZE

    mantissa = 1.0
    for i in range(EXPONENT_SIZE, BIT_LENGTH):
        mantissa += ieee[i] * (TWO ** (EXPONENT_SIZE - 1 - i))

    return mantissa * (TWO ** exponent)

def addition_float(first, second):
    first_ieee = float_to_ieee754(first)
    second_ieee = float_to_ieee754(second)

    result = first + second
    return float_to_ieee754(result)

def menu(choise):
    match choise:
        case 1:
            first_num = input('Введите первое число: ')
            first_bin_num = to_bin(int(first_num), 'additionally')

            second_num = input('Введите второе число: ')
            second_bin_num = to_bin(int(second_num), 'additionally')
            result = addition_bin(first_bin_num, second_bin_num)
            print(result)
            return twos_complement_to_decimal(result)
        case 2:
            first_num = input('Введите первое число: ')
            first_bin_num = to_bin(int(first_num), 'additionally')

            second_num = input('Введите второе число: ')
            second_bin_num = to_bin(int(second_num), 'additionally')
            second_bin_num = to_bin_for_subtraction(-int(second_num))

            result = addition_bin(first_bin_num, second_bin_num)
            print(result)
            return twos_complement_to_decimal(result)
        case 3:
            first_num = input('Введите первое число: ')
            first_bin_num = to_bin(int(first_num), 'additionally')

            second_num = input('Введите второе число: ')
            second_bin_num = to_bin(int(second_num), 'additionally')
            result = multiplication_bin(first_bin_num, second_bin_num)
            print(result)
            return binary_to_decimal(result)
        case 4:
            first_num = input('Введите первое число: ')
            first_bin_num = to_bin(int(first_num), 'direct')

            second_num = input('Введите второе число: ')
            second_bin_num = to_bin(int(second_num), 'direct')

            result = division_bin(first_bin_num, second_bin_num)
            print(result)
            return binary_to_decimal_str(result)
        case 5:
            first_num = float(input('Введите первое положительное число: '))
            second_num = float(input('Введите второе положительное число: '))
            if first_num < 0 or second_num < 0:
                return "Числа должны быть положительными"

            result_ieee = addition_float(first_num, second_num)
            print("Результат в IEEE-754:", result_ieee)
            return ieee754_to_float(result_ieee)
        case _:
            return 'Ошибка в выборе'


if __name__ == '__main__':
    choise = input('Введите название операции\n'
                   '1 - сложение в дополнительном коде\n'
                   '2 - вычитание в дополнительном коде\n'
                   '3 - умножение в прямом коде\n'
                   '4 - деление в прямом коде\n'
                   '5 - сложение чисел с плавающей точкой\n'
                   'Ввод: ')
    print(menu(int(choise)))
