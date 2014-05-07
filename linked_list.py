class linked_list(tuple):

    def __new__(self, seq):
        out = null
        for elem in reversed(seq):
            out = cons(elem, out)
        return out

    def __getitem__(self, key):
        for num, elem in enumerate(self):
            if num == key:
                return elem
        raise KeyError

    def __len__(self):
        try:
            return self.__len
        except AttributeError:
            self.__len = len(list(iter(self)))
            return self.__len

    def __iter__(self):
        if self is null:
            return
        yield tuple.__getitem__(self, 0)
        for elem in cdr(self):
            yield elem

    def __repr__(self):
        if self is null:
            return '()'
        return "'("+" ".join(map(str, self)) + ')'
        


def car(linked_list):
    return tuple.__getitem__(linked_list, 0)

def cdr(linked_list):
    return tuple.__getitem__(linked_list, 1)

null = tuple.__new__(linked_list, ())

def cons(car, cdr):    
    return tuple.__new__(linked_list, (car, cdr))
