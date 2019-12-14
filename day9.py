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
ADJ_REL=9

def parse_opcode(opcode: int) -> Tuple[int, List[int]]:
    opcode_part = opcode % 100
    hu_digit = (opcode // 100) % 10
    th_digit = (opcode // 1000) % 10
    tt_digit = (opcode // 10000) % 10
    return (opcode_part, [hu_digit, th_digit, tt_digit])

assert parse_opcode(1002) == (2, [0, 1, 0])

def get_value(mode: int, pos: int, rel_pos: int, list: List, offset : int = 1) -> int:
    if mode == 0: # positional
        value = list[list[pos + offset]]
    elif mode == 1: # immediate
        value = list[pos + offset]
    elif mode == 2: # relative
        value = list[list[pos + offset] + rel_pos]
    else:
        raise ValueError(f"Error - incorrect mode: {mode}")
    return value

def get_address(mode: int, pos: int, rel_pos: int, list: List, offset : int = 1) -> int:
    if mode == 0: # positional
        address_value = list[pos + offset]
    elif mode == 2: # relative
        address_value = list[pos + offset] + rel_pos
    else:
        raise ValueError(f"Error - incorrect mode: {mode}")
    return address_value

def calc(list : List[int], input: List[int]) -> List:
    list = list[:]
    list.extend([0] * 10000000)
    output = []
    pos = rel_pos = 0

    while list[pos] != 99: # stop
        opcode, modes = parse_opcode(list[pos])
        print(f"p={pos}, r={rel_pos}, op={opcode}, m={modes}")
        if opcode == ADD: #1
            value1 = get_value(modes[0], pos, rel_pos, list, 1)
            value2 = get_value(modes[1], pos, rel_pos, list, 2)
            #address = get_address(modes[0], pos, rel_pos, list, 3)
            #list[address] = value1 + value2
            # value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            # value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            list[list[pos + 3]] = value1 + value2
            pos += 4
        elif opcode == MULT: #2
            value1 = get_value(modes[0], pos, rel_pos, list, 1)
            value2 = get_value(modes[1], pos, rel_pos, list, 2)
            # value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            # value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            list[list[pos + 3]] = value1 * value2
            pos += 4
        elif opcode == SAVE: #3
            input_value = input[0]
            input = input[1:]
            address = get_address(modes[0], pos, rel_pos, list, 1)
            list[address] = input_value
            #list[list[pos + 1]] = input_value
            pos += 2
        elif opcode == OUTPUT:
            value = get_value(modes[0], pos, rel_pos, list, 1)
            # if modes[0] == 0:
            #     value = list[list[pos + 1]]
            # elif modes[0] == 2:
            #     value = list[list[pos + rel_pos]]
            # else:
            #     value = list[pos + 1]
            output.append(value)
            pos += 2
        elif opcode == JUMP_IF_TRUE:
            value1 = get_value(modes[0], pos, rel_pos, list, 1)
            value2 = get_value(modes[1], pos, rel_pos, list, 2)
            # value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            # value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 != 0:
                pos = value2
            else:
                pos += 3
        elif opcode == JUMP_IF_FALSE:
            value1 = get_value(modes[0], pos, rel_pos, list, 1)
            value2 = get_value(modes[1], pos, rel_pos, list, 2)
            # value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            # value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 == 0:
                pos = value2
            else:
                pos += 3
        elif opcode == LT:
            value1 = get_value(modes[0], pos, rel_pos, list, 1)
            value2 = get_value(modes[1], pos, rel_pos, list, 2)
            # value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            # value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 < value2:
                list[list[pos + 3]] = 1
            else:
                list[list[pos + 3]] = 0
            pos += 4
        elif opcode == EQ:
            value1 = get_value(modes[0], pos, rel_pos, list, 1)
            value2 = get_value(modes[1], pos, rel_pos, list, 2)
            # value1 = list[list[pos + 1]] if modes[0] == 0 else list[pos + 1]
            # value2 = list[list[pos + 2]] if modes[1] == 0 else list[pos + 2]
            if value1 == value2:
                list[list[pos + 3]] = 1
            else:
                list[list[pos + 3]] = 0
            pos += 4
        elif opcode == ADJ_REL:
            #rel_pos = list[list[pos + 1]]
            rel_pos += get_value(modes[0], pos, rel_pos, list, 1)
            print(f"ADJUSTING relative pos to {rel_pos}")
            pos += 2
        else:
            raise ValueError(f"Error: {list[pos]}")
    print(output)
    return output

#assert calc([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], []) == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
#assert calc([1102,34915192,34915192,7,4,7,99,0], [0]) == [1219070632396864]
#assert calc([104,1125899906842624,99], [0]) == [1125899906842624]

PROGRAM = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,37,0,1012,1101,26,0,1008,1101,0,39,1016,1101,0,36,1007,1101,669,0,1024,1102,1,29,1009,1102,0,1,1020,1102,24,1,1003,1102,22,1,1013,1101,0,30,1019,1101,260,0,1027,1101,38,0,1018,1101,642,0,1029,1102,25,1,1004,1101,23,0,1017,1101,21,0,1001,1102,20,1,1010,1102,33,1,1015,1102,35,1,1002,1102,1,1,1021,1102,31,1,1014,1101,895,0,1022,1101,0,32,1011,1102,1,28,1005,1101,0,892,1023,1101,263,0,1026,1102,1,27,1000,1101,647,0,1028,1101,0,34,1006,1102,1,660,1025,109,9,1208,-7,38,63,1005,63,201,1001,64,1,64,1106,0,203,4,187,1002,64,2,64,109,4,2101,0,-5,63,1008,63,24,63,1005,63,227,1001,64,1,64,1106,0,229,4,209,1002,64,2,64,109,5,21107,40,41,0,1005,1018,251,4,235,1001,64,1,64,1105,1,251,1002,64,2,64,109,18,2106,0,-9,1105,1,269,4,257,1001,64,1,64,1002,64,2,64,109,-40,1208,6,35,63,1005,63,287,4,275,1105,1,291,1001,64,1,64,1002,64,2,64,109,11,2102,1,0,63,1008,63,35,63,1005,63,315,1001,64,1,64,1106,0,317,4,297,1002,64,2,64,109,6,21107,41,40,-3,1005,1010,337,1001,64,1,64,1106,0,339,4,323,1002,64,2,64,109,-2,2101,0,-8,63,1008,63,24,63,1005,63,365,4,345,1001,64,1,64,1105,1,365,1002,64,2,64,109,9,21102,42,1,-3,1008,1017,43,63,1005,63,385,1105,1,391,4,371,1001,64,1,64,1002,64,2,64,109,-4,1206,5,407,1001,64,1,64,1105,1,409,4,397,1002,64,2,64,109,13,1206,-9,427,4,415,1001,64,1,64,1106,0,427,1002,64,2,64,109,-25,2107,27,1,63,1005,63,449,4,433,1001,64,1,64,1106,0,449,1002,64,2,64,109,-3,1202,-1,1,63,1008,63,27,63,1005,63,475,4,455,1001,64,1,64,1105,1,475,1002,64,2,64,109,6,21108,43,41,8,1005,1015,491,1106,0,497,4,481,1001,64,1,64,1002,64,2,64,109,6,1205,8,515,4,503,1001,64,1,64,1105,1,515,1002,64,2,64,109,-11,1207,1,23,63,1005,63,531,1105,1,537,4,521,1001,64,1,64,1002,64,2,64,109,1,2108,24,0,63,1005,63,559,4,543,1001,64,1,64,1105,1,559,1002,64,2,64,109,12,21101,44,0,1,1008,1016,44,63,1005,63,585,4,565,1001,64,1,64,1105,1,585,1002,64,2,64,109,-23,2102,1,8,63,1008,63,27,63,1005,63,607,4,591,1105,1,611,1001,64,1,64,1002,64,2,64,109,18,21108,45,45,3,1005,1013,633,4,617,1001,64,1,64,1105,1,633,1002,64,2,64,109,11,2106,0,7,4,639,1106,0,651,1001,64,1,64,1002,64,2,64,109,-1,2105,1,4,4,657,1001,64,1,64,1105,1,669,1002,64,2,64,109,-10,2107,26,-6,63,1005,63,685,1105,1,691,4,675,1001,64,1,64,1002,64,2,64,109,9,1205,1,703,1106,0,709,4,697,1001,64,1,64,1002,64,2,64,109,-12,2108,22,-3,63,1005,63,729,1001,64,1,64,1106,0,731,4,715,1002,64,2,64,109,-11,1207,10,35,63,1005,63,753,4,737,1001,64,1,64,1106,0,753,1002,64,2,64,109,9,21101,46,0,5,1008,1010,43,63,1005,63,773,1105,1,779,4,759,1001,64,1,64,1002,64,2,64,109,-1,1201,4,0,63,1008,63,26,63,1005,63,801,4,785,1105,1,805,1001,64,1,64,1002,64,2,64,109,7,1201,-8,0,63,1008,63,22,63,1005,63,825,1106,0,831,4,811,1001,64,1,64,1002,64,2,64,109,-1,1202,-6,1,63,1008,63,23,63,1005,63,855,1001,64,1,64,1106,0,857,4,837,1002,64,2,64,109,7,21102,47,1,0,1008,1017,47,63,1005,63,883,4,863,1001,64,1,64,1106,0,883,1002,64,2,64,109,8,2105,1,-2,1106,0,901,4,889,1001,64,1,64,4,64,99,21101,0,27,1,21101,915,0,0,1105,1,922,21201,1,20897,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1106,0,922,22101,0,1,-1,21201,-2,-3,1,21102,957,1,0,1106,0,922,22201,1,-1,-2,1106,0,968,22102,1,-2,-2,109,-3,2105,1,0]
# part 1
print(calc(PROGRAM, [1]))
