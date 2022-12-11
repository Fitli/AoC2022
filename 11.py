import math
import re


def file_to_text(filename):
    with open(filename) as f:
        return f.read()


class Monkey:
    def __init__(self, mid, items, transform_fcn, throw_fcn, decide_prime):
        self.id = mid
        self.items = items
        self.transform_fcn = transform_fcn
        self.throw_fcn = throw_fcn
        self.decide_prime = decide_prime
        self.num_inspections = 0

    def __str__(self):
        return f"Monkey {self.id}: items {self.items}, num inspections {self.num_inspections}"

    def catch(self, item):
        self.items.append(item)

    def play(self, additional_transform, monkeys):
        for item in self.items:
            item = self.transform_fcn(item)
            item = additional_transform(item)
            throw_to = monkeys[self.throw_fcn(item)]
            throw_to.catch(item)
            self.num_inspections += 1
        self.items = []


def parse_transform_fcn(line):
    m = re.search(r"Operation: new = (\d+|old) ([*+]) (\d+|old)$", line)
    if m.group(2) == "+":
        if m.group(1) == "old" and m.group(3) == "old":
            return lambda old: old + old
        elif m.group(1) == "old":
            return lambda old: old + int(m.group(3))
        elif m.group(3) == "old":
            return lambda old: old + int(m.group(1))
        else:
            return lambda old: int(m.group(1)) + int(m.group(3))
    if m.group(2) == "*":
        if m.group(1) == "old" and m.group(3) == "old":
            return lambda old: old * old
        elif m.group(1) == "old":
            return lambda old: old * int(m.group(3))
        elif m.group(3) == "old":
            return lambda old: old * int(m.group(1))
        else:
            return lambda old: int(m.group(1)) * int(m.group(3))


def parse_monkey(text):
    lines = text.split("\n")
    m = re.search(r"Monkey (\d+):", lines[0])
    mid = int(m.group(1))
    m = re.search(r"Starting items: (\d+(, \d+)*)", lines[1])
    items = list(map(int, m.group(1).split(",")))
    transform_fcn = parse_transform_fcn(lines[2])
    m = re.search(r"Test: divisible by (\d+)$", lines[3])
    test = int(m.group(1))
    m = re.search(r"If true: throw to monkey (\d+)$", lines[4])
    true = int(m.group(1))
    m = re.search(r"If false: throw to monkey (\d+)$", lines[5])
    false = int(m.group(1))
    throw_fcn = (lambda x: true if x % test == 0 else false)
    return Monkey(mid, items, transform_fcn, throw_fcn, test)


def task1(text):
    monkeys = list(map(parse_monkey, text.split("\n\n")))
    for _ in range(20):
        for monkey in monkeys:
            monkey.play(lambda x: x // 3, monkeys)
    max2 = sorted(monkeys, key=lambda m: m.num_inspections, reverse=True)[:2]
    return max2[0].num_inspections * max2[1].num_inspections


def task2(text):
    monkeys = list(map(parse_monkey, text.split("\n\n")))
    modulo = math.prod([m.decide_prime for m in monkeys])
    for i in range(10000):
        for monkey in monkeys:
            monkey.play(lambda x: x % modulo, monkeys)
    max2 = sorted(monkeys, key=lambda m: m.num_inspections, reverse=True)[:2]
    return max2[0].num_inspections * max2[1].num_inspections


inp = file_to_text("11in.txt")
print(task1(inp))
print(task2(inp))
