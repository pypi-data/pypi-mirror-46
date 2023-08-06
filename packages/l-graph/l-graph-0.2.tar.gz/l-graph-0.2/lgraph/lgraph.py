import string
import json

from collections import OrderedDict
from enum import Enum
from lgraph.vertex import Vertex
from lgraph.edge import Edge


class LGraph:
    class LGraphType(Enum):
        RECURSIVELY_ENUMERABLE = 0
        CONTEXT_SENSITIVE = 1
        CONTEXT_FREE = 2
        REGULAR = 3

    def __init__(self, vtx_num=0, alphabet=string.ascii_lowercase):
        self.__initial_main_name = 'initial_main'
        self.__final_main_name = 'final_main'

        self.__initial_prefix = 'initial'
        self.__final_prefix = 'final'
        self.__transition_prefix = 'transition'

        self.__alphabet = alphabet
        self.__initials = dict(initial_main=Vertex(self.__initial_main_name))
        self.__finals = dict(final_main=Vertex(self.__final_main_name))
        self.__vertexes = dict()
        self.__edges = set()

        for _ in range(vtx_num):
            self.add_vertex()

    def __dict__(self):
        def edge_dict_key(edg):
            return edg['beginning'], edg['end'], edg['label'], edg['round_trace'], edg['square_trace']

        return OrderedDict(
            alphabet=self.__alphabet,
            initials=sorted(list(self.__initials.keys())),
            finals=sorted(list(self.__finals.keys())),
            vertexes=sorted(list(self.__vertexes.keys())),
            edges=sorted([edg.__dict__() for edg in self.__edges], key=edge_dict_key),
        )

    def __contains__(self, item):
        return self.find_successful_path(item) is not None

    def __add__(self, other):
        if not self.is_context_sensitive() or not other.is_context_sensitive():
            raise TypeError('Can not unite recursively enumerable L-graphs')

        lg = LGraph(alphabet=''.join(sorted(set(self.alphabet) | set(other.alphabet))))

        for vtx in self.vertexes:
            lg.add_vertex(vtx_name=vtx.name)

        names_dict = dict()
        for vtx in other.vertexes:
            names_dict[vtx.name] = lg.add_vertex(vtx_name=vtx.name, adjust_name=True)

        for edg in self.edges:
            lg.add_edge(
                beg_vtx_name=edg.beg.name if edg.beg not in self.initials else lg.initial_main.name,
                end_vtx_name=edg.end.name if edg.end not in self.finals else lg.final_main.name,
                label=edg.label,
                round_trace=edg.round_trace,
                square_trace=edg.square_trace
            )

        for edg in other.edges:
            lg.add_edge(
                beg_vtx_name=names_dict[edg.beg.name] if edg.beg not in other.initials else lg.initial_main.name,
                end_vtx_name=names_dict[edg.end.name] if edg.end not in other.finals else lg.final_main.name,
                label=edg.label,
                round_trace=edg.round_trace,
                square_trace=edg.square_trace
            )

        lg.reduce()

        return lg

    def __mul__(self, other):
        if not self.is_context_sensitive() or not other.is_context_sensitive():
            raise TypeError('Can not concatenate recursively enumerable L-graphs')

        lg = LGraph(alphabet=''.join(sorted(set(self.alphabet) | set(other.alphabet))))

        for initial in self.initials:
            if initial.name != self.__initial_main_name:
                lg.add_vertex(vtx_name=initial.name)

        for final in other.finals:
            if final.name != self.__final_main_name:
                lg.add_vertex(vtx_name=final.name)

        for vtx in self.vertexes:
            lg.add_vertex(vtx_name=vtx.name)

        names_dict = dict()
        for vtx in other.vertexes:
            names_dict[vtx.name] = lg.add_vertex(vtx_name=vtx.name, adjust_name=True)

        transition_name = lg.add_vertex(vtx_name=self.__transition_prefix, adjust_name=True)

        max_round_trace_idx = 0
        max_square_trace_idx = 0

        for edg in self.edges:
            lg.add_edge(
                beg_vtx_name=edg.beg.name,
                end_vtx_name=edg.end.name if edg.end not in self.finals else transition_name,
                label=edg.label,
                round_trace=edg.round_trace,
                square_trace=edg.square_trace
            )
            max_round_trace_idx = max(max_round_trace_idx, edg.round_trace[1])
            max_square_trace_idx = max(max_square_trace_idx, edg.square_trace[1])

        for edg in other.edges:
            lg.add_edge(
                beg_vtx_name=names_dict[edg.beg.name] if edg.beg not in other.initials else transition_name,
                end_vtx_name=names_dict[edg.end.name] if edg.end not in other.finals else edg.end.name,
                label=edg.label,
                round_trace=(edg.round_trace[0], edg.round_trace[1] + max_round_trace_idx + 1),
                square_trace=(edg.square_trace[0], edg.square_trace[1] + max_square_trace_idx + 1)
            )

        lg.reduce()

        return lg

    def __imul__(self, other):
        return self * other

    def __iadd__(self, other):
        return self + other

    def __find_successful_path(self, start: Vertex, item: str, round_brackets: list, square_brackets: list):
        if not item and start in self.finals and not round_brackets and not square_brackets:
            return []

        allowed_edges = [edg for edg in start.edges if edg.label == '' or edg.label == (item[0] if item else '')]
        for edg in allowed_edges:
            new_round_brackets_stack = round_brackets.copy()
            new_square_brackets_stack = square_brackets.copy()

            if edg.round_trace[0] == '(':
                new_round_brackets_stack.append(edg.round_trace)
            elif edg.round_trace[0] == ')':
                if not new_round_brackets_stack or edg.round_trace[1] != new_round_brackets_stack[-1][1]:
                    return None
                new_round_brackets_stack = new_round_brackets_stack[:-1]

            if edg.square_trace[0] == '[':
                new_square_brackets_stack.append(edg.square_trace)
            elif edg.square_trace[0] == ']':
                if not new_square_brackets_stack or edg.square_trace[1] != new_square_brackets_stack[-1][1]:
                    return None
                new_square_brackets_stack = new_square_brackets_stack[:-1]

            path = self.__find_successful_path(edg.end, item[len(edg.label):],
                                               new_round_brackets_stack, new_square_brackets_stack)
            if path is not None:
                return [edg] + path
        return None

    @property
    def alphabet(self):
        return self.__alphabet

    @property
    def initials(self):
        return self.__initials.values()

    @property
    def finals(self):
        return self.__finals.values()

    @property
    def vertexes(self):
        return self.__vertexes.values()

    @property
    def edges(self):
        return self.__edges

    @property
    def initial_main(self):
        return self.__initials[self.__initial_main_name]

    @property
    def final_main(self):
        return self.__finals[self.__final_main_name]

    @property
    def vertex_names(self):
        return list(self.__vertexes) + list(self.__initials) + list(self.__finals)

    @property
    def number_of_vertexes(self):
        return len(self.__vertexes)

    @property
    def number_of_edges(self):
        return len(self.__edges)

    @property
    def type(self):
        return (
            LGraph.LGraphType.REGULAR if self.is_regular() else
            LGraph.LGraphType.CONTEXT_FREE if self.is_context_free() else
            LGraph.LGraphType.CONTEXT_SENSITIVE if self.is_context_sensitive() else
            LGraph.LGraphType.RECURSIVELY_ENUMERABLE
        )

    def add_vertex(self, vtx_name=None, adjust_name=False):
        vertex_dict = (
            self.__initials if vtx_name and vtx_name.startswith(self.__initial_prefix) else
            self.__finals if vtx_name and vtx_name.startswith(self.__final_prefix) else
            self.__vertexes
        )
        new_vtx_name = vtx_name if vtx_name else f'{len(self.__vertexes) + 1}'
        if vtx_name in self.vertex_names and not adjust_name:
            raise ValueError(f'Vertex with name "{vtx_name}" already exists.')
        elif vtx_name in self.vertex_names and adjust_name:
            i = 1
            while new_vtx_name in self.vertex_names:
                new_vtx_name = f'{vtx_name}_{i}'
                i += 1

        vertex_dict[new_vtx_name] = Vertex(name=new_vtx_name)
        return new_vtx_name

    def remove_vertex(self, vtx_name: str):
        if vtx_name in [self.__initial_main_name, self.__final_main_name]:
            raise ValueError(f'Can not remove vertex with name {vtx_name}')
        vtx_removed = (
            self.__initials.pop(vtx_name, None),
            self.__finals.pop(vtx_name, None),
            self.__vertexes.pop(vtx_name, None)
        )
        if not any(vtx_removed):
            raise ValueError(f'Vertex with name "{vtx_name}" was not found.')

    def get_vertex(self, vtx_name: str):
        vtx = (
            self.__vertexes[vtx_name] if vtx_name in self.__vertexes else
            self.__initials[vtx_name] if vtx_name in self.__initials else
            self.__finals[vtx_name] if vtx_name in self.__finals else
            None
        )
        if not vtx:
            raise ValueError(f'Vertex with name "{vtx_name}" was not found.')
        return vtx

    def rename_vertex(self, vtx_name: str, new_vtx_name: str):
        if new_vtx_name in self.vertex_names:
            raise ValueError(f'Vertex with name "{new_vtx_name}" already exists.')
        if vtx_name not in self.vertex_names:
            raise ValueError(f'Vertex with name "{vtx_name}" was not found.')
        vtx_dict = (
            self.__vertexes if vtx_name in self.__vertexes else
            self.__initials if vtx_name in self.__initials else
            self.__finals if vtx_name in self.__finals else
            None
        )
        vtx_dict[new_vtx_name] = vtx_dict[vtx_name]
        vtx_dict[new_vtx_name].rename(new_vtx_name)
        vtx_dict.pop(vtx_name, None)

    def add_edge(self, beg_vtx_name: str, end_vtx_name: str, label='', round_trace=('', 0), square_trace=('', 0)):
        if label not in self.alphabet:
            raise ValueError(f'Edge label "{label}"" is not from the alphabet.')

        beg_vtx, end_vtx = self.get_vertex(beg_vtx_name), self.get_vertex(end_vtx_name)
        edg = Edge(beg_vtx, end_vtx, label=label, round_trace=round_trace, square_trace=square_trace)
        self.__edges.add(edg)
        beg_vtx.add_edge(edg)

    def remove_edge(self, edg: Edge):
        try:
            self.__edges.remove(edg)
        except KeyError:
            raise ValueError(f'Edge from {edg.beg.name} to {edg.end.name} with label "{edg.label}", '
                             f'round trace {edg.round_trace} and square trace {edg.square_trace} was not found.')
        edg.beg.remove_edge(edg)

    def get_edges_between(self, beg_vtx: Vertex, end_vtx: Vertex):
        return [edg for edg in self.__edges if edg.beg == beg_vtx and edg.end == end_vtx]

    def save(self, path: str):
        with open(path, 'w') as file:
            print(json.dumps(self.__dict__(), indent=4), file=file)

    def load(self, path: str):
        with open(path, 'r') as file:
            data = json.load(file)
            self.__init__(vtx_num=0, alphabet=data['alphabet'])

            for vtx_set_name in ['initials', 'finals', 'vertexes']:
                for vtx_name in data[vtx_set_name]:
                    if vtx_name not in [self.__initial_main_name, self.__final_main_name]:
                        self.add_vertex(vtx_name)

            for edg in data['edges']:
                self.add_edge(
                    edg['beginning'], edg['end'],
                    label=edg['label'],
                    round_trace=tuple(edg['round_trace']),
                    square_trace=tuple(edg['square_trace'])
                )

    def find_successful_path(self, item: str):
        for initial in self.initials:
            path = self.__find_successful_path(initial, item, list(), list())
            if path:
                return path
        return None

    def reduce(self):
        edges_to_remove = list()
        edges_to_add = list()
        vertexes_to_remove = list()

        for vtx in self.vertexes:
            destinations = set(edg.end for edg in vtx.edges)
            if len(destinations) == 1 and all(edg.label == edg.round_trace[0] == edg.square_trace[0] == '' for edg in vtx.edges):
                destination = destinations.pop()
                vertexes_to_remove.append(vtx.name)
                for edg in self.edges:
                    if edg.end == vtx:
                        edges_to_add.append(dict(
                            beg_vtx_name=edg.beg.name,
                            end_vtx_name=destination.name,
                            label=edg.label,
                            round_trace=edg.round_trace,
                            square_trace=edg.square_trace
                        ))
                    if edg.beg == vtx or edg.end == vtx:
                        edges_to_remove.append(edg)

        for edg_dict in edges_to_add:
            self.add_edge(**edg_dict)
        for edg in edges_to_remove:
            self.remove_edge(edg)
        for vtx_name in vertexes_to_remove:
            self.remove_vertex(vtx_name)

    def is_regular(self):
        return not any(edg.round_trace[0] or edg.square_trace[0] for edg in self.__edges)

    def is_context_free(self):
        return not any(edg.square_trace[0] for edg in self.__edges)

    def is_context_sensitive(self):
        return not any(edg.square_trace[0] == '[' and not edg.label for edg in self.__edges)

    @staticmethod
    def path_to_string(path: list):
        if not path:
            return 'No path'
        result = ''.join(f'{edg.beg.name}--{edg.label}-->' for edg in path)
        return result + f'{path[-1].end.name}'
