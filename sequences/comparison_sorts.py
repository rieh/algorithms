import random
import Queue


def quick_sort(lst):
    '''Randomized quicksort.'''
    
    if len(lst) <= 1:
        return lst
    
    ind = random.randint(0, len(lst) - 1)
    pivot = lst[ind]
    less = [x for x in lst if x < pivot]
    same = [x for x in lst if x == pivot]
    bigger = [x for x in lst if x > pivot]

    return quick_sort(less) + same + quick_sort(bigger)


def merge_sort(lst):
    
    if len(lst) <= 1:
        return lst
    left = merge_sort(lst[:len(lst) / 2])
    right = merge_sort(lst[len(lst) / 2:])
    return _merge(left, right)

def _merge(left_lst, right_lst):
    '''Return the merge of sorted lists left_lst and right_lst'''

    if not left_lst or not right_lst:
      return left_lst or right_lst

    left, right = left_lst[0], right_lst[0]
    if left <= right:
      return [left] + _merge(left_lst[1:], right_lst)
    else:
      return [right] + _merge(left_lst, right_lst[1:])

def insertion_sort(lst):
    
    for i in range(len(lst)):
        j = i
        while j > 0 and lst[j - 1] > lst[j]:
            lst[j], lst[j - 1] = lst[j - 1], lst[j]
            j -= 1
    return lst

def bubble_sort(lst):
    
    for i in range(len(lst)):
        for j in range(len(lst) - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

def selection_sort(lst):
    
    for i, m in enumerate(range(len(lst))):
        for j in range(i, len(lst)):
            m = min(m, j, lambda x: lst[x])
        lst[i], lst[m] = lst[m], lst[i]
    return lst

def heap_sort(lst):

    make_heap(lst)
    res = []
    while lst:
        res.append(lst[0])
        lst[0] = lst.pop()
        bubble_down(lst, 0)
    return res


def make_heap(lst):
    '''Turn lst into a min-heap'''

    for i in range(len(lst)/2 - 1, -1, -1):
        bubble_down(lst, i)

def bubble_down(lst, i):
    '''Bubble down element at index i in lst'''
    
    while True:
        lc = 2 * i + 1
        rc = 2 * i + 2
        
        if lc >= len(lst) and rc >= len(lst):
            break
        
        if lc >= len(lst) or rc >= len(lst) :
            child = min(lc, rc)
        elif lst[lc] < lst[rc]:
            child = lc
        else:
            child = rc
        
        if lst[i] > lst[child]:
            lst[child], lst[i] = lst[i], lst[child]
            i = child
        else:
            break
