from typing import NamedTuple, List
from dataclasses import dataclass
import copy, math

# make immutable
@dataclass
class XYZ:
    x: int
    y: int
    z: int

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

class Moon:
    def __init__(self, pos: XYZ, vel: XYZ = None) -> None:
        self.pos = pos
        self.vel = vel or XYZ(0, 0, 0)

    def __repr__(self):
        return f"Moon(pos={self.pos}, vel={self.vel})"

    def potential_energy(self) -> int:
        return self.pos.energy()

    def kinetic_energy(self) -> int:
        return self.vel.energy()

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()

    def apply_velocity(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def sig_x(self):
        return (self.pos.x, self.vel.x)

    def sig_y(self):
        return (self.pos.y, self.vel.y)

    def sig_z(self):
        return (self.pos.z, self.vel.z)

def step(moons: List[Moon]) -> None:
    # first apply acceleration
    n = len(moons)
    for moon1 in moons:
        for moon2 in moons:
            if moon1 != moon2:
                # adjust the velocity of moon1
                if moon1.pos.x < moon2.pos.x:
                    moon1.vel.x += 1
                elif moon1.pos.x > moon2.pos.x:
                    moon1.vel.x -= 1

                if moon1.pos.y < moon2.pos.y:
                    moon1.vel.y += 1
                elif moon1.pos.y > moon2.pos.y:
                    moon1.vel.y -= 1

                if moon1.pos.z < moon2.pos.z:
                    moon1.vel.z += 1
                elif moon1.pos.z > moon2.pos.z:
                    moon1.vel.z -= 1

    # next apply velocity
    for moon in moons:
        moon.apply_velocity()

moons = [Moon(XYZ(-1, 0, 2)),
         Moon(XYZ(2, -10, -7)),
         Moon(XYZ(4, -8, 8)),
         Moon(XYZ(3, 5, -1))]

# part 1
# for x in range(10):
#     step(moons)
#     print(x)
#     for moon in moons:
#         print(moon)

moons = [Moon(XYZ(14, 2, 8)),
        Moon(XYZ(7, 4, 10)),
        Moon(XYZ(1, 17, 16)),
        Moon(XYZ(-4, -1, 1))]

# for x in range(1000):
#     step(moons)
# print(sum(moon.total_energy() for moon in moons))

# part 2
def sig_x(moons: List[Moon]):
    return tuple(moon.sig_x() for moon in moons)

def sig_y(moons: List[Moon]):
    return tuple(moon.sig_y() for moon in moons)

def sig_z(moons: List[Moon]):
    return tuple(moon.sig_z() for moon in moons)


def steps_to_repeat(moons: List[Moon], sig_fn) -> int:
    moons = copy.deepcopy(moons)

    seen = set()
    seen.add(sig_fn(moons))

    num_steps = 0

    while True:
        num_steps += 1
        step(moons)
        sig = sig_fn(moons)
        if sig in seen:
            return num_steps
        else:
            seen.add(sig)

a = steps_to_repeat(moons, sig_x)
b = steps_to_repeat(moons, sig_y)
c = steps_to_repeat(moons, sig_z)
print(a, b, c)
ab = a * b // math.gcd(a, b)
abc = ab * c // math.gcd(ab, c)
print(ab, abc)


