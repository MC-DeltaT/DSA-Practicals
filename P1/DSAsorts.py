#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

def bubbleSort(A):
    n = 0
    is_sorted = False
    while not is_sorted and n < len(A) - 1:
        is_sorted = True
        for i in range(len(A) - 1 - n):
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i]
                is_sorted = False
        n += 1


def insertionSort(A):
    for n in range(1, len(A)):
        i = n
        while A[i - 1] > A[i] and i > 0:
            A[i], A[i - 1] = A[i - 1], A[i]
            i -= 1


def selectionSort(A):
    for i in range(len(A)):
        min_idx = i
        for j in range(i + 1, len(A)):
            if A[j] < A[min_idx]:
                min_idx = j
        A[i], A[min_idx] = A[min_idx], A[i]


def mergeSort(A):
    """ mergeSort - front-end for kick-starting the recursive algorithm
    """
    ...

def mergeSortRecurse(A, leftIdx, rightIdx):
    ...

def merge(A, leftIdx, midIdx, rightIdx):
    ...

def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    ...

def quickSortRecurse(A, leftIdx, rightIdx):
    ...

def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    ...


