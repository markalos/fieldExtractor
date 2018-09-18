def sliceArray(arr, size):
    assert size > 1
    cnt = (len(arr) - 1) // size
    start = 0
    for i in range(cnt):
        yield arr[start : start + size]
        start = start + size
    yield arr[start:]