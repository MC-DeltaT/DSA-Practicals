from dsa_stack import DSAStack

import sys
from typing import Union


class TowersOfHanoi:
    def __init__(self, num_pegs: int, num_disks: int) -> None:
        self.num_pegs = num_pegs
        self.num_disks = num_disks
        self.pegs = [
            DSAStack(num_disks),
            DSAStack(num_disks),
            DSAStack(num_disks),
        ]

    def place_disk(self, peg: int, disk: int) -> None:
        peg = self.pegs[peg]
        if peg.is_empty() or disk < peg.top():
            peg.push(disk)
        else:
            raise ValueError(
                "Disk of size {} cannot be placed on disk of size {}.".format(disk, peg.top()))

    def remove_disk(self, peg: int) -> int:
        peg = self.pegs[peg]
        return peg.pop()

    def move_disk(self, src: int, dst: int) -> None:
        self.place_disk(dst, self.remove_disk(src))

    # Gets the disk at the given peg and index from bottom, or None if none
    # exists.
    def disk_at(self, peg: int, i: int) -> Union[int, None]:
        p = self.pegs[peg].as_list()
        if i < len(p):
            d = p[-1 - i]
        else:
            d = None
        return d


# Moves n disks from peg src to peg dst (1-indexed).
def solve(n: int, src: int, dst: int) -> None:
    src -= 1
    dst -= 1

    towers = TowersOfHanoi(3, n)

    for i in range(n, 0, -1):
        towers.place_disk(src, i)

    step = 0
    display_progress(towers, step)

    solve_impl(towers, n, src, dst, step)


# Moves n disks from peg src to peg dst (0-indexed).
# Returns the new step count.
def solve_impl(towers: TowersOfHanoi, n: int, src: int, dst: int, step: int) -> int:
    if n <= 0:
        raise AssertionError("n must be > 0.")
    elif n == 1:
        towers.move_disk(src, dst)
        step += 1
        display_progress(towers, step)
    else:
        other = 3 - src - dst
        step = solve_impl(towers, n - 1, src, other, step)
        towers.move_disk(src, dst)
        step += 1
        display_progress(towers, step)
        step = solve_impl(towers, n - 1, other, dst, step)
    return step


def display_progress(towers: TowersOfHanoi, step: int) -> None:
    header = "Step {}:".format(step)
    indent = " " * (len(header) + 2)
    disk_width = len(str(towers.num_disks))
    print(header)
    for i in range(towers.num_disks - 1, -1, -1):
        print(indent, end="")
        for j in range(towers.num_pegs):
            disk = towers.disk_at(j, i)
            if disk is None:
                s = "|"
            else:
                s = str(disk)
            # Padding for when disk could be multiple columns wide.
            s = " " * (disk_width - len(s)) + s
            print(s + " ", end="")
        print()
    print()


if len(sys.argv) != 4:
    print("Usage: python {} num_disks src_peg dst_peg".format(sys.argv[0]))
else:
    try:
        num_disks = int(sys.argv[1])
        src = int(sys.argv[2])
        dst = int(sys.argv[3])
    except ValueError:
        print("Parameters must be integers.")
    else:
        if num_disks < 1:
            print("num_disks must be > 0.")
        # Currently needs 8 extra stack frames to run, will require adjustment
        # if implementation changes.
        elif sys.getrecursionlimit() < num_disks + 8:
            print("Solving with num_disks={} would exceed max call stack depth."
                .format(num_disks))
        elif not 0 < src <= 3:
            print("src_peg must be > 0 and <= 3.")
        elif not 0 < dst <= 3:
            print("dst_peg must be > 0 and <= 3.")
        else:
            print("Solving Towers of Hanoi with {} pegs and {} disks, starting from peg {} and ending at peg {}."
                .format(3, num_disks, src, dst))
            print("Number of moves required: {}.".format(2 ** num_disks - 1))
            print()
            solve(num_disks, src, dst)
