from random import randrange

class SortError(Exception):
    def __init__(self, List):
        self.List = List
    def __str__(self):
        sort_L = sorted(self.List)
        return " List is not sorted: \n" + repr(self.List) + "\ntrue sort = \n" + repr(sort_L) 

def is_sorted(L: list):
    prev = L[0]
    for i in L:
        if i < prev:
            raise SortError(L)
        prev = i
    return "Good Stuff"

def RandomList(F: int = 0,E: int = 10, n: int = 20 )->list:
    '''
    Creates random list of size n, with values ranging from F to E
    '''
    L = []
    for i in range(n):
        L.append(randrange(F,E))
    return L

def left_child(x):
    return 2*x + 1

def right_child(x):
    return 2*x + 2

def parent(x):
    return (x-1)//2

def print_heap(Heap):
    from math import log, floor
    height = floor(log(len(Heap), 2))
    for level in range(height + 1):
        print("   " * (2**(height) - (2**level)//2), end = '')
        for j in range(2**level - 1, 2**(level + 1)-1):
            if(j > len(Heap) - 1):
                break
            print("[", Heap[j], "]", end = '')
        print("\n")
    











    
