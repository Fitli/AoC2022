import re


def fts(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def task1(inp: str) -> str:
    lines = inp.split("\n")
    ncolumns = (len(lines[0]) + 1) // 4
    stacks = [[] for _ in range(ncolumns)]
    for line in lines:
        if "[" in line:
            for i in range(ncolumns):
                if line[4 * i + 1] != " ":
                    stacks[i].insert(0, line[4 * i + 1])
        if line and line[0] == "m":
            move = re.search(r"move (\d+) from (\d) to (\d)", line)
            num = int(move.group(1))
            fr = int(move.group(2)) - 1
            to = int(move.group(3)) - 1
            for _ in range(num):
                stacks[to].append(stacks[fr].pop(-1))
    return "".join([x[-1] for x in stacks])


def task2(inp: str) -> str:
    lines = inp.split("\n")
    ncolumns = (len(lines[0]) + 1) // 4
    stacks = [[] for _ in range(ncolumns)]
    for line in lines:
        if "[" in line:
            for i in range(ncolumns):
                if line[4 * i + 1] != " ":
                    stacks[i].insert(0, line[4 * i + 1])
        if line and line[0] == "m":
            move = re.search(r"move (\d+) from (\d) to (\d)", line)
            num = int(move.group(1))
            fr = int(move.group(2)) - 1
            to = int(move.group(3)) - 1
            stacks[to] += stacks[fr][(-num):]
            stacks[fr] = stacks[fr][:(-num)]
    return "".join([x[-1] for x in stacks])


text = fts("05in.txt")
print(task1(text))
print(task2(text))
