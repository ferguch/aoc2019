from typing import List, Dict

def read_input() -> List[str]:
    with open("day6_input", "r") as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

def build_orbits(input: List[str]) -> Dict:
    orbits_dict = {}
    for orbits in input:
        (orbit, planet) = orbits.split(")")
        orbits_dict[planet] = orbit
    print(orbits_dict)
    return orbits_dict

def total_orbits(input: List[str]) -> int:
    orbits = build_orbits(input)
    orbit_count = 0
    for planet in orbits:
        direct_orbit = orbits[planet]
        orbit_count += 1

        while direct_orbit != "COM":
            direct_orbit = orbits[direct_orbit]
            orbit_count += 1
    return orbit_count

# part 1
assert total_orbits(["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"]) == 42
input = read_input()
print(total_orbits(input))

#part 2
def common_planet_steps(input: List[str], planet1: str, planet2: str) -> int:
    orbits_dict = build_orbits(input)
    orbit_steps = {}
    orbit_count = 0
    while planet1 != "COM":
        orbit_count += 1
        planet1 = orbits_dict[planet1]
        orbit_steps[planet1] = orbit_count

    orbit_count = 0
    while planet2 != "COM":
        orbit_count += 1
        planet2 = orbits_dict[planet2]
        if planet2 in orbit_steps.keys():
            return orbit_count + orbit_steps[planet2] - 2
    return -1

assert common_planet_steps(["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","K)YOU","I)SAN"], "YOU", "SAN") == 4
print(common_planet_steps(input, "YOU", "SAN"))