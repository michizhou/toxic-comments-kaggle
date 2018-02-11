class Pair:
    def __init__(self, k, v, naturalOrder=False):
        self.first = k
        self.second = v
        self.naturalOrder = naturalOrder

    def __lt__(self, other):
        if self.naturalOrder:
            return self.second < other.second
        return self.second * -1 < other.second

    def __gt__(self, other):
        return other.__lt__(self)

    def __le__(self, other):
        if self.naturalOrder:
            return self.second <= other.second
        return self.second * -1 <= other.second

    def __ge__(self, other):
        return other.__le__(self)

    def __eq__(self, other):
        if self.naturalOrder:
            return self.second == other.second
        return self.second * -1 == other.second

    def __ne__(self, other):
        return not self.__eq__(other)
