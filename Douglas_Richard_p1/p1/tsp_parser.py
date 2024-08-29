"""
the following is an example of the format used in TSP files:
NAME : a280
COMMENT : drilling problem (Ludwig)
TYPE : TSP
DIMENSION: 280
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
  1 288 149
  2 288 129
  3 270 133
  4 256 141

*the first number is the city number, the other two are its coordinates.

this program creates an instance of nodes in the form of a dictionary
it also implements various functions to calculate costs for traversing nodes and logs the costs calculated for the various implemented algorithms
"""

import math
import random
from datetime import datetime
from itertools import permutations
import gc
gc.set_threshold(0)

# approximation of itertools permutation function as per the docs
# def permutations(iterable, r=None):
#     pool = tuple(iterable)
#     n = len(pool)
#     r = n if r == None else r 
#     if r>n: return 

#     indices = list(range(n))
#     cycles = list(range(n, n-r, -1))
#     yield tuple(pool[i] for i in indices[:r])

#     while n:
#         for i in reversed(range(n)):
#             cycles[i] -= 1
#             if cycles[i] == 0:
#                 indices[i:] = indices [i+1:] + indices[i:i+1]
#                 cycles[i] = n-1
#             else:
#                 j = cycles[i]
#                 indices[i], indices[-j] = indices[j], indices[i]
#                 yield tuple(pool[i] for i in indices[:r])
#         else: return
def garbage_man(silent=False):
    unreachable_objects = gc.collect()
    if silent == False:
        print(f"Number of unreachable objects collected: {unreachable_objects}")

