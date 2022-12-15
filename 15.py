import re
from collections import namedtuple
from typing import List, Tuple

Coordinates = namedtuple("Coordinates", "x y")
Segment = namedtuple("Segment", "start end")


def ftl(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return f.read().strip().split("\n")


def distance(a: Coordinates, b: Coordinates):
    return abs(a.x - b.x) + abs(a.y - b.y)


def segment_covered(sensor: Coordinates, beacon: Coordinates, line: int):
    dist = distance(sensor, beacon)
    to_line = abs(sensor.y - line)
    if dist >= to_line:
        return Segment(sensor.x - (dist - to_line), sensor.x + (dist - to_line))
    return None


def simplify_segments(segments: List[Segment]):
    segments.sort(key=lambda s: s.start)
    last_seg = segments[0]
    new_segments = []
    for seg in segments[1:]:
        if seg.start > last_seg.end + 1:
            new_segments.append(last_seg)
            last_seg = seg
            continue
        if seg.end <= last_seg.end:
            continue
        last_seg = Segment(last_seg.start, seg.end)
    new_segments.append(last_seg)
    return new_segments


def vals_in_segments(segments: List[Segment]):
    vals = set()
    for segment in segments:
        vals.update(range(segment.start, segment.end + 1))
    return vals


def parse(lines: List[str]) -> List[Tuple[Coordinates, Coordinates]]:
    coords = []
    for line in lines:
        m = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
                     line)
        sensor = Coordinates(int(m.group(1)), int(m.group(2)))
        beacon = Coordinates(int(m.group(3)), int(m.group(4)))
        coords.append((sensor, beacon))
    return coords


def task1(lines, line):
    coords = parse(lines)
    segments = []
    beacons = set()
    for sensor, beacon in coords:
        if beacon.y == line:
            beacons.add(beacon.x)
        seg = segment_covered(sensor, beacon, line)
        if seg:
            segments.append(seg)
    segments = simplify_segments(segments)
    count = 0
    for seg in segments:
        count += seg.end - seg.start + 1
    count -= len(beacons)
    return count


def frequency(x, y):
    print(x, y)
    return 4000000 * x + y


def task2(lines, max_coord):
    coords = parse(lines)
    for line in range(max_coord + 1):
        segments = []
        for sensor, beacon in coords:
            seg = segment_covered(sensor, beacon, line)
            if seg:
                segments.append(seg)
        segments = simplify_segments(segments)
        if len(segments) == 1 and segments[0].start <= 0 and segments[0].end >= max_coord:
            continue
        if segments[0].start > 0:
            return frequency(0, line)
        return frequency(segments[0].end + 1, line)


inp = ftl("15in.txt")
print(task1(inp, 2000000))
print(task2(inp, 4000000))
