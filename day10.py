from typing import NamedTuple, List, Dict, Tuple
from collections import defaultdict
import math

class Asteroid(NamedTuple):
    x: int
    y: int

Asteroids = List[Asteroid]

def parse_asteroids(input: str) -> Asteroids:
    return [
        Asteroid(x, y)
        for y, line in enumerate(input.strip().split("\n"))
        for x, c in enumerate(line)
        if c == '#'
    ]
def count_visible(asteroids: Asteroids, station: Asteroid) -> int:
    slopes = set()
    for x, y in asteroids:
        dx = x - station.x
        dy = y - station.y

        gcd = math.gcd(dx, dy)

        if dx == dy == 0:
            pass
        else:
            slopes.add((dx / gcd, dy / gcd))
    return len(slopes)

def best_station(asteroids: Asteroids) -> Tuple[Asteroid, int]:
    results = [(a, count_visible(asteroids, a)) for a in asteroids]
    return max(results, key=lambda pair: pair[1])

A = parse_asteroids("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""")

print(A)

ASTERIODS = parse_asteroids(""".#......##.#..#.......#####...#..
...#.....##......###....#.##.....
..#...#....#....#............###.
.....#......#.##......#.#..###.#.
#.#..........##.#.#...#.##.#.#.#.
..#.##.#...#.......#..##.......##
..#....#.....#..##.#..####.#.....
#.............#..#.........#.#...
........#.##..#..#..#.#.....#.#..
.........#...#..##......###.....#
##.#.###..#..#.#.....#.........#.
.#.###.##..##......#####..#..##..
.........#.......#.#......#......
..#...#...#...#.#....###.#.......
#..#.#....#...#.......#..#.#.##..
#.....##...#.###..#..#......#..##
...........#...#......#..#....#..
#.#.#......#....#..#.....##....##
..###...#.#.##..#...#.....#...#.#
.......#..##.#..#.............##.
..###........##.#................
###.#..#...#......###.#........#.
.......#....#.#.#..#..#....#..#..
.#...#..#...#......#....#.#..#...
#.#.........#.....#....#.#.#.....
.#....#......##.##....#........#.
....#..#..#...#..##.#.#......#.#.
..###.##.#.....#....#.#......#...
#.##...#............#..#.....#..#
.#....##....##...#......#........
...#...##...#.......#....##.#....
.#....#.#...#.#...##....#..##.#.#
.#.#....##.......#.....##.##.#.##""")