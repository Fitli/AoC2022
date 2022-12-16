from collections import namedtuple
from typing import Tuple, Dict, List
import re
CachedItem = namedtuple("CachedItem", "exact upper")


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def parse_problem(text):
    lines = text.strip().split("\n")
    flows: Dict[str, int] = {}
    tunnels: Dict[str, List[str]] = {}

    for line in lines:
        m = re.match(r"Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (\w{2}(, \w{2})*)", line)
        if m:
            valve = m.group(1)
            flow = int(m.group(2))
            tunnel_to = m.group(3).split(", ")
            flows[valve] = flow
            tunnels[valve] = []
            for v in tunnel_to:
                tunnels[valve].append(v)
    return flows, tunnels


def distances(tunnels):
    dists: Dict[Tuple[str, str], int] = {}
    for start in tunnels:
        dists[(start, start)] = 0
        to_inspect = {start}
        while to_inspect:
            new_inspect = set()
            for v in to_inspect:
                for t in tunnels[v]:
                    if (start, t) not in dists:
                        dists[(start, t)] = dists[(start, v)] + 1
                        new_inspect.add(t)
            to_inspect = new_inspect
    return dists


def maximize(origin, flows, dists, used, minutes, cache, lower_bound):
    if minutes <= 1:
        return 0
    reachable = tuple(f for f in flows if f not in used
                      and dists[(origin, f)] < minutes
                      and flows[f] > 0)

    if (reachable, minutes) in cache[origin]:
        return cache[origin][(reachable, minutes)]

    # weird idea turned into microoptimization: check cache for slightly relaxed problems
    for mins in range(minutes + 1, minutes + 5):
        if cache[origin].get((reachable, mins), lower_bound) < lower_bound:
            return 0

    max_pressure = 0
    for r in reachable:
        arrival = minutes - dists[(origin, r)]
        # open
        pressure = (arrival-1) * flows[r]
        used.add(r)
        pressure += maximize(r, flows, dists, used, arrival - 1,
                             cache, max(max_pressure, lower_bound) - pressure)
        if pressure > max_pressure:
            max_pressure = pressure
        used.remove(r)
    cache[origin][reachable, minutes] = max_pressure
    return max_pressure


def task1(text):
    flows, tunnels = parse_problem(text)
    dists = distances(tunnels)
    cache = {v: {} for v in flows}
    return maximize("AA", flows, dists, set(), 30, cache, 0)


def all_sols(origin, flows, dists, used, minutes, prev_pressure, solutions):
    if minutes <= 1:
        return 0
    reachable = tuple(f for f in flows if f not in used
                      and dists[(origin, f)] < minutes
                      and flows[f] > 0)
    for r in reachable:
        arrival = minutes - dists[(origin, r)]
        # open
        pressure = (arrival-1) * flows[r]
        used.add(r)
        t_used = tuple(used)
        if prev_pressure + pressure > solutions.get(t_used, 0):
            solutions[t_used] = prev_pressure + pressure
        all_sols(r, flows, dists, used, arrival - 1, prev_pressure + pressure, solutions)
        used.remove(r)


def task2(text):
    flows, tunnels = parse_problem(text)
    dists = distances(tunnels)
    solutions = {}
    all_sols("AA", flows, dists, set(), 26, 0, solutions)

    max_pressure = 0
    sorted_sols = sorted(solutions.items(), key=lambda x: x[1], reverse=True)
    for me in range(len(sorted_sols)):
        my_set = None
        for elephant in range(me):
            pressure = sorted_sols[me][1] + sorted_sols[elephant][1]
            if pressure < max_pressure:
                break
            if pressure == max_pressure:
                continue
            if not my_set:
                my_set = set(sorted_sols[me][0])
            if not my_set.intersection(sorted_sols[elephant][0]):
                max_pressure = pressure
    return max_pressure


if __name__ == "__main__":
    inp = fts("16in.txt")
    print(task1(inp))
    print(task2(inp))
