from dsa_tree import DSABinarySearchTree

import pickle
from typing import List, Tuple, Union


def read_csv() -> Union[DSABinarySearchTree, None]:
    tree = None
    print()
    path = input("Enter file path: ")
    try:
        file = open(path, "r")
        lines = [line.rstrip("\n") for line in file]
    except FileNotFoundError:
        print("File not found.")
    except OSError:
        print("Failed to read from file")
    else:
        try:
            pairs: List[Tuple[int, int]] = []
            for line in lines:
                cols = line.split(",")
                pairs.append((int(cols[0]), int(cols[1])))
        except (IndexError, ValueError):
            print("Invalid CSV format.")
        else:
            tree = DSABinarySearchTree()
            for key, value in pairs:
                try:
                    tree.insert(key, value)
                except ValueError:
                    print("Warning: duplicate key found; ignoring.")
        finally:
            try:
                file.close()
            except OSError:
                pass
    return tree


def read_serialised() -> Union[DSABinarySearchTree, None]:
    tree = None
    print()
    path = input("Enter file path: ")
    try:
        file = open(path, "rb")
    except FileNotFoundError:
        print("File not found.")
    except OSError:
        print("Failed to open file.")
    else:
        try:
            tree = pickle.load(file)
        # I know this is bad practice, but as usual, Python docs don't actually
        # give a comprehensive list of exceptions that pickle.load may raise.
        except Exception:
            print("Failed to read serialised tree")
        else:
            if not isinstance(tree, DSABinarySearchTree):
                print("Serialised file does not contain a DSABinarySearchTree.")
                tree = None
        finally:
            try:
                file.close()
            except OSError:
                pass
    return tree


def display_tree(tree: DSABinarySearchTree) -> None:
    print()
    if tree:
        tree.display()
    else:
        print("No tree has been created.")


def write_csv(tree: DSABinarySearchTree) -> None:
    print()
    path = input("Enter file path: ")

    print("Select a tree traversal order:")
    print("\t1) In order")
    print("\t2) Pre-order")
    print("\t3) Post-order")
    option = None
    while option is None:
        s = input()
        try:
            option = int(s)
        except ValueError:
            print("Enter an integer from 1-3")
        else:
            if not 1 <= option <= 3:
                print("Enter an integer from 1-3")
                option = None

    if option == 1:
        iterator = tree.in_order()
    elif option == 2:
        iterator = tree.pre_order()
    elif option == 3:
        iterator = tree.post_order()
    else:
        raise AssertionError("Didn't expect option {}".format(option))

    try:
        file = open(path, "x")
    except FileExistsError:
        print("File already exists.")
    except OSError:
        print("Failed to open file.")
    else:
        try:
            for key, value in iterator:
                file.write("{},{}\n".format(key, value))
        except OSError:
            print("Failed to write to file.")
        finally:
            try:
                file.close()
            except OSError:
                pass


def write_serialised(tree: DSABinarySearchTree) -> None:
    print()
    path = input("Enter file path: ")
    try:
        file = open(path, "xb")
    except FileExistsError:
        print("File already exists.")
    except OSError:
        print("Failed to open file.")
    else:
        try:
            pickle.dump(tree, file)
        # I know this is bad practice, but as usual, Python docs don't actually
        # give a comprehensive list of exceptions that pickle.dump may raise.
        except Exception:
            print("Failed to write serialised tree.")
        finally:
            try:
                file.close()
            except OSError:
                pass


tree = None
option = None
while option != 6:
    if option is not None:
        print()
    print("Select an option:")
    print("\t1) Read data from CSV file")
    print("\t2) Read serialised tree")
    print("\t3) Display tree")
    print("\t4) Write data to CSV file")
    print("\t5) Serialise tree")
    print("\t6) Exit")

    option = None
    while option is None:
        s = input()
        try:
            option = int(s)
        except ValueError:
            print("Enter an integer from 1-5")
        else:
            if not 1 <= option <= 5:
                print("Enter an integer from 1-5")
                option = None

    if option == 1:
        tree = read_csv()
    elif option == 2:
        tree = read_serialised()
    elif option == 3:
        display_tree(tree)
    elif option == 4:
        write_csv(tree)
    elif option == 5:
        write_serialised(tree)
    elif option == 6:
        pass
    else:
        raise AssertionError("Didn't expect option {}".format(option))
