import re


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


inverse = {
    "l": {
        "+": lambda x, d: d - x,
        "-": lambda x, d: d + x,
        "*": lambda x, d: d // x,
        "//": lambda x, d: d * x,
        "=": lambda x, d: x
    },
    "r": {
        "+": lambda x, d: d - x,
        "-": lambda x, d: x - d,
        "*": lambda x, d: d // x,
        "//": lambda x, d: x // d,
        "=": lambda x, d: x
    }
}


class Monkey:
    def __init__(self, name, job):
        self.name = name
        m = re.match("\d+$", job)
        if m:
            self.value = int(m.group())
            self.left, self.right, self.oper = None, None, None
        m = re.match(r"(\w{4}) ([\+\-\*\/]) (\w{4})", job)
        if m:
            self.value = None
            self.left = m.group(1)
            self.right = m.group(3)
            self.oper = m.group(2)
        if self.oper == "/":
            self.oper = "//"

    def evaluate(self, monkeys, part):
        if part == 2 and self.name == "humn":
            self.value = None
            return None
        if self.value is not None:
            return self.value
        l = monkeys[self.left].evaluate(monkeys, part)
        r = monkeys[self.right].evaluate(monkeys, part)
        if l is None or r is None:
            return None
        self.value = eval(f"{l}{self.oper}{r}")
        return self.value

    def determine(self, required, monkeys):
        # print(f"{self.name} has to shout {required}")
        self.value = required
        if self.name == "humn":
            return
        l = monkeys[self.left].value
        r = monkeys[self.right].value
        if l is None:
            monkeys[self.left].determine(inverse["l"][self.oper](r, required), monkeys)
        if r is None:
            monkeys[self.right].determine(inverse["r"][self.oper](l, required), monkeys)


def load_monkeys(text: str):
    monkeys = {}
    for line in text.strip().split("\n"):
        name, job = line.split(": ")
        monkeys[name] = Monkey(name, job)
    return monkeys


def task1(text):
    monkeys = load_monkeys(text)
    return monkeys["root"].evaluate(monkeys, 1)


def task2(text):
    monkeys = load_monkeys(text)
    monkeys["root"].oper = "="
    monkeys["root"].evaluate(monkeys, 2)
    monkeys["root"].determine(1, monkeys)
    return monkeys["humn"].value


if __name__ == "__main__":
    inp = fts("21in.txt")
    print(task1(inp))
    print(task2(inp))
