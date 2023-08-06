
class Vertex:
    def __init__(self, name=''):
        self.__name = name
        self.__edges = set()

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self):
        return self.__name

    @property
    def edges(self):
        return self.__edges

    def add_edge(self, edg):
        if edg.beg != self:
            raise ValueError(f'Trying to add an edge to the vertex "{self.name}" the beginning of which is "{edg.beg.name}".')
        self.__edges.add(edg)

    def remove_edge(self, edg):
        self.__edges.remove(edg)

    def rename(self, new_name: str):
        self.__name = new_name
