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
            return "()"
        return "("+" ".join(map(str, self)) + ')'
        


def car(linked_list):
    return tuple.__getitem__(linked_list, 0)

def cdr(linked_list):
    return tuple.__getitem__(linked_list, 1)

null = tuple.__new__(linked_list, ())

def cons(car, cdr):    
    return tuple.__new__(linked_list, (car, cdr))

class sym(str):

    index = 0
    instances = {}

    def __new__(cls, string):
        string = str(string)
        if string in sym.instances:
            return sym.instances[string]
        instance = str.__new__(sym, string)
        instance.__hash = sym.index
        sym.index += 1
        sym.instances[string] = instance
        return instance

    def __eq__(self, other):
        return hash(self) == hash(other) and isinstance(other, sym)

    def __hash__(self):
        return self.__hash

    def __repr__(self):
        return '<sym:'+str.__repr__(self)+'>'

class quote(object):

    def __new__(cls, value):
        if isinstance(value, (str, int, float, bool)):
            return value
        out = object.__new__(cls)
        out.__init__(value)
        return out

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "'" + str(self.value)

    def __repr__(self):
        return '<quote:'+repr(self.value)+'>'

class macro(object):

    def __init__(self, value):
        self.value = value

class closure(dict):

    def __init__(self, outer = None):
        super().__init__()
        self.outer = outer

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        try:
            return self.outer[key]
        except AttributeError:
            raise KeyError
