from collections import namedtuple
Coordinates = namedtuple("Coordinates", "x y")


def file_to_lines(filename):
    with open(filename) as f:
        return f.readlines()


def move_head(head: Coordinates, direction: str) -> Coordinates:
    if direction == "R":
        return Coordinates(head.x+1, head.y)
    if direction == "L":
        return Coordinates(head.x-1, head.y)
    if direction == "U":
        return Coordinates(head.x, head.y+1)
    if direction == "D":
        return Coordinates(head.x, head.y-1)


def is_too_far(tail: Coordinates, head: Coordinates) -> bool:
    return max(abs(tail.x - head.x), abs(tail.y - head.y)) > 1


def is_next_to(tail: Coordinates, head: Coordinates) -> Coordinates:
    return (abs(tail.x - head.x) == 1 and tail.y == head.y) or \
           (abs(tail.y - head.y) == 1 and tail.x == head.x)


def is_diagonal(tail: Coordinates, head: Coordinates) -> Coordinates:
    return (abs(tail.x - head.x) == 1) and (abs(tail.y - head.y) == 1)


def move_tail(tail: Coordinates, head: Coordinates) -> Coordinates:
    if not is_too_far(tail, head):
        return tail
    for i in range(tail.x-1, tail.x+2):
        for j in range(tail.y-1, tail.y+2):
            if is_next_to(Coordinates(i, j), head):
                return Coordinates(i, j)
    for i in (tail.x-1, tail.x+1):
        for j in (tail.y-1, tail.y+1):
            if is_diagonal(Coordinates(i, j), head):
                return Coordinates(i, j)


def simulate(lines, num_knots):
    knots = [Coordinates(0, 0)] * num_knots
    tail_set = {knots[-1]}
    for line in lines:
        direction, distance = line.split()
        distance = int(distance)
        for _ in range(distance):
            knots[0] = move_head(knots[0], direction)
            for i in range(1, num_knots):
                knots[i] = move_tail(knots[i], knots[i-1])
            tail_set.add(knots[-1])
    return len(tail_set)


inp = file_to_lines("09in.txt")
print(simulate(inp, 2))
print(simulate(inp, 10))
