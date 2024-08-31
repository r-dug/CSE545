'''
The size of the tsp_parser file seemed to be getting a bit out of hand... so I am moving the traversal algorithms into a separate file
I'm simply going to import * from here, but I'm not sure if I'll want to... idk. I'm going to just leave this all here for now. 
maybe I'll have this class inherit the traversal... I haven't really decided. Mayby I'll just leave these here for now...

Ok. I thought about it and I think it will probably be the most appropriate to store traversal algorithms in here and a class,
    then in a driver script import both this class, the plotting class, and the parser class.
    In the driver script, Parser objects can still be instantiated, then passed into traversal algorithms from this class.
    
'''
from datetime import datetime
from itertools import permutations
import random
# import tsp_parser
class Traversal:
    def brute_force(parser):
        start = datetime.now()
        node_names = list(parser.nodes.keys())
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
                this_cost += parser.nodes[current_node]["costs"][next_node]
                i+=1
                j+=1
            this_cost += parser.nodes[current_node]["costs"][start_node]
            if best_cost == None or this_cost<best_cost:
                best_cost = this_cost
        runtime = datetime.now() - start
        parser.tour_costs.append(
            {"algorithm":"brute_force", 
                "input_size": len(node_names), 
                "cost": best_cost, 
                "runtime":runtime,
                "tsp_file": parser.path.split('/')[-1]})

    def brute_force_restart(parser):
        start = datetime.now()
        node_names = list(parser.nodes.keys())
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
                this_cost += parser.nodes[current_node]["costs"][next_node]
                if best_cost != None and this_cost > best_cost:
                    break
                i+=1
                j+=1
            this_cost += parser.nodes[current_node]["costs"][start_node]
            if best_cost == None:
                best_cost = this_cost
            elif this_cost < best_cost:
                best_cost = this_cost
        runtime = datetime.now() - start
        parser.tour_costs.append(
            {"algorithm":"brute_restart", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": parser.path.split('/')[-1]})

    def random(parser):
        start = datetime.now()
        node_names = list(parser.nodes.keys())
        current_node = parser.nodes[node_names[0]]
        best_cost = 0
        visited = [node_names[0]]
        while len(visited) < len(parser.nodes):
            prev_node = current_node
            rand_idx = random.randint(0, len(node_names)-1)
            curr_node_name = node_names[rand_idx]
            current_node = parser.nodes[curr_node_name]
            if not curr_node_name in visited:
                best_cost += prev_node["costs"][curr_node_name]
                visited.append(curr_node_name)
        best_cost += current_node["costs"][node_names[0]]
        visited.append(node_names[0])
        runtime = datetime.now() - start
        parser.tour_costs.append(
            {"algorithm":"random", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": parser.path.split('/')[-1]})

    def greedy(parser):
        start = datetime.now()
        node_names = list(parser.nodes.keys())
        current_node = parser.nodes[node_names[0]]
        visited = [node_names[0]]
        best_cost = 0
        i = 0
        while len(visited) < len(parser.nodes):
            cost_list = list(current_node["costs"].keys())
            potential_next = cost_list[i]
            if potential_next not in visited:
                prev_node = current_node
                current_node = parser.nodes[potential_next]
                best_cost += prev_node["costs"][potential_next]
                visited.append(potential_next)
                i = 0
            i += 1
        best_cost += current_node["costs"][node_names[0]]
        visited.append(node_names[0])
        runtime = datetime.now() - start
        parser.tour_costs.append(
            {"algorithm":"greedy", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": parser.path.split('/')[-1]})

    def random_restart(parser, runs):
        start = datetime.now()
        node_names = list(parser.nodes.keys())
        run = 0
        best_cost = None
        while run < runs:
            current_node = parser.nodes[node_names[0]]
            current_cost = 0
            visited = [node_names[0]]
            while len(visited) < len(node_names):
                rand_idx = random.randint(0, len(parser.nodes)-1)
                next_node_name = node_names[rand_idx]
                if not next_node_name in visited:
                    current_cost += current_node["costs"][next_node_name]
                    current_node = parser.nodes[next_node_name]
                    visited.append(next_node_name)
                    if best_cost != None and current_cost > best_cost:
                        continue
            current_cost += current_node["costs"][node_names[0]]
            visited.append(node_names[0])
            
            if best_cost == None:
                best_cost = current_cost
            elif current_cost < best_cost:
                best_cost = current_cost
            run+=1
        runtime = datetime.now() - start
        parser.tour_costs.append(
            {"algorithm":"random_restart", 
             "input_size": len(node_names), 
             "cost": best_cost, 
             "runtime":runtime,
             "tsp_file": parser.path.split('/')[-1]})

    def DFS(nodes):
        return
    
    def BFS(nodes):
        best_cost = None
        
        best_path = []
        queue = []
        head_cost = 
        return