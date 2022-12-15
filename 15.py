import re
import time
from collections import namedtuple
from typing import List, Tuple, Set

Coordinates = namedtuple("Coordinates", "x y")
Segment = namedtuple("Segment", "start end")
Rectangle = Tuple[Coordinates, Coordinates]


def fts(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


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


def task1(text: str):
    lines = text.strip().split("\n")
    line = 2000000
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
    return 4000000 * x + y


def transform(point: Coordinates) -> Coordinates:
    return Coordinates(point.x + point.y, point.y - point.x)


def detransform(point: Coordinates) -> Coordinates:
    return Coordinates((point.x - point.y) // 2, (point.x + point.y) // 2)


def make_rectangle(sensor, beacon):
    dist = distance(sensor, beacon)
    return (transform(Coordinates(sensor.x, sensor.y - dist)),
            transform(Coordinates(sensor.x, sensor.y + dist)))


def difference(orig, removed) -> Set[Rectangle]:
    if orig[0].x > removed[1].x or orig[0].y > removed[1].y or \
            orig[1].x < removed[0].x or orig[1].y < removed[0].y:
        return {orig}
    res = set()
    x = orig[0].x
    y = orig[0].y
    if x < removed[0].x <= removed[1].x:
        res.add((Coordinates(x, y), Coordinates(removed[0].x - 1, orig[1].y)))
        x = removed[0].x
    if y < removed[0].y <= orig[1].y:
        res.add((Coordinates(x, y), Coordinates(orig[1].x, removed[0].y - 1)))
        y = removed[0].y
    if x <= removed[1].x < orig[1].x:
        res.add((Coordinates(removed[1].x + 1, y), orig[1]))
    if y <= removed[1].y < orig[1].y:
        res.add((Coordinates(x, removed[1].y + 1),
                 Coordinates(min(orig[1].x, removed[1].x), orig[1].y)))
    return res


def corners(rectangle):
    cs = [detransform(rectangle[0]),
          detransform(rectangle[1]),
          detransform(Coordinates(rectangle[0].x, rectangle[1].y)),
          detransform(Coordinates(rectangle[1].x, rectangle[0].y))]
    return cs


def task2(text: str):
    lines = text.strip().split("\n")
    max_coord = 4000000
    coords = parse(lines)
    rectangles = {(transform(Coordinates(max_coord // 2, -max_coord // 2)),
                   transform(Coordinates(max_coord // 2, 3 * max_coord // 2)))}
    for sensor, beacon in coords:
        new_rectangles = set()
        removed = make_rectangle(sensor, beacon)
        for rectangle in rectangles:
            new_rectangles.update(difference(rectangle, removed))
        rectangles = new_rectangles
    for rectangle in rectangles:
        for corner in corners(rectangle):
            if 0 <= corner.x <= max_coord and 0 <= corner.y <= max_coord:
                return frequency(corner.x, corner.y)


if __name__=="__main__":
    inp = fts("15in.txt")
    print(task1(inp))
    start = time.time()
    print(task2(inp))
    print(f"time: {time.time() - start} s")
