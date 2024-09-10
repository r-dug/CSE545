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
from collections import deque
import math
import gui

def calculate_cost(parser, path):
    cost = 0
    i = 0
    j = 1
    while j < len(path):
        cost += parser.nodes[path[i]]["costs"][path[j]]
        i += 1
        j += 1
    return cost
def dfs_rec(adj, visited, s, d, t, r, best_cost, lh, lhp, parser, tsp_gui):
    visited[s] = True
    temp = []
    # Recursively visit all adjacent vertices
    for i in adj[s]:
        
        if not visited[i]:
            
            temp = t.copy()  # Create a copy of the current path
            temp.append(i)   # Add the next node to the path
            cost = calculate_cost(parser, temp)
            if cost > best_cost[0]:
                continue
            if i == d:
                if len(temp) < lh[0]:
                    lh[0] = len(temp)
                    lhp[:] = temp
                if cost < best_cost[0]:
                    best_cost[0] = cost
                    r[:] = temp
            else:
                # Continue the recursion if destination not found
                dfs_rec(adj, visited, i, d, temp, r, best_cost, lh, lhp, parser, tsp_gui)
    # gui.animate(tsp_gui, "dfs", temp, d, best_cost)
    
    # Mark the current node as unvisited for other paths (backtracking)
    visited[s] = False

# the only difference we want here is to return the first valid result instead of all valid results
def greedy_rec(adj, visited, s, d, t, r, best_cost, lh, lhp, parser, tsp_gui):
    visited[s] = True
    temp = []
    # Recursively visit all adjacent vertices
    for i in adj[s]:
        
        if not visited[i]:
            
            temp = t.copy()  # Create a copy of the current path
            temp.append(i)   # Add the next node to the path
            cost = calculate_cost(parser, temp)
            if cost > best_cost[0]:
                continue
            if i == d:
                if len(temp) < lh[0]:
                    lh[0] = len(temp)
                    lhp[:] = temp
                if cost < best_cost[0]:
                    best_cost[0] = cost
                    r[:] = temp
                    break
            else:
                # Continue the recursion if destination not found
                greedy_rec(adj, visited, i, d, temp, r, best_cost, lh, lhp, parser, tsp_gui)
    # gui.animate(tsp_gui, "greedy", temp, d, best_cost)
    
    # Mark the current node as unvisited for other paths (backtracking)
    visited[s] = False
    # Mark the current node as unvisited for other paths (backtracking)
    visited[s] = False

def a_star_costs(parser, d):
    for node in parser.nodes:
        parser.nodes[node]["a_star_costs"] = {}
        for n in parser.nodes[node]["costs"]:
            to_next = parser.nodes[node]['costs'][n]
            next_x, next_y = parser.nodes[n]['xy']
            dest_x, dest_y = parser.nodes[d]['xy']
            dist = (dest_x-next_x)**2+(dest_y-next_y)**2
            to_dest = math.sqrt(dist)
            parser.nodes[node]["a_star_costs"][n] =  to_dest + to_next

def a_star_rec(parser, adj, visited, s, d, t):
    # Mark the current vertex as visited
    visited[s] = True
    
    # If the current node is the destination, return the path
    if s == d:
        return t

    # Recursively visit all adjacent vertices
    for i in adj[s]:
        if not visited[i]:
            # calculate sum of cost to next node and next node to destination
            temp = t.copy()  # Copy the current path to avoid modifying it
            temp.append(i)    # Add the next node to the path
            result = greedy_rec(adj, visited, i, d, temp)
            if result is not None:
                return result  # Return the first valid path found
    
    # Backtrack: unmark the current node as visited
    visited[s] = False

    # If no valid path is found in this branch, return None
    return None
def add_edge(adj, s, t):
    # Add edge from vertex s to t
    adj[s].append(t)
# not actually sure if we need to call all of these static methods. I read somewhere that this is not necessary in newer python versions.
class FullTraversal:
    @staticmethod
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
        return parser

    @staticmethod
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
        return parser

    @staticmethod
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
        return parser

    @staticmethod
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
        return parser

    @staticmethod
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
        return parser


