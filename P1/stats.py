# Additional visualisation of sorting algorithms.
# Not part of the prac, I just did it anyway.



from DSAsorts import bubbleSort, insertionSort, selectionSort

from collections import defaultdict
import random
import time

import matplotlib.pyplot as plot
import numpy


array_size_min = 100
array_size_max = 2000
array_size_inc = 100
array_val_min = 0
array_val_max = 1000


# Generates an array of the given size with random integer elements.
def random_array(size: int):
    return numpy.random.randint(low=array_val_min, high=array_val_max, size=size)


# Generates a random array of the given size that has the fraction p elements unsorted.
def nearly_sorted_array(size: int, p: float):
    assert 0.0 <= p <= 1.0
    sorted_count = round(size * p)
    l = random.sample(range(array_val_min, array_val_max), k=sorted_count)
    l = sorted(l)
    for i in range(size - sorted_count):
        pos = random.randrange(0, len(l))
        val = random.randint(array_val_min, array_val_max)
        l.insert(pos, val)
    return numpy.array(l)


# Sorts arr with the given sorting function and returns the time taken in seconds.
def do_sort(arr, sorter):
    t1 = time.perf_counter()
    sorter(arr)
    t2 = time.perf_counter()
    return t2 - t1


sizes = []
times = defaultdict(list)
for size in range(array_size_min, array_size_max, array_size_inc):
    print(size)
    sizes.append(size)

    arr = random_array(size)
    for sorter in (bubbleSort, insertionSort, selectionSort):
        times[sorter.__name__ + "_random"].append(do_sort(arr.copy(), sorter))

    arr = nearly_sorted_array(size, 0.1)
    for sorter in (bubbleSort, insertionSort, selectionSort):
        times[sorter.__name__ + "_nearlySorted"].append(do_sort(arr.copy(), sorter))


for sorter in times:
    plot.plot(sizes, times[sorter], label=sorter)
plot.title("Array size vs. sort time")
plot.xlabel("Array size")
plot.ylabel("Time (s)")
plot.legend()
plot.show()
