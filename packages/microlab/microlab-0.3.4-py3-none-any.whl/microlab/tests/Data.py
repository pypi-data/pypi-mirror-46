import numpy

# Time
a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Value
b = [0, 1, 2, 3, 1, -1, -2, -3, -2, -1, 1]

# 1 Dimension
List_a = list(a)
List_b = list(b)

Tuple_a = tuple(a)
Tuple_b = tuple(b)

# 2 Dimensions
npArray_a = numpy.array(a)
npArray_b = numpy.array(b)


# Datasets
dataset_list = list([List_a, List_b])
dataset_tuple = tuple([Tuple_a, Tuple_b])
dataset_npArray = numpy.array([npArray_a, npArray_b])