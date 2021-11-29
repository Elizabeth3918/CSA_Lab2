"""
Coded by Elizabeth Laba
K-20
"""
import numpy as np
import os
BITNESS = 26  # битность чисел
REGISTERS_COUNT = 4  # Количество регистров

A = 0  # Аккумулятор
REGISTERS = np.zeros(REGISTERS_COUNT, dtype=np.int32)  # Регистры


PS = 0  # регістр лічильника статусу(знак)
PC = 0  # регістр лічильника команд
TC = 0  # регістр лічильника тактів


def to_int(value, bitness):
    return value + (1 << bitness - 1)


def from_int(value , bitness):
    return value - (1 << bitness - 1)


def _to_bit(val):
    return int(bool(val))


def _str_bits(val , bits , end="\n") :
    res = ""
    for i in range(bits - 1 , -1 , -1) :
        if i % 8 == 7 :
            res += " "
        res += str(_to_bit(val & (1 << i)))
    return res


def add_mod_2(a, b):
    temp = 0
    for i in range((BITNESS + 8) // 8):
        temp <<= 8
        for j in range(8):
            temp |= b & (1 << j)

    temp_res = a ^ temp

    res = 0
    for i in range(0, BITNESS):
        res |= temp_res & (1 << i)
    return res


def upd_sign():
    global PS , A
    PS = _to_bit(A & (1 << BITNESS - 1))


def prepare_move(operand):
    global A, REGISTERS, PS, PC, TC

    TC += 1

    if operand.startswith("R"):
        register_index = int(operand[1:])
        A = REGISTERS[register_index]

    elif (operand.startswith("-") and operand[1:].isdigit()) or operand.isdigit() :
        literal = to_int(int(operand) , BITNESS)  # переводим число в 26 бит
        A = literal

    else:
        raise ValueError(f"Invalid command syntax: MOVE {operand}")


def prepare_save(operand) :
    global A , REGISTERS , PS , PC , TC

    TC += 1

    if not operand.startswith("R") :
        raise ValueError(f"Invalid command syntax: SAVE {operand}")

    register_index = int(operand[1 :])  # переводим индекс регистра в целое
    REGISTERS[register_index] = A  # перетаскиваем с аккумулятора в регистр


def prepare_add(operand) :
    global A , REGISTERS , PS , PC , TC

    TC += 1

    if operand.startswith("R") :
        register_index = int(operand[1 :])
        A = add_mod_2(A , REGISTERS[register_index])

    elif operand == "A" :
        A = add_mod_2(A , A)

    elif (operand.startswith("-") and operand[1 :].isdigit()) or operand.isdigit() :
        literal = to_int(int(operand) , BITNESS)
        A = add_mod_2(A , literal)

    else :
        raise ValueError(f"Invalid command syntax: ADD {operand}")


def do_command(str_cmd):
    global A , REGISTERS , PS , PC , TC

    TC = 0
    PC += 1

    operator , operand , *_ = str_cmd.split()
    operator = operator.lower().strip()
    operand = operand.strip()

    print(f"Current command: {operator} {operand}")
    TC += 1
    info()
    print()

    if operator == "move":
        prepare_move(operand)

    elif operator == "save":
        prepare_save(operand)

    elif operator == "add":
        prepare_add(operand)

    upd_sign()


def info() :
    global A , REGISTERS , PS , PC , TC
    print("Info:")

    print(f"A:\t{_str_bits(A , BITNESS)} | {from_int(A , BITNESS)}")
    for i , register_data in enumerate(REGISTERS) :
        print(f"R{i}:\t{_str_bits(register_data , BITNESS)} | {from_int(register_data , BITNESS)}")

    if PS == 1 :
        sign = "+"
    else :
        sign = "-"
    print(f"PS:\t{sign}")
    print(f"PC:\t{PC}")
    print(f"TC:\t{TC}")


def main():
    rows = None
    with open("commands.txt", "r") as file:
        rows = file.readlines()
    for row in rows:
        if not row.isspace():
            os.system("cls")
            print(row.strip())
            do_command(row)
            info()
            os.system("pause")


if __name__ == "__main__" :
    main()