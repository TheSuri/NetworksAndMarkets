import graph as graph
import random

# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# 7 (a)
# implement an algorithm that given a bipartite graph G, outputs
# either a perfect matching or a constricted set
# Note: this will be used in 7 (b) so you can implement it however you
# like
def matching_or_cset(G: graph.MarketGraph):
    residual_graph, max_flow = graph.ford_fulkerson(G, G.source, G.sink)
    if max_flow == len(G.buyer_node_set):
        print("Max flow of", max_flow,  "achieved.")
        return residual_graph
    else:
        constricted_sellers = graph.find_constricted_set(residual_graph)
        return constricted_sellers

# 7 (b)
# implement an algorithm that given n (the number of players and items,
# which you can assume to just be labeled 0,1,...,n-1 in each case),
# and values where values[i][j] represents the ith players value for item j,
# output a market equilibrium consisting of prices and matching
# (p,M) where player i pays p[i] for item M[i]. 


def market_eq(n, values, prices=None):
    if prices is None:
        prices = [0]*n
    market_graph = graph.MarketGraph()
    market_graph.create_market_graph(n, values, prices)
    constricted_set_sellers = matching_or_cset(market_graph)
    # keep going till the function matching_or_cset returns
    # a residual graph instead of a constricted set
    while type(constricted_set_sellers) is set:
        market_graph.update_prices(constricted_set_sellers)
        #print("Constricted sellers from current iteration:")
        # for node in constricted_set_sellers:
            # print("node.id:", node.id, "curr price:", market_graph.get_node(node.id).price)
        market_graph.set_utilities()
        market_graph.create_best_valuation_edges()
        constricted_set_sellers = matching_or_cset(market_graph)
    #The constricted_set_sellers variable is actually the residual graph here:
    p, M = graph.get_matching(market_graph, constricted_set_sellers)
    return (p,M)

# 8 (b)
# Given n players 0,...,n-1 and m items 0,...,m-1 and valuations
# values such that values[i][j] is player i's valuation for item j,
# implement the VCG mechanism with Clarke pivot rule that outputs
# a set of prices and assignments (p,M) such that player i pays p[i]
# (which should be positive) for item M[i].
def vcg(n, m, values):
    p = [0]*n
    M = [0]*n
    return (p,M)


def write_results_to_file(fileName, values, n, p, M):
    f_7 = open(fileName, 'a')
    f_7.write("INPUTS:\n")
    f_7.write("Values(Valuation for each player) for " + str(n) + " houses:\n")
    f_7.write("\n".join(str(item) for item in values))
    f_7.write("\nOUTPUTS:\n")
    f_7.write("p[i]:(p[i] shows how much player i will have to pay aka price of house assigined to i)\n")
    f_7.write(" ".join(str(item) for item in p))
    f_7.write("\nM[i]:(M[i] is the the house player i is assigned to aka index of house)\n")
    f_7.write(" ".join(str(item) for item in M))
    f_7.write('\n\n')
    f_7.close()


valuations = [[4, 12, 5], [7,10,9], [7,7,10]]
p, M = market_eq(3, valuations, None)
write_results_to_file("p7.txt", valuations, 3, p, M)

valuations = [[4, 12, 5, 0, 0], [7, 10, 9, 0, 0], [7, 7, 10, 0, 0], [0, 0, 0, 10, 0], [0, 0, 0, 0, 11]]
p, M = market_eq(5, valuations, [0,0,0,0,0])
write_results_to_file("p7.txt", valuations, 5, p, M)

for i in range(10):
    even = i % 2
    n = 5 if even else 10
    valuations = []
    for j in range(n):
        valuations.append(random.sample(range(11), n))
    p, M = market_eq(n, valuations, None)
    write_results_to_file("p7.txt", valuations, n, p, M)







