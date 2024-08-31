'''
The size of the tsp_parser file seemed to be getting a bit out of hand... so I am moving the traversal algorithms into a separate file
I'm simply going to import * from here, but I'm not sure if I'll want to... idk. I'm going to just leave this all here for now. 
maybe I'll have this class inherit the traversal... I haven't really decided. Mayby I'll just leave these here for now...
'''
from datetime import datetime
from itertools import permutations
import random
import tsp_parser
class Traversal:
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
        visited = [node_names[0]]
        best_cost = 0
        i = 0
        while len(visited) < len(self.nodes):
            cost_list = list(current_node["costs"].keys())
            potential_next = cost_list[i]
            if potential_next not in visited:
                prev_node = current_node
                current_node = self.nodes[potential_next]
                best_cost += prev_node["costs"][potential_next]
                visited.append(potential_next)
                i = 0
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
                        continue
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
