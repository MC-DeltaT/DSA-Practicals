from dsa_hash_table import DSAHashTable


def from_file(path: str) -> DSAHashTable:
    with open(path) as file:
        hashtable = DSAHashTable(1000)
        for line_num, line in enumerate(file, 1):
            line = line.rstrip("\n")
            cols = line.split(",")
            if len(cols) != 2:
                raise ValueError(
                    f"On line {line_num}: expected 2 values but got {len(cols)}.")
            key, value = cols
            hashtable.put(key, value)
        return hashtable


def to_file(hashtable: DSAHashTable, path: str) -> None:
    with open(path, "w") as file:
        for key, value in hashtable.items():
            file.write(f"{key},{value}\n")


if __name__ == "__main__":
    try:
        hashtable = from_file("RandomNames7000.csv")
    except OSError as e:
        print(f"Failed to read input file: {e}")
    else:
        try:
            to_file(hashtable, "activity3_output.csv")
        except OSError as e:
            print(f"Failed to write output file: {e}")