# separate class for search functions in a directed graph...
# we aren't going to assume we know a starting node or a destination. let's get closer to this being real and useful - gosh....
class Directed:

    @staticmethod
    def bfs_cost(parser, start_node, dest_node, tsp_gui): # include branching rate? could that be useful in this context? the search space is finite, so maybe not...         
        start = datetime.now()  
        q = deque()
        V = [False] * len(parser.nodes.keys())  # Visited array

        # Start with the start node in the queue
        q.append((start_node, [start_node]))  # (current node, path leading to it)
        
        least_hops_path = None
        best_cost_path = None
        least_hops = float('inf')
        best_cost = float('inf')

        while q:
            # Pop the front of the queue (BFS explores level-by-level)
            curr, path = q.popleft()
            # gui.animate(tsp_gui, "bfs", path, dest_node, best_cost)

            # If we reach the destination, calculate the cost and hops
            cost = calculate_cost(parser, path)
            hops = len(path) - 1
            if cost < best_cost or hops > least_hops:
                continue
            if curr == dest_node:
                # Update least hops if applicable
                if hops < least_hops:
                    least_hops = hops
                    least_hops_path = path

                # Update best cost if applicable
                if cost < best_cost:
                    best_cost = cost
                    best_cost_path = path

                # Since this is BFS, we could break here if we're only concerned with the first valid path

            # Mark current node as visited
            V[curr] = True

            # Explore all adjacent nodes
            for neighbor, cost in parser.nodes[curr]["costs"].items():
                if not V[neighbor]:
                    # Append the neighbor node to the path and add it to the queue
                    q.append((neighbor, path + [neighbor]))
        runtime = datetime.now() - start
        # log collected data in parser object
        parser.tour_costs.append(
            {
                "algorithm":"bfs", 
                "input_size": len(list(parser.nodes.keys())), 
                "best_cost": best_cost,
                "best_cost_path": best_cost_path,
                "least_hops": least_hops, 
                "least_hops_path": least_hops_path,
                "runtime":runtime,
                "tsp_file": parser.path.split('/')[-1]
            })
    
    @staticmethod
    # we are simply going to iterate through paths numerically in this implementation and track the best path so far
    def dfs_cost(parser, start_node, dest_node, tsp_gui):
        
        start = datetime.now()
        # start by sorting the costs. simplifies algorithm
        adj = [[] for node in parser.nodes]
        for node in parser.nodes:
            for connection in parser.nodes[node]["costs"].items():
                add_edge(adj, node, connection[0])
        visited = [False] * len(adj)
        traversal = [start_node]
        best_cost = [float("inf")]
        best_cost_path = []
        least_hops = [float("inf")]
        least_hops_path = []
        dfs_rec(adj, visited, start_node, dest_node, traversal, best_cost_path, best_cost, least_hops, least_hops_path, parser, tsp_gui)
        runtime = datetime.now() - start
        # log collected data in parser object
        if best_cost[0] != float('inf'):
            parser.tour_costs.append(
                {
                    "algorithm":"dfs", 
                    "input_size": len(list(parser.nodes.keys())), 
                    "best_cost": best_cost[0],
                    "best_cost_path": best_cost_path,
                    "least_hops": least_hops[0], 
                    "least_hops_path": least_hops_path,
                    "runtime":runtime,
                    "tsp_file": parser.path.split('/')[-1]
                })
    
    @staticmethod
    # fast search using incredibly simple (very possibly BAD) heuristic of least cost to next node
    def greedy_cost(parser, start_node, dest_node, tsp_gui):
        start = datetime.now()
        # start by sorting the costs. simplifies algorithm
        parser.sort_costs()
        adj = [[] for _ in parser.nodes]
        for node in parser.nodes:
            for connection in parser.nodes[node]["costs"].items():
                add_edge(adj, node, connection[0])

        # simply look for the closest node and move to it if not visited.
        visited = [False] * len(adj)
        traversal = [start_node]
        best_cost = [float("inf")]
        best_cost_path = []
        least_hops = [float("inf")]
        least_hops_path = []
        greedy_rec(adj, visited, start_node, dest_node, traversal, best_cost_path, best_cost, least_hops, least_hops_path, parser, tsp_gui)

        runtime = datetime.now() - start
        # log collected data in parser object
        if best_cost[0] != float('inf'):
            parser.tour_costs.append(
                {
                    "algorithm":"greedy", 
                    "input_size": len(list(parser.nodes.keys())), 
                    "best_cost": best_cost[0],
                    "best_cost_path": best_cost_path,
                    "least_hops": least_hops[0], 
                    "least_hops_path": least_hops_path,
                    "runtime":runtime,
                    "tsp_file": parser.path.split('/')[-1]
                })
    
    @staticmethod
    # A better heuristic: which directly connected node is closest to the goal node
    def a_star(parser, start_node, dest_node):
        a_star_costs(parser, dest_node)
        for node in parser.nodes:
            print(node)
            print(parser.nodes[node]["a_star_costs"])
        
    
    @staticmethod
    # maybe an even better heuristic: which directly connected node has the lowest combined value of (dist from current + dist to goal)
    def ida_star(parser, start_node, dest_nodes):
        

        return
    