import time
from enum import Enum
import re

from ortools.sat.python import cp_model


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


class Material(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4


def parse_line(line):
    m = re.match(
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. "
        r"Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore "
        r"and (\d+) obsidian.", line)
    blueprint = int(m.group(1))
    robot_cost = {}
    robot_cost[Material.ORE] = {Material.ORE: int(m.group(2)), Material.CLAY: 0,
                                Material.OBSIDIAN: 0, Material.GEODE: 0}
    robot_cost[Material.CLAY] = {Material.ORE: int(m.group(3)), Material.CLAY: 0,
                                 Material.OBSIDIAN: 0, Material.GEODE: 0}
    robot_cost[Material.OBSIDIAN] = {Material.ORE: int(m.group(4)), Material.CLAY: int(m.group(5)),
                                     Material.OBSIDIAN: 0, Material.GEODE: 0}
    robot_cost[Material.GEODE] = {Material.ORE: int(m.group(6)), Material.CLAY: 0,
                                  Material.OBSIDIAN: int(m.group(7)), Material.GEODE: 0}
    return blueprint, robot_cost


def solve(recipes, time):
    init_robs = {
        Material.ORE: 1,
        Material.CLAY: 0,
        Material.OBSIDIAN: 0,
        Material.GEODE: 0,
    }

    model = cp_model.CpModel()

    # Variables
    bulid_robots = [
        {r: model.NewBoolVar(f'b{i},{r}') for r in init_robs}
        for i in range(time)
    ]
    robots_n = [
        {r: model.NewIntVar(0, i + 1, f'r{i},{r}') for r in init_robs}
        for i in range(time)
    ]
    stock_n = [
        {m: model.NewIntVar(0, i ** 2, f's{i},{m}') for m in init_robs}
        for i in range(time)
    ]

    # Constraints
    # Can't make multiple robots at once
    for t in range(time):
        model.AddAtMostOne(bulid_robots[t][r] for r in init_robs)

    # Initial state
    for r in init_robs:
        model.Add(robots_n[0][r] == init_robs[r])
        model.Add(stock_n[0][r] == 0)

    # Robot update
    for t in range(1, time):
        for r in init_robs:
            model.Add(robots_n[t][r] == robots_n[t - 1][r] + bulid_robots[t - 1][r])

    # stock update
    for t in range(1, time):
        for m in init_robs:
            model.Add(stock_n[t - 1][m] >= sum(
                [bulid_robots[t - 1][r] * recipes[r][m] for r in init_robs]))
            model.Add(stock_n[t][m] == stock_n[t - 1][m] + robots_n[t - 1][m] - sum(
                [bulid_robots[t - 1][r] * recipes[r][m] for r in init_robs]))

    model.Maximize(stock_n[time - 1][Material.GEODE] + robots_n[time - 1][Material.GEODE])

    solver = cp_model.CpSolver()
    solver.Solve(model)

    return int(solver.ObjectiveValue())


def task1(text):
    lines = text.strip().split("\n")
    score = 0
    for line in lines:
        blueprint, recipes = parse_line(line)
        geodes = solve(recipes, 24)
        score += geodes * blueprint
    return score


def task2(text):
    lines = text.strip().split("\n")
    score = 1
    for line in lines[:3]:
        blueprint, recipes = parse_line(line)
        geodes = solve(recipes, 32)
        score *= geodes
    return score


if __name__=="__main__":
    start = time.time()
    inp = fts("19in.txt")
    print(task1(inp))
    print(task2(inp))
    print(f"{time.time() - start} s")
