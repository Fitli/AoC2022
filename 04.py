import re


def fts(path):
    with open(path, "r") as f:
        return f.read()


lines = fts("04in.txt").split()
count1 = 0
count2 = 0
for line in lines:
    match = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
    nums = list(map(int, match.groups()))
    if nums[0] <= nums[2] and nums[3] <= nums[1]:
        count1 += 1
    elif nums[2] <= nums[0] and nums[1] <= nums[3]:
        count1 += 1
    if set(range(nums[0], nums[1]+1)).intersection(set(range(nums[2], nums[3]+1))):
        count2 += 1

print(count1)
print(count2)

