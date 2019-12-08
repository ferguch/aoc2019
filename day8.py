from typing import List
from collections import Counter
import copy
import sys

Layer = List[List[int]]
Image = List[Layer]

def parse(raw: str, width: int, height: int) -> Image:
    pixels = [int(pixel) for pixel in raw]
    num_layers = len(pixels) // height // width
    image = []
    for _ in range(num_layers):
        image.append([[0 for _ in range(width)]
            for _ in range(height)])

    layer = x = y = 0

    for pixel in pixels:
        image[layer][y][x] = int(pixel)

        if x == width - 1:
            x = 0
            y += 1
            if y == height:
                layer += 1
                y = 0
        else:
            x += 1

    return image

def count_colours(image: Image) -> List[Counter]:
    layers_counter = []
    for layer in image:
        layer_pixels = [pixel for row in layer for pixel in row]
        layers_counter.append(Counter(layer_pixels))    # Counter is a Dict
    return layers_counter

def multiply_counts(image: Image, fewest_value: int) -> int:
    fewest_count = sys.maxsize
    colour_counts = count_colours(image)
    fewest_count_layer = min(colour_counts, key=lambda colour_count: colour_count[0])
    # for colour_count in colour_counts:
    #     current_fewest_count = colour_count.get(fewest_value, 0)
    #     if current_fewest_count < fewest_count:
    #         fewest_count = current_fewest_count
    #         fewest_count_layer = colour_count
    return fewest_count_layer.get(1) * fewest_count_layer.get(2)

# part 1
test_image = parse("123456789012", 3, 2)
assert test_image == [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]
print(count_colours(test_image))
assert multiply_counts(test_image, 0) == 1

with open("day8_input") as f:
    raw = f.read().strip()

image = parse(raw, 25, 6)
print(multiply_counts(image, 0))

# part 2
def decode(image: Image, width: int, height: int) -> Layer:
    master_layer = copy.deepcopy(image[0])
    for y in range(height):
        for x in range(width):
            #print("x=" + str(x) + ", y=" + str(y))
            for layer in image:
                if layer[y][x] != 2:
                    master_layer[y][x] = str(layer[y][x])
                    break
    return master_layer

test_image = parse("0222112222120000", 2, 2)
assert decode(test_image, 2, 2) == [["0", "1"], ["1", "0"]]

decoded_image = decode(image, 25, 6)
for layer in decoded_image:
    layer_str = "".join(layer)
    print(layer_str.replace("1", "*").replace("0", " "))