import collections


class DictCounter(object):
    def __init__(self):
        super(DictCounter, self).__init__()
        self.__dict_internal = {}

    def add(self, key, addition=1):
        val = self.__dict_internal.get(key, 0)
        val += addition
        self.__dict_internal[key] = val

    def to_dict(self):
        return self.__dict_internal


class DictList(object):
    def __init__(self):
        super(DictList, self).__init__()
        self.__dict_internal = {}

    def add(self, key, value, dup=False):
        arr = self.__dict_internal.get(key, [])

        if dup:
            arr.append(value)
        else:
            if value not in arr:
                arr.append(value)

        self.__dict_internal[key] = arr

    def to_dict(self):
        return self.__dict_internal


class OrderedDictList(object):
    def __init__(self):
        super(OrderedDictList, self).__init__()
        self.__dict_internal = collections.OrderedDict()

    def add(self, key, value):
        arr = self.__dict_internal.get(key, [])
        arr.append(value)
        self.__dict_internal[key] = arr

    def to_dict(self):
        return dict(self.__dict_internal)

