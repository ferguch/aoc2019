from typing import List, NamedTuple, Tuple

HALT=99
ADD=1
MULT=2
SAVE=3
OUTPUT=4
JUMP_IF_TRUE=5
JUMP_IF_FALSE=6
LT=7
EQ=8

def parse_opcode(opcode: int) -> Tuple[int, List[int]]:
    opcode_part = opcode % 100
    hu_digit = (opcode // 100) % 10
    th_digit = (opcode // 1000) % 10
    tt_digit = (opcode // 10000) % 10
    return (opcode_part, [hu_digit, th_digit, tt_digit])

assert parse_opcode(1002) == (2, [0, 1, 0])

def calc(list : List[int], input: List[int]) -> List:
    list = list[:]
    output = []
    pos = 0

    while list[pos] != 99: # stop
        opcode, modes = parse_opcode(list[pos])
        if opcode == ADD:
            value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            list[list[pos + 3]] = value1 + value2
            pos += 4
        elif opcode == MULT:
            value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            list[list[pos + 3]] = value1 * value2
            pos += 4
        elif opcode == SAVE:
            input_value = input[0]
            input = input[1:]
            list[list[pos + 1]] = input_value
            pos += 2
        elif opcode == OUTPUT:
            value = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            output.append(value)
            pos += 2
        elif opcode == JUMP_IF_TRUE:
            value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 != 0:
                pos = value2
            else:
                pos += 3
        elif opcode == JUMP_IF_FALSE:
            value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 == 0:
                pos = value2
            else:
                pos += 3
        elif opcode == LT:
            value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 < value2:
                list[list[pos + 3]] = 1
            else:
                list[list[pos + 3]] = 0
            pos += 4
        elif opcode == EQ:
            value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 == value2:
                list[list[pos + 3]] = 1
            else:
                list[list[pos + 3]] = 0
            pos += 4
        else:
            raise ValueError(f"Error: {list[pos]}")
    return output

#assert calc([3,0,4,0,99], [1]) == [1]
#assert calc([3,0,4,0,99], [2097]) == [2097]

PROGRAM = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,91,92,225,1102,85,13,225,1,47,17,224,101,-176,224,224,4,224,1002,223,8,223,1001,224,7,224,1,223,224,223,1102,79,43,225,1102,91,79,225,1101,94,61,225,1002,99,42,224,1001,224,-1890,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,102,77,52,224,1001,224,-4697,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1101,45,47,225,1001,43,93,224,1001,224,-172,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,1102,53,88,225,1101,64,75,225,2,14,129,224,101,-5888,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,101,60,126,224,101,-148,224,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1102,82,56,224,1001,224,-4592,224,4,224,1002,223,8,223,101,4,224,224,1,224,223,223,1101,22,82,224,1001,224,-104,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,344,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,107,226,677,224,102,2,223,223,1006,224,374,101,1,223,223,8,677,677,224,102,2,223,223,1006,224,389,1001,223,1,223,1008,226,677,224,1002,223,2,223,1006,224,404,101,1,223,223,7,677,677,224,1002,223,2,223,1005,224,419,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,1108,226,226,224,102,2,223,223,1005,224,449,1001,223,1,223,107,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,479,101,1,223,223,1007,226,677,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,108,226,677,224,1002,223,2,223,1005,224,554,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,569,1001,223,1,223,1107,677,677,224,102,2,223,223,1005,224,584,1001,223,1,223,7,677,226,224,102,2,223,223,1005,224,599,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,614,1001,223,1,223,7,226,677,224,1002,223,2,223,1006,224,629,101,1,223,223,1107,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,226,677,224,102,2,223,223,1006,224,659,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226]
# part 1
print(calc(PROGRAM, [1]))

# part 2
print(calc(PROGRAM, [5]))
