from SortLibrary import *

def merge(L):
    size = len(L)
    if size == 1:
        return L
    
    L1 = merge(L[0:size//2])
    L2 = merge(L[size//2:])

    new_L = []
    i_f = 0
    i_e = 0
    
    while(i_f < len(L1) and i_e < len(L2)):
        if(L1[i_f] < L2[i_e]):
            new_L.append(L1[i_f])
            i_f += 1
        else:
            new_L.append(L2[i_e])
            i_e += 1

    if(i_f == len(L1)):
        new_L.extend(L2[i_e:])
    else:
        new_L.extend(L1[i_f:])
        
    return new_L

for i in range(100):
    random_L = RandomList()
    new_L = merge(random_L)
    is_sorted(new_L)
is_sorted(random_L)
