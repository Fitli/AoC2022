def file_to_lines(filename):
    with open(filename) as f:
        return f.readlines()


def process_line(line):
    spl = line.strip().split()
    if spl[0] == "noop":
        return 0, 1
    if spl[0] == "addx":
        return int(spl[1]), 2


def task1(lines):
    cycle = 0
    x = 1
    s = 0
    interesting_cycle = 20
    for line in lines:
        dx, dcycle = process_line(line)
        x, cycle = x + dx, cycle + dcycle
        if (cycle + 1 - cycle % 2) == interesting_cycle - 1:
            s += interesting_cycle * x
            print(cycle, x, interesting_cycle * x, s)
            interesting_cycle += 40
        if cycle > 220:
            break
    return s


def task2(lines):
    x = 1
    line_i = 0
    dx = 0
    wait = 0
    for _ in range(6):
        line = ""
        for pos in range(40):
            if wait == 0:
                x += dx
                dx, wait = process_line(lines[line_i])
                line_i += 1
            if x - 1 <= pos <= x + 1:
                line += "#"
            else:
                line += "."
            wait -= 1
        print(line)


inp = file_to_lines("10in.txt")
print(task1(inp))
task2(inp)
