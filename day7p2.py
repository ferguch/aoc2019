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

def calc(list : List[int], input: List[int], pos: int) -> List[int]:
    list = list[:]
    output = []
    #pos = 0

    while True:
        opcode, modes = parse_opcode(list[pos])
        print(pos, input, opcode, modes)
        if opcode == 99:  # stop
            return None
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
            return output, pos
            #value = self.get_value(self.pos + 1, modes[0])
            #self.pos += 2
            #return value
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

def run_amp(program: List[int], input_signal: int, phase: int, pos: int) -> List[int]:
    inputs = [phase, input_signal]
    outputs = calc(program, inputs, pos)
    return outputs

def run_program(program: List[int], phases: List[int]) -> int:
    output = 0
    phase_pos = {}
    for phase in phases:
        phase_pos[phase] = 0

    while output is not None:
        for phase in phases:
            print("PHASE " + str(phase))
            temp, latest_pos = run_amp(program, output, phase, phase_pos[phase])
            output = temp.pop()
            phase_pos[phase] = latest_pos

    return output

def best_program(program: List[int]) -> int:
    max = 0
    for phases in itertools.permutations(range(5)):
        output = run_program(program, phases)
        print("phases: " + str(phases) + " -> " + str(output))
        max = output if output > max else max
    return max

# part 2
with open("day7_input", "r") as f:
    lines = [int(x) for x in f.readline().split(",")]


PROGRAM2 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
PHASES2 = [9,8,7,6,5]
OUTPUT_SIGNAL2 = 139629729

print(run_program(PROGRAM2, PHASES2))
