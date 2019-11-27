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
def stable_outcome(market_graph, num_dummies, num_riders):
    p, M = matching_market.market_eq(market_graph.valuations, [0] * (num_dummies+num_riders))
    allocations = []
    for index, match in enumerate(M):
        if match >= num_riders:
            driver_allocation = "No match"
            rider_allocation = "Dummy - No Match"
            M[index] = "Dummy - No Match"
        else:
            driver_allocation = market_graph.valuations[index][match] - p[index]
            rider_allocation = p[index]
            if driver_allocation < 0:
                driver_allocation = "LOSS- No Match"
                rider_allocation = "Driver Loss - No Match"
        allocations.append((driver_allocation, rider_allocation))
    print("Prices: ", p)
    print("Matching: ", M)
    print("Allocation [(driver_allocation, rider_allocation):", allocations)
    return (M,allocations)


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
            edge_weight = rider_values[r_dx] - cost
            graph.add_directed_edge(driver, rider, edge_weight)
    print("Exchange graph created.")
    #graph.print_graph()
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
    print("Bipartite graph created. See valuations for each driver below:")
    print(valuations)
    market_graph = G.MarketGraph()
    market_graph.create_market_graph(num_drivers, num_riders + diff, valuations, prices)
    return stable_outcome(market_graph, diff, num_riders)


def generate_uber_examples_and_run(r, d, n=100):
    values = [1000]*r
    driver_locations = list()
    rider_locations = list()
    for driver in range(d):
        driver_locations.append((random.randint(0,n), (random.randint(0,n))))
    for rider in range(r):
        rider_locations.append((random.randint(0,n), (random.randint(0,n))))
        destinations.append((random.randint(0,n), (random.randint(0,n))))
    print("-------Starting!----")
    print("driver_locations: ", driver_locations)
    print("rider_locations: ", rider_locations)
    print("destinations: ", destinations)
    print("rider_values: ", rider_values)
    return create_bipartite_graph(driver_locations, rider_locations, destinations, values)


driver_locations = [(1,2), (2,3), (7,7), (9,9), (11,11)]
rider_locations = [(0,0), (1,1), (2,3), (5,4), (6,7)]
destinations = [(1,1), (2,1), (4, 5), (9,9), (11,11)]
rider_values = [30, 40, 20, 60, 1]
print("-------Starting!----")
print("driver_locations: ", driver_locations)
print("rider_locations: " , rider_locations)
print("destinations: " , destinations)
print("rider_values: ", rider_values)
exchange_graph = create_exchange_graph(driver_locations, rider_locations, destinations, rider_values)
create_bipartite_graph(driver_locations, rider_locations, destinations, rider_values)


driver_locations = [(0,0), (1,1), (2,3), (5,4), (6,7)]
rider_locations = [(1,2), (2,3), (7,7), (9,9), (11,11)]
destinations = [(1,1), (2,1), (4, 5), (9,9), (11,11)]
rider_values = [8, 8, 100, 20, 800]
print("-------Starting!----")
print("driver_locations: ", driver_locations)
print("rider_locations: " , rider_locations)
print("destinations: " , destinations)
print("rider_values: ", rider_values)
exchange_graph = create_exchange_graph(driver_locations, rider_locations, destinations, rider_values)
create_bipartite_graph(driver_locations, rider_locations, destinations, rider_values)

generate_uber_examples_and_run(r=10, d=10, n=100)
generate_uber_examples_and_run(r=5, d=20, n=100)
generate_uber_examples_and_run(r=20, d=5, n=100)



