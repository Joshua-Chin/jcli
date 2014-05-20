class sym(str):

    index = 0
    instances = {}

    def __new__(cls, string):
        if string in cls.instances:
            return cls.instances[string]
        else:
            instance = super().__new__(cls, string)
            instance._hash = cls.index
            cls.index += 1
            cls.instances[string] = instance
            return instance

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return "<sym: "+super().__repr__()+">"

class linked_list(tuple):

    def __new__(self, seq):
        out = null
        for elem in reversed(seq):
            out = cons(elem, out)
        return out

    def __iter__(self):
        while self is not null:
            yield car(self)
            self = cdr(self)

    def __len__(self):
        try:
            return self.__len
        except AttributeError:
            self.__len = len(list(iter(self)))
            return self.__len

    def __getitem__(self, index):
        for i, elem in enumerate(self):
            if i == index:
                return elem
        raise IndexError("index out of range")

    def __repr__(self):
        return repr(list(self))

def cons(car, cdr):
    return tuple.__new__(linked_list, (car, cdr))

def car(ll):
    return tuple.__getitem__(ll, 0)

def cdr(ll):
    return tuple.__getitem__(ll, 1)

null = tuple.__new__(linked_list, ())

class frame(dict):

    def __init__(self, outer = None):
        super().__init__()
        self.outer = outer

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        try:
            return self.outer[key]
        except (AttributeError, TypeError):
            raise KeyError

class function(tuple):

    def __repr__(self):
        return "<function>"
