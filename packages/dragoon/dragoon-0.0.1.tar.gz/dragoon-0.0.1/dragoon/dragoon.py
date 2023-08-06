#!/usr/bin/env python
import random
import sys


def main():
    grid = Grid()

    t = 5 if len(sys.argv) < 2 else int(sys.argv[1])
    for _ in range(t):
        x, y = roll()
        grid.hit(x, y)

    grid.draw()


def roll():
    bad = ((1, 1), (4, 4), (1, 4), (4, 1))
    r = random.randint(0, 5), random.randint(0, 5)

    if r in bad:
        r = roll()

    return r


class Grid:
    def __init__(self):
        self.g = [[0] * 6 for _ in range(6)]

    def draw(self):
        vert = "│"
        hor = "─" * 3
        top = "  ┌{}┐".format("┬".join([hor] * 6))
        divide = "  ├{}┤".format(("┼").join([hor] * 6))
        bottom = "  └{}┘".format("┴".join([hor] * 6))

        print()
        print(top)
        for i, r in zip(range(6, 0, -1), self.g):
            if i != 6:
                print(divide)
            r = [str(c) if c else " " for c in r]
            r = " {} ".format(vert).join(r)
            print("{} {} {} {}".format(red(i), vert, r, vert))
        print(bottom)
        print(
            "   {}".format(" ".join(" {} ".format(str(i)) for i in range(1, 7))),
            end="\n" * 2,
        )

    def hit(self, x, y):
        self.g[x][y] += 1


def red(s):
    return "\u001b[31m{}\u001b[0m".format(s)
