import numpy as np
import collections


class Node:
    def __init__(self, id):
        self.id = id
        self.edges = list()
        self.infected = False
        self.num_infected_neighbors = 0

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_all_edges(self):
        self.edges = list()


class DirectedEdge:
    def __init__(self, node_from, node_to, weight=1):
        self.weight = weight
        self.node_from = node_from
        self.node_to = node_to


class Graph:
    def __init__(self):
        self.nodes = dict()

    def add_node(self, node):
        self.nodes[node.id] = node

    def get_node(self, id):
        return self.nodes.get(id)

    def add_undirected_edge(self, node1, node2):
        if type(node1) is int and type(node2) is int:
            node1, node2 = self.nodes[node1], self.nodes[node2]
        edge1 = DirectedEdge(node1, node2)
        edge2 = DirectedEdge(node2, node1)
        node1.add_edge(edge1)
        node2.add_edge(edge2)

    def add_directed_edge(self, node1, node2, weight):
        if type(node1) is str or type(node1) is int or type(node1) is float:
            node1 = self.nodes[node1]
        if type(node2) is str or type(node2) is int or type(node2) is float:
            node2 = self.nodes[node2]
        edge1 = DirectedEdge(node1, node2)
        edge1.weight = weight
        node1.add_edge(edge1)

    def infect_single_node(self, node_id):
        curr_node = self.nodes[node_id]
        curr_node.infected = True
        for edge in curr_node.edges:
            node_to = edge.node_to
            node_to.num_infected_neighbors += 1

    def print_graph(self):
        for node in self.nodes:
            print("Node:", node)
            print("Edges:")
            for edge in self.nodes[node].edges:
                print("\t", edge.node_to.id, "\t", "weight:", edge.weight)


class BuyerNode(Node):
    def __init__(self, id: str, valuations: list):
        super().__init__(id)
        self.valuations = valuations
        self.utilities = list()
        self.max_utility_indices = list()
        self.max_utility = int()

    def calculate_utilities(self, curr_prices: list):
        self.max_utility_indices = list()

        if len(self.utilities) < len(curr_prices):
            self.utilities = [None] * len(curr_prices)

        for i, value in enumerate(self.valuations):
            self.utilities[i] = value - curr_prices[i]
        self.max_utility = max(self.utilities)
        for i, utility in enumerate(self.utilities):
            if utility == self.max_utility:
                self.max_utility_indices.append(i)


class SellerNode(Node):
    def __init__(self, id: str, price: int):
        super().__init__(id)
        self.price = price

    def set_price(self, price):
        self.price = price


class MarketGraph(Graph):
    def __init__(self):
        super().__init__()
        self.source = Node(float('-inf'))
        self.sink = Node(float('inf'))
        self.buyer_node_set = set()
        self.seller_node_set = set()
        self.prices = list()
        self.add_node(self.source)
        self.add_node(self.sink)

    def create_market_graph(self, num_buyers, num_sellers, valuations, prices):
        self.prices = prices
        for i in range(num_buyers):
            buyer_node = BuyerNode('b' + str(i), valuations[i])
            self.add_node(buyer_node)
            self.add_directed_edge(self.source, buyer_node, 1)
            self.buyer_node_set.add(buyer_node)
        for i in range(num_sellers):
            seller_node = SellerNode('s' + str(i), prices[i])
            self.add_node(seller_node)
            self.seller_node_set.add(seller_node)
            self.add_directed_edge(seller_node, self.sink, 1)
        self.set_utilities()
        self.create_best_valuation_edges()

    def set_utilities(self):
        for buyer_node in self.buyer_node_set:
            buyer_node.calculate_utilities(self.prices)
            # print(buyer_node.id, buyer_node.utilities)

    def remove_all_edges(self):
        for buyer_node in self.buyer_node_set:
            buyer_node.remove_all_edges()

    def create_best_valuation_edges(self):
        self.remove_all_edges()
        for buyer_node in self.buyer_node_set:
            for max_utility_index in buyer_node.max_utility_indices:
                self.add_directed_edge(buyer_node, self.get_node('s' + str(max_utility_index)), 1)

    def update_prices(self, constricted_set_sellers):
        constricted_seller_list = [self.get_node(x.id) for x in constricted_set_sellers]
        for constricted_seller in constricted_seller_list:
            constricted_seller.price = constricted_seller.price + 1
            self.prices[int(constricted_seller.id[1:])] = constricted_seller.price
        for seller in self.seller_node_set:
            if seller.price == 0:
                return
        # downgrading all prices in case there are no prices = 0
        for seller in self.seller_node_set:
            seller.price = seller.price - 1
            self.prices[int(seller.id[1:])] = seller.price


def get_matching(original_graph, residual_graph):
    path_dict = find_path(residual_graph, residual_graph.get_node(float('inf')),
                          residual_graph.get_node(float('-inf')))
    p = [None] * len(original_graph.buyer_node_set)
    M = [None] * len(original_graph.buyer_node_set)
    for buyer_node in original_graph.buyer_node_set:
        house_assigned = path_dict[residual_graph.get_node(buyer_node.id)]
        M[int(buyer_node.id[1:])] = int(house_assigned.id[1:])
        p[int(buyer_node.id[1:])] = original_graph.get_node(house_assigned.id).price
    return p, M


