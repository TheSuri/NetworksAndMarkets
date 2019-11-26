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


def market_eq(values, prices=None):
    num_buyers = len(values)
    if prices is None:
        prices = [0] * len(values[0])
    assert len(values[0]) == len(prices)
    num_sellers = len(prices)

    # assert num_buyers == len(values)
    # assert num_sellers == len(prices)
    market_graph = graph.MarketGraph()
    market_graph.create_market_graph(num_buyers, num_sellers, values, prices)
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
    prices = [0] * m
    p_original, M_original = market_eq(values, prices)
    social_value_original = sum([values[i][M_original[i]] for i in range(len(values)) ])
    for i in range(n):
        prices = [0] * m
        values_without_player_i = values[:i] + [[0 for x in range(len(values[i]))]] + values[i+1:]
        p_new, M_new = market_eq(values_without_player_i, prices)
        social_value_new =  sum([values_without_player_i[j][M_new[j]] for j in range(len(values_without_player_i))])
        # Dont include the valuation of the original in social_value_original hence subtracting values[i][M_original[i]]
        print(social_value_new, social_value_original, values[i][M_original[i]])
        p[i] = social_value_new - (social_value_original - values[i][M_original[i]])
    return p, M_original


def write_results_to_file_p7(fileName, values, n, p, M):
    f_7 = open(fileName, 'a')
    f_7.write("INPUTS:\n")
    f_7.write("Values(Valuation for each player) for " + str(n) + " items:\n")
    f_7.write("\n".join(str(item) for item in values))
    f_7.write("\nOUTPUTS:\n")
    f_7.write("p[i]:(p[i] shows how much player i will have to pay aka price of house assigined to i)\n")
    f_7.write(" ".join(str(item) for item in p))
    f_7.write("\nM[i]:(M[i] is the the house player i is assigned to aka index of item)\n")
    f_7.write(" ".join(str(item) for item in M))
    f_7.write('\n\n')
    f_7.close()


def write_results_to_file_p8(fileName, values, n, p, M):
    f_8 = open(fileName, 'a')
    f_8.write("INPUTS:\n")
    f_8.write("Values(Valuation for each player) for " + str(n) + " items:\n")
    f_8.write("\n".join(str(item) for item in values))
    f_8.write("\nOUTPUTS:\n")
    f_8.write("p[i]:(p[i] shows player i's externality)\n")
    f_8.write(" ".join(str(item) for item in p))
    f_8.write("\nM[i]:(M[i] is the the house player i is assigned to aka index of item)\n")
    f_8.write(" ".join(str(item) for item in M))
    f_8.write('\n\n')
    f_8.close()


def run_tests():
    valuations = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    p, M = market_eq(valuations, None)
    write_results_to_file_p7("p7.txt", valuations, 3, p, M)
    p, M = vcg(3, 3, valuations)
    write_results_to_file_p8("p8.txt", valuations, 3, p, M)

    valuations = [[4, 12, 5, 0, 0], [7, 10, 9, 0, 0], [7, 7, 10, 0, 0], [0, 0, 0, 10, 0], [0, 0, 0, 0, 11]]
    p, M = market_eq(valuations, [0, 0, 0, 0, 0])
    write_results_to_file_p7("p7.txt", valuations, 5, p, M)
    p, M = vcg(5, 5, valuations)
    write_results_to_file_p8("p8.txt", valuations, 5, p, M)

    valuations = [[2, 0, 7],
                  [10, 1, 9],
                  [9, 6, 3]]
    p, M = vcg(3, 3, valuations)


    for i in range(10):
        even = i % 2
        n = 5 if even else 10
        # n = 3
        valuations = []
        for j in range(n):
            valuations.append(random.sample(range(11), n))
        p, M = market_eq(valuations, None)
        write_results_to_file_p7("p7.txt", valuations, n, p, M)
        p, M = vcg(n, n, valuations)
        write_results_to_file_p8("p8.txt", valuations, n, p, M)


run_tests()


#Question 9:
def q_9_c():
    num_players, num_items = 20, 20
    # n = 3
    player_valuations = []
    for i in range(num_players):
        valuations = []
        valuation = random.sample(range(1, 51), 1)[0]
        for j in range(1, num_items+1):
            valuations.append(valuation * j)
        player_valuations.append(valuations)
    p, M = market_eq(player_valuations, None)
    write_results_to_file_p7("p9.txt", player_valuations, num_players, p, M)
    p, M = vcg(num_players, num_items, player_valuations)
    write_results_to_file_p8("p9.txt", player_valuations, num_players, p, M)

q_9_c()

