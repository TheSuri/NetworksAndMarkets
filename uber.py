# Some helper functions for Part 5
# you may use these or define your own. Make sure it is clear where your solutions are
import graph as G
import numpy as np



# compute the manhattan distance between two points a and b (represented as pairs)
def dist(a,b):
    return abs(b[0]-a[0]) + abs(b[1]-a[1])

# Give a representation for riders/ drivers somewhere which can be included in your graph used in stable_outcome

# Given a (bipartite) graph G with edge values specified by v, 
# output a stable outcome (M,a) consisting of a matching and allocations
def stable_outcome(G,v):
    M = None
    a = None
    return (M,a)

#Example of how to create an n*n graph
def create_exchange_graph(driver_locations, rider_locations, destinations, rider_values):
    num_riders = len(rider_locations)
    num_drivers = len(driver_locations)

    graph = G.Graph()
    graph = G.create_graph(num_riders + num_drivers + 2, 0) # 1 source, 1 sink
    drivers = [graph.get_node(x) for x in range(num_drivers)]
    riders = [graph.get_node(x) for x in range(num_drivers, num_drivers + num_riders)]

    for d_dx, driver in enumerate(drivers):
        for r_dx, rider in enumerate(riders):
            cost = dist(driver_locations[d_dx], rider_locations[r_dx]) + dist(rider_locations[r_dx], destinations[r_dx])
            # print(driver_locations[d_dx], rider_locations[r_dx], destinations[r_dx])
            edge_weight = rider_values[r_dx] - cost
            # print(cost, rider_values[r_dx], edge_weight)
            graph.add_directed_edge(driver, rider, edge_weight)
    print("Please see Graph below: ")
    graph.print_graph()



driver_locations = [(1,2), (2,3)]
rider_locations = [(0,0), (1,1), (2,3)]
destinations = [(1,1), (2,1), (4, 5)]
rider_values = [3, 4, 2]
create_exchange_graph(driver_locations, rider_locations, destinations, rider_values)