def create_graph(n, probability):
    graph = Graph()
    for i in range(n):
        node = Node(i)
        graph.add_node(node)
    if probability <= 0:
        return graph
    for i in range(n):
        for j in range(i + 1, n):
            if coin_flip(probability):
                graph.add_undirected_edge(graph.get_node(i), graph.get_node(j))
    print("Done creating nodes of Graph")
    return graph


def coin_flip(prob):
    return np.random.binomial(1, prob, 1)[0] == 1


def ford_fulkerson(graph: Graph, source: Node, sink: Node):
    residual_graph = create_residual_graph(graph)
    # print("-----------Residual Graph before FF ----------")
    # residual_graph.print_graph()
    source, sink = residual_graph.get_node(source.id), residual_graph.get_node(sink.id)
    parent_dict = find_path(residual_graph, source, sink)
    max_flow = 0
    while sink in parent_dict:
        min_edge = find_min_edge(parent_dict, sink)
        max_flow += min_edge
        residual_graph = update_residual_graph(residual_graph, parent_dict, min_edge, sink)
        parent_dict = find_path(residual_graph, source, sink)
    # find_min_cut_max_flow(residual_graph)
    # print("-----------Residual Graph after FF ----------")
    # residual_graph.print_graph()
    return residual_graph, max_flow


def create_residual_graph(original_graph):
    residual_graph = Graph()
    for node_id in original_graph.nodes.keys():
        node = Node(node_id)
        residual_graph.add_node(node)
    for node in original_graph.nodes.values():
        for edge in node.edges:
            residual_graph.add_directed_edge(edge.node_from.id, edge.node_to.id, edge.weight)
            residual_graph.add_directed_edge(edge.node_to.id, edge.node_from.id, 0)
    return residual_graph


def update_residual_graph(residual_graph: Graph, parent_dict: dict, min_edge_weight: int, sink: Node):
    curr = sink
    while (parent_dict[curr] != None):
        parent = parent_dict[curr]
        for parent_edge in parent.edges:
            if parent_edge.node_to == curr:
                parent_edge.weight = parent_edge.weight - min_edge_weight
        for curr_edge in curr.edges:
            if curr_edge.node_to == parent:
                curr_edge.weight = curr_edge.weight + min_edge_weight
        curr = parent
    return residual_graph


def find_min_edge(parent_dict: dict, target: Node):
    min_edge_weight = float('inf')
    curr = target
    route = []
    while parent_dict[curr] is not None:
        parent = parent_dict[curr]
        route.append(parent.id)
        for parent_edge in parent.edges:
            if parent_edge.node_to == curr:
                min_edge_weight = min(parent_edge.weight, min_edge_weight)
                break
        curr = parent
    return min_edge_weight


def find_path(residual_graph: Graph, source: Node, sink: Node):
    parent_dict = {source: None}
    visited_set = set()
    q = collections.deque()
    q.append(source)
    while q:
        curr_node = q.popleft()
        visited_set.add(curr_node)
        if curr_node == sink:
            break
        for edge in curr_node.edges:
            if edge.weight > 0 and edge.node_to not in visited_set:
                q.append(edge.node_to)
                parent_dict[edge.node_to] = curr_node
    return parent_dict


# n is number of drivers and number of riders
def create_random_bipartite_graph(n: int, p: float):
    graph = Graph()
    graph = create_graph((n * 2) + 2, 0)
    source = graph.get_node(0)
    sink = graph.get_node((n * 2) + 1)
    drivers = [graph.get_node(x) for x in range(1, n + 1)]
    riders = [graph.get_node(x) for x in range(n + 1, (2 * n) + 1)]
    # add edges from source to drivers
    for driver in drivers:
        graph.add_directed_edge(source, driver, 1)
    # add edges from sink to riders
    for rider in riders:
        graph.add_directed_edge(rider, sink, 1)
    # add edges from drivers to riders based on probability
    for driver in drivers:
        for rider in riders:
            if coin_flip(p):
                graph.add_directed_edge(driver, rider, 1)
    return graph, source, sink


def run_simulations():
    results = dict()
    n = 100
    for p in np.arange(0.0, 1.01, 0.05):
        graph, source, sink = create_random_bipartite_graph(n, p)
        residual_graph, max_flow = ford_fulkerson(graph, source, sink)
        results[p] = max_flow / 100
    return results


def find_constricted_set(residual_graph):
    source = residual_graph.get_node(float('-inf'))
    sink = residual_graph.get_node(float('inf'))
    parent_dict = find_path(residual_graph, source, sink)
    constricted_set_buyers = set()
    constricted_set_sellers = set()
    for node in parent_dict:
        if type(node.id) is str and node.id[0] == 'b' and parent_dict[node] == source:
            constricted_set_buyers.add(node)
        elif type(node.id) is str and node.id[0] == 's':
            constricted_set_sellers.add(node)
    return constricted_set_sellers

