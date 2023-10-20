import sys
import os
import pylcs

ARGC = 4

class Mode:
    LCS = 1
    BASIC = 2

if len(sys.argv) != ARGC:
    sys.exit(f"Expected {ARGC - 1} args: dir1, dir2, min_percent")

# get args skipping command name
dir1_name, dir2_name, min_percent = sys.argv[1:]

min_percent = int(min_percent)

if min_percent < 0 or min_percent > 100:
    sys.exit("Wrong min_percent")

if dir1_name == dir2_name:
    sys.exit(f"Comparison with oneself for {dir1_name}")

def dir_files(dir_name: str) -> str:
    for root, dirs, files in os.walk(dir_name):
        if len(dirs):
            sys.exit(f"Subdirectories are not supprted (found in {dir_name})")
        for file_name in files:
            yield os.path.join(root, file_name)

total_size_dir1 = 0
total_size_dir2 = 0
percentage = dict()

print("Considered files:")
for file_name in dir_files(dir1_name):
    size = os.stat(file_name).st_size
    total_size_dir1 += size
    print(f"{file_name} of size {size}")

for file_name in dir_files(dir2_name):
    size = os.stat(file_name).st_size
    total_size_dir2 += size
    print(f"{file_name} of size {size}")

mode = Mode.LCS if total_size_dir1 * total_size_dir2 < 10 ** 8 else Mode.BASIC

def count_similar(s1: str, s2: str) -> int:
    res = 0
    for c1, c2 in zip(s1, s2):
        res += 1 if c1 == c2 else 0

def get_max_len(s1: str, s2: str) -> int:
    return max(len(s1), len(s2))

pairs = []
for file_name1 in dir_files(dir1_name):
    for file_name2 in dir_files(dir2_name):
        pairs.append((file_name1, file_name2))
        with open(file_name1, 'rb') as file1:
            s1 = file1.read()
        with open(file_name2, 'rb') as file2:
            s2 = file2.read()
        match mode:
            case Mode.LCS:
                percentage[(file_name1,file_name2)] = pylcs.lcs_sequence_length(s1, s2) / get_max_len(s1, s2) if get_max_len(s1, s2) else 1
            case Mode.BASIC:
                percentage[(file_name1,file_name2)] = count_similar(s1, s2) / get_max_len(s1, s2) if get_max_len(s1, s2) else 1

pairs.sort(key=lambda x: percentage[x], reverse=True)

identical = []
simmilar = []
used = set()

for p in pairs:
    if percentage[p] * 100 < min_percent:
        break
    if p[0] in used or p[1] in used:
        continue
    used.add(p[0])
    used.add(p[1])
    if (percentage[p] == 1):
        identical.append(p)
    else:
        simmilar.append(p)

print("Identical files:")
for p in identical:
    print(p)

print("Simmilar files:")
for p in simmilar:
    print(f"{p} with percentage {percentage[p] * 100}")

print(f"Only in {dir1_name}:")
for file_name in dir_files(dir1_name):
    if not file_name in used:
        print(file_name)

print(f"Only in {dir2_name}:")
for file_name in dir_files(dir2_name):
    if not file_name in used:
        print(file_name)
