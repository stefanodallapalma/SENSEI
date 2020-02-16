def array_split(array, size_of_array):
    """
    q = int(len(array) / size_of_array)
    r = len(array) % size_of_array

    subarray_numbers = q
    if r > 0:
        subarray_numbers += 1

    sub_arrays = np.array_split(array, subarray_numbers)
"""
    sub_arrays = []
    partion_numbers = int(len(array) / size_of_array)
    if (len(array) % size_of_array) > 0:
        partion_numbers += 1

    for i in range(partion_numbers):
        start = i * size_of_array
        if i < (partion_numbers-1):
            end = (i + 1) * size_of_array
        else:
            end = len(array)
        sub_arrays.append(array[start:end])

    return sub_arrays
