from lgraph.vertex import Vertex


class Edge:
    ROUND_BRACKETS = ['(', ')', '']
    SQUARE_BRACKETS = ['[', ']', '']

    def __init__(self, beg_vertex: Vertex, end_vertex: Vertex, label='', round_trace=('', 0), square_trace=('', 0)):
        self.__beg = beg_vertex
        self.__end = end_vertex
        self.__label = label
        if isinstance(round_trace, str) and round_trace in self.ROUND_BRACKETS:
            round_trace = (round_trace, 0)
        if isinstance(square_trace, str) and square_trace in self.SQUARE_BRACKETS:
            square_trace = (square_trace, 0)

        if not (isinstance(round_trace, tuple) and isinstance(square_trace, tuple) and len(round_trace) == len(square_trace) == 2
                and isinstance(round_trace[1], int) and isinstance(square_trace[1], int)):
            raise ValueError('Bracket trace should be a tuple object with a bracket as first element and its number as a second.')
        if not round_trace[0] in self.ROUND_BRACKETS:
            raise ValueError('Round bracket trace should be a tuple object with a '
                             'round bracket as first element and its number as a second.')
        if not square_trace[0] in self.SQUARE_BRACKETS:
            raise ValueError('Square bracket trace should be a tuple object with a '
                             'square bracket as first element and its number as a second.')

        self.__round_trace = round_trace
        self.__square_trace = square_trace

    def __eq__(self, other):
        return (isinstance(self, type(other))
                and self.__beg == other.__beg
                and self.__end == other.__end
                and self.__label == other.__label
                and self.__round_trace == other.__round_trace
                and self.__square_trace == other.__square_trace)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key())

    def __dict__(self):
        return dict(
            beginning=self.__beg.name,
            end=self.__end.name,
            label=self.__label,
            round_trace=self.__round_trace,
            square_trace=self.__square_trace,
        )

    def __key(self):
        return self.__beg.name, self.__end.name, self.__label, self.__round_trace, self.__square_trace

    @property
    def beg(self):
        return self.__beg

    @property
    def end(self):
        return self.__end

    @property
    def label(self):
        return self.__label

    @property
    def round_trace(self):
        return self.__round_trace

    @property
    def square_trace(self):
        return self.__square_trace