class Parser:   
    def __init__(self, path, num_nodes=None, verbose = False):
        self.file_obj = open(path)
        self.path = path
        self.num_nodes = num_nodes
        self.verbose = verbose
        self.name = self.file_obj.readline()
        self.comment = self.file_obj.readline()
        self.file_type = self.file_obj.readline()
        self.dimension = self.file_obj.readline()
        self.edge_type = self.file_obj.readline()
        self.header = self.file_obj.readline()

        self.nodes = {}
        self.tour_costs = []
        self.runtimes = {}
 
    def print_nodes(self):
        for node in self.nodes:
            print(node)
    
    def print_tour_costs(self):
        for i in range(len(self.tour_costs)):
            # uses quick sort implementation? check docs
            print(self.tour_costs[i] )
    
    def create_nodes(self):
        lines = self.file_obj.readlines()
        i = 0
        for line in lines:
            if i == 0 and line.strip().split()[0] != "1": 
                if self.verbose == True:
                    print("DISCARDED LINE",line)
                continue
            if self.num_nodes !=None and i >= self.num_nodes:
                break
            line = line.strip().split()
            if len(line) > 1:
                self.nodes[line[0]] = {"x": float(line[1]), "y": float(line[2]), "costs": {}}
            i += 1

    def clear_nodes(self):
        self.nodes = []
        self.tour_costs = []

    def add_costs(self):
        node_names = list(self.nodes.keys())
        for i in node_names:
            current = self.nodes[i]
            x1 = current["x"]
            y1 = current['y']
            for j in node_names:
                to_node = self.nodes[j]
                x2 = to_node["x"]
                y2 = to_node["y"]
                current["costs"][j] = math.sqrt((x2-x1)**2+(y2-y1)**2)
    
    def sort_costs(self):
        node_names = list(self.nodes.keys())
        for name in node_names:
            # uses quick sort implementation? check docs
            self.nodes[name]["costs"] = dict(sorted(self.nodes[name]["costs"].items(), key=lambda item: item[1]))

    def brute_force(self):
        start = datetime.now()
        node_names = list(self.nodes.keys())
        node_perms = permutations(node_names)
        best_cost = None
        for perm in node_perms:
            perm = list(perm)
            start_node = perm[0]
            this_cost = 0
            i, j = 0, 1
            while j < len(perm):
                current_node = perm[i]
                next_node = perm[j]
                this_cost += self.nodes[current_node]["costs"][next_node]
                i+=1
                j+=1
            this_cost += self.nodes[current_node]["costs"][start_node]
            if best_cost == None or this_cost<best_cost:
                best_cost = this_cost
        runtime = datetime.now() - start
        self.tour_costs.append(
            {"algorithm":"brute_force", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": self.path.split('/')[-1]})

    def brute_force_restart(self):
        start = datetime.now()
        node_names = list(self.nodes.keys())
        node_perms = permutations(node_names)
        best_cost = None 
        for perm in node_perms:
            perm = list(perm)
            start_node = perm[0]
            this_cost = 0
            i, j = 0, 1
            while j < len(perm):
                current_node = perm[i]
                next_node = perm[j]
                this_cost += self.nodes[current_node]["costs"][next_node]
                if best_cost != None and this_cost > best_cost:
                    break
                i+=1
                j+=1
            this_cost += self.nodes[current_node]["costs"][start_node]
            if best_cost == None:
                best_cost = this_cost
            elif this_cost < best_cost:
                best_cost = this_cost
        runtime = datetime.now() - start
        self.tour_costs.append(
            {"algorithm":"brute_restart", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": self.path.split('/')[-1]})

    def random(self):
        start = datetime.now()
        node_names = list(self.nodes.keys())
        current_node = self.nodes[node_names[0]]
        best_cost = 0
        visited = [node_names[0]]
        while len(visited) < len(self.nodes):
            prev_node = current_node
            rand_idx = random.randint(0, len(node_names)-1)
            curr_node_name = node_names[rand_idx]
            current_node = self.nodes[curr_node_name]
            if not curr_node_name in visited:
                best_cost += prev_node["costs"][curr_node_name]
                visited.append(curr_node_name)
        best_cost += current_node["costs"][node_names[0]]
        visited.append(node_names[0])
        runtime = datetime.now() - start
        self.tour_costs.append(
            {"algorithm":"random", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": self.path.split('/')[-1]})

    def greedy(self):
        start = datetime.now()
        node_names = list(self.nodes.keys())
        current_node = self.nodes[node_names[0]]
        cost_list = list(current_node["costs"].keys())
        visited = [node_names[0]]
        best_cost = 0
        i = 0
        while len(visited) < len(self.nodes):
            potential_next = cost_list[i]
            if potential_next not in visited:
                prev_node = current_node
                current_node = self.nodes[potential_next]
                best_cost += prev_node["costs"][potential_next]
                visited.append(potential_next)
                i = 0
                cost_list = list(current_node["costs"].keys())
            i += 1
        best_cost += current_node["costs"][node_names[0]]
        visited.append(node_names[0])
        runtime = datetime.now() - start
        self.tour_costs.append(
            {"algorithm":"greedy", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": self.path.split('/')[-1]})

    def random_restart(self, runs):
        start = datetime.now()
        node_names = list(self.nodes.keys())
        run = 0
        best_cost = None
        while run < runs:
            current_node = self.nodes[node_names[0]]
            current_cost = 0
            visited = [node_names[0]]
            while len(visited) < len(node_names):
                rand_idx = random.randint(0, len(self.nodes)-1)
                next_node_name = node_names[rand_idx]
                if not next_node_name in visited:
                    current_cost += current_node["costs"][next_node_name]
                    current_node = self.nodes[next_node_name]
                    visited.append(next_node_name)
                    if best_cost != None and current_cost > best_cost:
                        break
            current_cost += current_node["costs"][node_names[0]]
            visited.append(node_names[0])
            
            if best_cost == None:
                best_cost = current_cost
            elif current_cost < best_cost:
                best_cost = current_cost
            run+=1
        runtime = datetime.now() - start
        self.tour_costs.append(
            {"algorithm":"random_restart", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": self.path.split('/')[-1]})
