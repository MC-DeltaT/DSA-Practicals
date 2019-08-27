from dsa_tree import DSABinarySearchTree


print("Select an option:")
print("\t1) Read data from CSV file")
print("\t2) Read serialised tree")
print("\t3) Display tree")
print("\t4) Write data to CSV file")
print("\t5) Serialise tree")
print("\t6) Exit")

option = None
while option != 6:
    while option is None:
        s = input()
        try:
            option = int(s)
        except ValueError:
            print("Enter an integer from 1-5")

    if option == 1:
        ...
    elif option == 2:
        ...
    elif option == 3:
        ...
    elif option == 4:
        ...
    elif option == 5:
        ...
    elif option == 6:
        pass
    else:
        print("Enter an integer from 1-5")
