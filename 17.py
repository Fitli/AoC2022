def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


class Cave:
    def __init__(self):
        self.width = 7
        self.cols = [[False] * 10 for _ in range(self.width)]
        self.max_height = 0
        self.playground_height = 10

    def is_flat(self):
        if self.max_height == 0:
            return True
        for col in self.cols:
            if not col[self.max_height - 1]:
                return False
        return True


shapes = {
    0:((0, 0), (1,0), (2,0), (3,0)),
    1:((0,1), (1,2), (1,1), (1,0), (2,1)),
    2:((0,0), (1,0), (2,0), (2,1), (2,2)),
    3:((0, 0), (0,1), (0,2), (0,3)),
    4:((0,0), (0,1), (1,0), (1,1))
}


class Rock:
    def __init__(self, shape, cave: Cave):
        left_border = 2
        bottom_border = cave.max_height+3
        self.blocks = [(left_border + x, bottom_border + y) for x, y in shapes[shape]]
        self.cave = cave

    def test_move(self, direction):
        dx, dy = direction
        for x, y in self.blocks:
            x += dx
            y += dy
            if x < 0 or x >= 7 or y < 0 or self.cave.cols[x][y]:
                return False
        return True

    def move(self, direction):
        if not self.test_move(direction):
            return False
        dx, dy = direction
        for i, block in enumerate(self.blocks):
            x, y = block
            self.blocks[i] = (x+dx, y+dy)
        return True

    def settle(self):
        for x, y in self.blocks:
            self.cave.cols[x][y] = True
            self.cave.max_height = max(self.cave.max_height, y+1)
        missing_height = self.cave.max_height + 10 - self.cave.playground_height
        for _ in range(missing_height):
            for col in self.cave.cols:
                col.append(False)
            self.cave.playground_height += 1


def hashstate(cave, i, rock: Rock, limit=50):
    cave_state = tuple(tuple(col[-limit:]) for col in cave.cols)
    rock_state = ((x, y-cave.max_height) for x, y in rock.blocks)
    return hash((i, rock_state, cave_state))

def simulate(text, iters):
    cache = {}
    text = text.strip()
    text_len = len(text)
    cave = Cave()
    i = 0
    max_fall = 0
    sh = 0
    additional_height = 0
    while sh < iters:
        fall = 0
        rock = Rock(sh % 5, cave)
        while True:
            if text[i] == "<":
                rock.move((-1, 0))
            else:
                rock.move((1, 0))
            i += 1
            i %= text_len
            fall += 1

            state = hashstate(cave, i, rock, 50)
            if state in cache:
                freq = sh - cache[state][0]
                grow = cave.max_height - cache[state][1]
                skip = ((iters-sh)//freq)
                iters -= skip*freq
                additional_height = skip*grow
                cache = {}

            cache[state] = (sh, cave.max_height)

            if not rock.move((0, -1)):
                rock.settle()
                max_fall = max(fall, max_fall)
                break
        sh += 1

    return cave.max_height + additional_height

def task1(text):
    return simulate(text, 2022)

def task2(text):
    return simulate(text, 1000000000000)

if __name__ == "__main__":
    inp = fts("17in.txt")
    print(task1(inp))
    print(task2(inp))
