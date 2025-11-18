def howManyMissing(lst):
    how_missing = len(lst)
    how_many = lst[-1] - lst[0] + 1
    return how_many - how_missing


if __name__ == '__main__':
    assert howManyMissing([1, 2, 3, 8, 9]) == 4
    assert howManyMissing([1, 3]) == 1
    assert howManyMissing([7, 10, 11, 12]) == 2
    assert howManyMissing([1, 3, 5, 7, 9, 11]) == 5
    assert howManyMissing([5, 6, 7, 8]) == 0
    print("All tests passed!")
