import os

import eel
import numpy as np

from Data import *
from report import *


if __name__ == '__main__':
    eel.init("web")
    eel.start("index.html", mode="edge")



@eel.expose
def collect_data11(array1, array2):
    cons, nodes = array1, array2
    g = Graph()
    g.create_graph(connections=cons, nodes=nodes)
    table, ways = g.find_min_route()
    additional_line = convert_data_to_html(goods=g.goods, needs=g.needs, rows=table, senders=g.senders,
                                           getters=g.getters, connections=cons, names=g.names, ways=ways)
    graph2 = add_final_graph(names=g.names, connections=cons)
    data = Data(
        np.array(g.goods_data),
        np.array(g.needs_data),
        np.array(table)
    )
    save_html_to_file(solve(data, additional_line, graph2, g), 'report.html')
    os.startfile('report.html')
    return ""





