import re
import time
from enum import Enum
from typing import Dict, Optional, Set


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


class Material(Enum):
    GEODE = 1
    OBSIDIAN = 2
    CLAY = 3
    ORE = 4


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


def can_buy(my_material: Dict[Material, int], robot_cost, considered) -> Set[Optional[Material]]:
    robots = {None}
    for robot in considered:
        can_buy = True
        for m in robot_cost[robot]:
            if my_material[m] < robot_cost[robot][m]:
                can_buy = False
                break
        if can_buy:
            robots.add(robot)
    return robots


def next_buy_time(my_material: Dict[Material, int], my_robots, robot_cost, considered) -> int:
    min_t = 32
    for r in considered:
        t = max([-(-max(robot_cost[r][m] - my_material[m], 0) // max(my_robots[m], 1)) for m in
                 robot_cost[r]])
        if t < min_t:
            min_t = t
    return min_t


def pay(my_material, robot, robot_cost):
    if robot is None:
        return
    for m in robot_cost[robot]:
        my_material[m] -= robot_cost[robot][m]


def produce(my_material, my_robots, time):
    for robot in my_robots:
        my_material[robot] += my_robots[robot] * time


def state_to_tuple(my_material, my_robots):
    return (my_material[Material.ORE], my_material[Material.CLAY], my_material[Material.OBSIDIAN],
            my_material[Material.GEODE], my_robots[Material.ORE], my_robots[Material.CLAY],
            my_robots[Material.OBSIDIAN], my_robots[Material.GEODE])


def needed_robots(my_robots, robot_cost):
    productive = {Material.ORE, Material.CLAY, Material.OBSIDIAN}
    needed = {r for r in productive if my_robots[r] < max([robot_cost[m][r] for m in robot_cost])}
    needed.add(Material.GEODE)
    return needed


def explore(my_material, my_robots, minutes, cache, robot_cost, lb, considered_robots):
    t = state_to_tuple(my_material, my_robots)
    if t in cache and cache[t] >= minutes:
        return 0
    if minutes <= 0:
        return my_material[Material.GEODE]
    if my_material[Material.GEODE] + minutes * my_robots[Material.GEODE] + (
            minutes * (minutes - 1)) // 2 < lb:
        return 0
    max_g = 0
    cb = can_buy(my_material, robot_cost, considered_robots)
    if cb == {None}:
        return 0
    for robot in cb:
        new_material = my_material.copy()
        new_robots = my_robots.copy()
        pay(new_material, robot, robot_cost)
        produce(new_material, new_robots, 1)
        if robot is not None:
            new_robots[robot] += 1
            new_considered_robots = needed_robots(new_robots, robot_cost)
        else:
            new_considered_robots = considered_robots.difference(cb)
        time_jump = min(next_buy_time(new_material, new_robots, robot_cost, new_considered_robots),
                        minutes - 1)
        produce(new_material, new_robots, time_jump)
        result = explore(new_material, new_robots, minutes - 1 - time_jump, cache, robot_cost,
                         max(lb, max_g), new_considered_robots)
        if result > max_g:
            max_g = result
    cache[t] = minutes
    return max_g


def init_state():
    my_mat = {
        Material.ORE: 0,
        Material.CLAY: 0,
        Material.OBSIDIAN: 0,
        Material.GEODE: 0,
    }
    my_robs = {
        Material.ORE: 1,
        Material.CLAY: 0,
        Material.OBSIDIAN: 0,
        Material.GEODE: 0,
    }
    return my_mat, my_robs


def task1(text):
    lines = text.strip().split("\n")
    score = 0
    for line in lines:
        blueprint, robot_cost = parse_line(line)
        my_mat, my_robs = init_state()
        considered = needed_robots(my_robs, robot_cost)
        time_jump = next_buy_time(my_mat, my_robs, robot_cost, considered)
        produce(my_mat, my_robs, time_jump)
        result = explore(my_mat, my_robs, 24 - time_jump, {}, robot_cost, 0, considered)
        score += blueprint * result
    return score


def task2(text):
    lines = text.strip().split("\n")
    score = 1
    for line in lines[:3]:
        blueprint, robot_cost = parse_line(line)
        my_mat, my_robs = init_state()
        considered = needed_robots(my_robs, robot_cost)
        time_jump = next_buy_time(my_mat, my_robs, robot_cost, considered)
        produce(my_mat, my_robs, time_jump)
        result = explore(my_mat, my_robs, 32 - time_jump, {}, robot_cost, 0, considered)
        score *= result
    return score


if __name__ == "__main__":
    start = time.time()
    inp = fts("19small.txt")
    print(task1(inp))
    print(f"{time.time() - start} s")
    start = time.time()
    print(task2(inp))
    print(f"{time.time() - start} s")
