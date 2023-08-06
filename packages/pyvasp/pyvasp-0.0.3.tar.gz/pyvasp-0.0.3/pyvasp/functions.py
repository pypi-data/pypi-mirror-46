
import numpy as np

class Slice(object):
    def __getitem__(self, item):
        return item

def getInfo(file, pattern, index, last=True):
    '''get colIndex-th column of pattern matched line in file
    Args         Type     Description
    ============ ======== =====================================================
    file         str      file name
    pattern      str      key word
    index        sliceObj index
    last         bool     return last one if True else all

    Return
    ============ ======== =====================================================
    value        list
    '''

    with open(file) as f:
        value = [line.split()[index] for line in f.readlines()
                 if pattern in line]
    if not last:
        return value
    else:
        return value[-1]

def resize(x):
    if x > 1:
        return x - 1
    elif x < 0:
        return x + 1
    else:
        return x
vec_resize = np.vectorize(resize)
