# Some helper functions for Part 5
# you may use these or define your own. Make sure it is clear where your solutions are
import graph as G
import matching_market as matching_market
import random

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
    return graph


def create_bipartite_graph(driver_locations, rider_locations, destinations, rider_values):
    num_riders = len(rider_locations)
    num_drivers = len(driver_locations)
    diff = 0
    if num_riders < num_drivers:
        diff = num_drivers - num_riders
    valuations = list()
    prices = [0]*(num_riders+diff)
    for driver_loc in driver_locations:
        valuation_driver = list()
        for r_dx, rider_loc in enumerate(rider_locations):
            cost = dist(driver_loc, rider_loc) + dist(rider_loc, destinations[r_dx])
            valuation_driver.append(rider_values[r_dx] - cost)
        min_valuation = min(valuation_driver)-1
        for d in range(diff):
            valuation_driver.append(0)
        valuations.append(valuation_driver)
    print(valuations)
    market_graph = G.MarketGraph()
    market_graph.create_market_graph(num_drivers, num_riders + diff, valuations, prices)
    p, M = matching_market.market_eq(valuations, prices)
    print("Cost to drivers",p)
    print(M)


def generate_uber_examples_and_run(r, d, n=100):
    values = [100]*r
    driver_locations = list()
    rider_locations = list()
    for driver in range(d):
        driver_locations.append((random.randint(0,n), (random.randint(0,n))))
    for rider in range(r):
        rider_locations.append((random.randint(0,n), (random.randint(0,n))))
        destinations.append((random.randint(0,n), (random.randint(0,n))))
    create_bipartite_graph(driver_locations, rider_locations, destinations, values)



driver_locations = [(1,2), (2,3)]
rider_locations = [(0,0), (1,1), (2,3)]
destinations = [(1,1), (2,1), (4, 5)]
rider_values = [3, 4, 2]
exchange_graph = create_exchange_graph(driver_locations, rider_locations, destinations, rider_values)
bipartite_graph = create_bipartite_graph(driver_locations, rider_locations, destinations, rider_values)


driver_locations = [(0,0), (3,3), (9,9)]
rider_locations = [(1,1), (4,4)]
destinations = [(0,0), (3,3)]
rider_values = [8, 8]
exchange_graph = create_exchange_graph(driver_locations, rider_locations, destinations, rider_values)
bipartite_graph = create_bipartite_graph(driver_locations, rider_locations, destinations, rider_values)


generate_uber_examples_and_run(r = 10, d = 10, n = 100)
generate_uber_examples_and_run(r = 5, d = 20, n = 100)
generate_uber_examples_and_run(r = 20, d = 5, n = 100)


