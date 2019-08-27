# Takes student IDs from a CSV file, sorts them with various sorting
# algorithms, and outputs them to file.


from DSAsorts import bubbleSort, selectionSort, insertionSort

from typing import Mapping, Text

import numpy


input_file_path = "RandomNames7000.csv"
output_file_template = "Names_{}ed.csv"


# Reads the student IDs from the given file and returns them as a numpy array.
# Raises OSError on file IO error, ValueError on incorrect CSV format.
def read_ids(file_path: Text) -> numpy.ndarray:
    try:
        input_file = open(file_path)
        lines = list(input_file)
    finally:
        try:
            input_file.close()
        except OSError:
            pass

    # Already have file lines, just map so it's iterated as first CSV column.
    # ValueError if int can't be parsed.
    try:
        ids = list(map(lambda line: int(line.split(",")[0]), lines))
    except ValueError as e:
        raise ValueError("Invalid CSV format: expected integer for student ID.")
    ids = numpy.array(ids)

    return ids


# Sorts the given array with the different sorting algorithms and return them
# in a dictionary of (sorter_name, sorted_array) mappings.
def do_sorts(arr: numpy.ndarray) -> Mapping[str, numpy.ndarray]:
    sorts = {}
    for sorter in (bubbleSort, selectionSort, insertionSort):
        arr_sorted = arr.copy()
        sorter(arr_sorted)
        sorts[sorter.__name__] = arr_sorted
    return sorts


# Takes a dictionary of (sorter_name, sorted_array) mappings and writes each
# to an output file.
# Raises OSError on file IO error.
def output_sorts(sorts: Mapping[str, numpy.ndarray]) -> None:
    try:
        for sorter_name, sorted_arr in sorts.items():
            output_file_path = output_file_template.format(sorter_name)
            output_file = open(output_file_path, "w")
            for val in sorted_arr:
                output_file.write("{}\n".format(val))
    finally:
        output_file.close()


try:
    ids = read_ids(input_file_path)
except OSError as e:
    print("Failed to read file {}: {}".format(input_file_path, e))
except ValueError as e:
    print(str(e))
else:
    sorts = do_sorts(ids)
    try:
        output_sorts(sorts)
    except OSError as e:
        print("Failed to write to file: {}".format(e))
