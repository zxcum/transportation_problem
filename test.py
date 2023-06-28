import os

import eel
import numpy as np

from Data import *
from report import *

test_data_cons = [
    [1, 2, 55],
    [1, 8, 75],
    [1, 3, 65],
    [2, 7, 20],
    [2, 6, 60],
    [2, 3, 45],
    [3, 8, 40],
    [3, 9, 30],
    [3, 6, 70],
    [7, 6, 45],
    [8, 9, 70],
    [8, 4, 100],
    [6, 5, 50],
    [9, 5, 30],
    [9, 4, 50],
    [5, 4, 40]
]
test_data_nodes = [
    ["1.", 110], ["2.", 200], ["3.", 300], ["4", 50], ["5", 120], ["6", 50], ["7", 80], ["8", 160], ["9", 140]
]

g = Graph()
g.create_graph(connections=test_data_cons, nodes=test_data_nodes)
table, ways = g.find_min_route()
additional_line = convert_data_to_html(goods=g.goods, needs=g.needs, rows=table, senders=g.senders,
                                           getters=g.getters, connections=test_data_cons, names=g.names, ways=ways)
graph2 = add_final_graph(names=g.names, connections=test_data_cons)
data = Data(
    np.array(g.goods_data),
    np.array(g.needs_data),
    np.array(table)
    )
save_html_to_file(solve(data, additional_line, graph2, g), 'report.html')
os.startfile('report.html')


# data = Data(
    #     np.array([12, 30, 13]),
    #     np.array([23, 40, 12, 32]),
    #     np.array([
    #  [64, 32, 45, 12],
    #     [32, 78, 23, 90],
    #     [88, 67, 10, 32],
    # ]),
    # )