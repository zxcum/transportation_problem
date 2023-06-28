from typing import Dict, Optional, Tuple

import numpy as np
import copy

class Data:
    """
    a - обьемы поставщиков;\n
    b - обьемы потребителей;\n
    c - матрица затрат на транспортировку;\n
    r - штраф за излишки/дефицит;\n
    (все значения в ед. товара)
    """

    def __init__(
        self, a: np.array, b: np.array, c: np.array, r: Optional[Dict[str, np.array]] = None,
    ) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.r = r if r is not None else {'a': np.full(self.m, 0), 'b': np.full(self.n, 0)}

        self.has_dummy_row = False
        self.has_dummy_column = False

    @property
    def m(self) -> int:
        """Количество поставщиков (строк матрицы c)."""
        return len(self.a)

    @property
    def n(self) -> int:
        """Количество потребителей (столбцов матрицы c)."""
        return len(self.b)

    def get_supply_demand_difference(self) -> int:
        """Получить разницу между спросом и предложением."""
        return sum(self.a) - sum(self.b)

    def add_dummy_supplier(self, volume: int) -> None:
        """Добавить фиктивного поставщика."""
        e = np.ones(self.n) * self.r['b']
        self.c = np.row_stack((self.c, e))
        self.a = np.append(self.a, volume)

        if np.all(e == 0):
            self.has_dummy_row = True

    def add_dummy_customer(self, volume: int) -> None:
        """Добавить фиктивного потребителя."""
        e = np.ones(self.m) * self.r['a']
        self.c = np.column_stack((self.c, e))
        self.b = np.append(self.b, volume)

        if np.all(e == 0):
            self.has_dummy_column = True

    def calculate_cost(self, x: np.ndarray) -> float:
        """Подсчет стоимости (целевой функции)."""
        return np.sum(self.c * np.nan_to_num(x))

    def calculate_potentials(self, x: np.ndarray) -> Dict[str, np.ndarray]:
        """Вычисление потенциалов."""
        res = {'a': [np.inf for _ in range(self.m)], 'b': [np.inf for _ in range(self.n)]}
        res['a'][0] = 0.0

        while np.inf in res['a'] or np.inf in res['b']:
            for i in range(self.m):
                for j in range(self.n):
                    if x[i][j] != 0:
                        if res['a'][i] != np.inf:
                            res['b'][j] = self.c[i][j] - res['a'][i]
                        elif res['b'][j] != np.inf:
                            res['a'][i] = self.c[i][j] - res['b'][j]

        return res

    def is_plan_optimal(self, x: np.ndarray, p: Dict[str, np.ndarray]) -> bool:
        """Проверка плана на оптимальность."""
        for i, j in zip(*np.nonzero(x == 0)):
            if p['a'][i] + p['b'][j] > self.c[i][j]:
                return False

        return True

    def get_best_free_cell(self, x: np.ndarray, p: Dict[str, np.ndarray]) -> Tuple[int, int]:
        free_cells = tuple(zip(*np.nonzero(x == 0)))
        return free_cells[np.argmax([p['a'][i] + p['b'][j] - self.c[i][j] for i, j in free_cells])]

    def __str__(self) -> str:
        return f'a: {self.a}\nb: {self.b}\n\nc:\n{self.c}\n\nr[a]: {self.r["a"]}\nr[b]: {self.r["b"]}'


class Node:
    def __init__(self, name, sup):
        self.connections = {}
        self.is_supply = sup
        self.Name = name
        self.short_ways = []



class Graph:
    def __init__(self):
        self.graph = {}
        self.senders = []
        self.getters = []
        self.table = []
        self.needs = {}
        self.goods = {}
        self.names = []
        self.nodes = []
        self.needs_data = []
        self.goods_data = []
        self.ways = []

    def create_graph(self, connections, nodes):
        for node in nodes:
            name = node[0]
            self.names.append(name)
            if name[-1] == '.':
                name = name[:-1]
                self.graph[int(name)] = Node(name=int(name), sup=True)
                self.senders.append(int(name))
                self.goods[int(name)] = int(node[1])
                self.nodes.append(int(name))
            else:
                self.graph[int(name)] = Node(name=int(name), sup=False)
                self.getters.append(int(name))
                self.needs[int(name)] = int(node[1])
                self.nodes.append(int(name))
        for connection in connections:
            node1 = int(connection[0])
            node2 = int(connection[1])
            weight = int(connection[2])
            if node1 not in self.graph or node2 not in self.graph:
                pass
            self.graph[node1].connections[node2] = weight
            self.graph[node2].connections[node1] = weight
        self.getters.sort()
        self.senders.sort()
        self.names.sort()
        for sender in self.senders:
            self.goods_data.append(self.goods[sender])
        for getter in self.getters:
            self.needs_data.append(self.needs[getter])

    def find_min_route(self):
        ways_full = []
        table = []
        for index_table, sender in enumerate(self.senders):
            table.append([])
            for getter in self.getters:
                q = [[sender, [sender]]]
                ways = []
                while q:
                    num = q.pop()
                    node = self.graph[num[0]]
                    for key in node.connections.keys():
                        if key in num[1]:
                            continue
                        elif key == getter:
                            way = copy.deepcopy(num[1])
                            way.append(key)
                            ways.append(way)
                            continue
                        else:
                            way = copy.deepcopy(num[1])
                            way.append(key)
                            q.append([key, way])
                min_length = np.inf
                short_way = []
                for way in ways:
                    cost = 0
                    for index, node in enumerate(way):
                        if index >= len(way) - 1:
                            continue
                        # print(way[index + 1], node, self.graph[node].connections)
                        cost += self.graph[node].connections[way[index + 1]]
                    if cost < min_length:
                        min_length = cost
                        short_way = way
                ways_full.append(short_way)
                table[index_table].append(min_length)
        print(ways_full)
        self.table = table
        self.ways = copy.deepcopy(ways_full)
        return table, ways_full





