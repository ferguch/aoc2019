from typing import List, NamedTuple, Tuple
import itertools

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

class Instruction(NamedTuple):
    opcode: int
    arguments: List[int]
    param_modes: List[int]


def calc(list : List[int], input: List[int]) -> List[int]:
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


def run_amp(program: List[int], input_signal: int, phase: int) -> List[int]:
    inputs = [phase, input_signal]
    outputs = calc(program, inputs)
    return outputs

def run_program(program: List[int], phases: List[int]) -> int:
    output = 0
    for phase in phases:
        temp = run_amp(program, output, phase)
        output = temp.pop()

    return output

PROGRAM = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
PHASES = [4,3,2,1,0]
OUTPUT_SIGNAL = 43210

assert run_program(PROGRAM, PHASES) == OUTPUT_SIGNAL
assert run_program([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]) == 54321
assert run_program([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]) == 65210

def best_program(program: List[int]) -> int:
    max = 0
    for phases in itertools.permutations(range(5)):
        output = run_program(program, phases)
        print("phases: " + str(phases) + " -> " + str(output))
        max = output if output > max else max
    return max

assert best_program([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321
assert best_program([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210

with open("day7_input", "r") as f:
    lines = [int(x) for x in f.readline().split(",")]
print(best_program(lines))