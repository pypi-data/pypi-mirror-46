class Combiner:
    def __init__(self, ele_set, min_eles, max_eles):
        if not all((isinstance(ele_set, (tuple, list, set)), isinstance(min_eles, int), isinstance(max_eles, int))):
            raise TypeError
        if min_eles < 1 or max_eles < min_eles:
            raise ValueError
        self._ele_set = ele_set
        self._min_eles = min_eles
        self._max_eles = max_eles
        self._index_range = len(self._ele_set) - 1
        self._max_index = self._max_eles - 1
        self._eles = len(self._ele_set)

    def __len__(self):
        total = 0
        for eles in range(self._min_eles, self._max_eles + 1):
            total += self._eles ** eles
        return total

    def __iter__(self):
        self._ele_tags = [-1 for _ in range(self._max_eles)]
        for index in range(self._min_eles - 1):
            self._ele_tags[index] = self._index_range
        return self

    def __next__(self):
        self._next()
        return [self._ele_set[tag] for tag in self._ele_tags if tag != -1][::-1]

    def _next(self, index=0):
        if self._ele_tags[index] == self._index_range:
            if index == self._max_index:
                raise StopIteration
            self._ele_tags[index] = 0
            self._next(index + 1)
        else:
            self._ele_tags[index] += 1
