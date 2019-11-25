# Some helper functions for Part 5
# you may use these or define your own. Make sure it is clear where your solutions are
import graph as G
import numpy as np



# compute the manhattan distance between two points a and b (represented as pairs)
def dist(a,b):
    return -1

# Give a representation for riders/ drivers somewhere which can be included in your graph used in stable_outcome

# Given a (bipartite) graph G with edge values specified by v, 
# output a stable outcome (M,a) consisting of a matching and allocations
def stable_outcome(G,v):
    M = None
    a = None
    return (M,a)



#Example of how to create an n*n graph
def create_bipartite_graph(riders:int, drivers:int, p:float):
    graph = G.Graph()
    graph = G.create_graph(riders + drivers + 2, 0) # 1 source, 1 sink
    source = graph.get_node(0)
    sink = graph.get_node((riders+drivers)+1)
    drivers = [graph.get_node(x) for x in range(1, drivers+1)]
    riders = [graph.get_node(x) for x in range(drivers + 1, drivers + riders + 2)]
    #add edges from source to drivers
    # for driver in drivers:
    # graph.add_directed_edge(source, driver, 1)
    # #add edges from sink to riders
    # for rider in riders:
    #     graph.add_directed_edge(rider, sink, 1)
    #   #add edges from drivers to riders based on probability
    #   for driver in drivers:
    #     for rider in riders:
    #       if coin_flip(p):
    #         graph.add_directed_edge(driver, rider, 1)
    #   return graph, source, sink


def coin_flip(prob):
  return np.random.binomial(1, prob, 1)[0] == 1




