from tsp_parser2 import Parser
from traversal import Directed
from traversal import FullTraversal
from plotting import Plotting
import os
import json
# test files
tsp_file_1 = f"./tsp_files/11NodeDFSBFS.tsp"
tsp_file_2 = "./tsp_files/a280.tsp"

def bfs(tsp_file):
    prsr1 = Parser(tsp_file, verbose = True)
    for num in [5,7,8,10]:
        Directed().bfs_cost(prsr1, 0, dest_node=num)
    for cost in prsr1.tour_costs:
        print(cost)

def bfs_rand(tsp_file):
    prsr1 = Parser(tsp_file, num_nodes=61, connection_src="random", verbose = True)
    for num in [5,7,8,10]:
        Directed().bfs_cost(prsr1, 0, dest_node=num)
    for cost in prsr1.tour_costs:
        print(cost)

def dfs(tsp_file):
    prsr1 = Parser(tsp_file, verbose = True)
    for num in [5,7,8,10]:
        Directed().dfs_cost(prsr1, 0, dest_node=num)
    for cost in prsr1.tour_costs:
        print(cost)

def dfs_rand(tsp_file):
    prsr1 = Parser(tsp_file, num_nodes=61,  connection_src="random", verbose = True)
    for num in [5,7,8,10]:
        Directed().dfs_cost(prsr1, 0, dest_node=num)
    for cost in prsr1.tour_costs:
        print(cost)

def greedy(tsp_file):
    prsr1 = Parser(tsp_file, num_nodes=61, verbose = True)
    for num in [5,7,8,10]:
        Directed().greedy_cost(prsr1, 0, dest_node=num)
    for cost in prsr1.tour_costs:
        print(cost)

def greedy_rand(tsp_file):
    prsr1 = Parser(tsp_file, num_nodes=61,  connection_src="random", verbose = True)
    for num in [5,7,8,10]:
        Directed().greedy_cost(prsr1, 0, dest_node=num)
    for cost in prsr1.tour_costs:
        print(cost)

def a_star(tsp_file):
    prsr1 = Parser(tsp_file, num_nodes=61, verbose = True)
    for num in [5,7,8,10]:
        Directed().a_star(prsr1, 0, 10)

if __name__ == "__main__":
    bfs(tsp_file_1)
    bfs_rand(tsp_file_1)
    bfs_rand(tsp_file_2)
    dfs(tsp_file_1)
    dfs_rand(tsp_file_1)
    dfs_rand(tsp_file_2)
    greedy(tsp_file_1)
    greedy_rand(tsp_file_1)
    greedy_rand(tsp_file_2)
    # a_star(tsp_file_1)