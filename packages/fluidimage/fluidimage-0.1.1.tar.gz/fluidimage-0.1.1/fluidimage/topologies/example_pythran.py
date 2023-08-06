import numpy as np

# pythran export cpu1(uint8[:,:], uint8[:,:], int)
def cpu1(array1, array2, nloops=10):

    a = np.arange(10000000 // nloops)
    result = a
    for i in range(nloops):
        result += a ** 3 + a ** 2 + 2

    for i in range(nloops):
        array1 = array1 * array2
    return (array1, array1)


# pythran export cpu2(uint8[:,:], uint8[:,:], int)
def cpu2(array1, array2, nloops=10):

    a = np.arange(10000000 // nloops)
    result = a
    for i in range(nloops):
        result += a ** 3 + a ** 2 + 2

    for i in range(nloops):
        array1 = np.multiply(array1, array2)
    return array1
