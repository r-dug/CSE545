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
import json
import random
from datetime import datetime
from itertools import permutations
import gc
gc.set_threshold(0)

connections = {
    0:{0:False,1: True, 2:True, 3:True, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False, 10:False},
    1:{0:False,1: False, 2:True, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False, 10:False},
    2:{0:False,1: False, 2:False, 3:True, 4:True, 5:False, 6:False, 7:False, 8:False, 9:False, 10:False},
    3:{0:False,1: False, 2:False, 3:False, 4:True, 5:True, 6:True, 7:False, 8:False, 9:False, 10:False},
    4:{0:False,1: False, 2:False, 3:False, 4:False, 5:False, 6:True, 7:True, 8:False, 9:False, 10:False},
    5:{0:False,1: False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:True, 8:False, 9:False, 10:False},
    6:{0:False,1: False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:True, 9:True, 10:False},
    7:{0:False,1: False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:True, 9:True, 10:True},
    8:{0:False,1: False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False, 10:True},
    9:{0:False,1: False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False, 10:True},
    10:{0:False,1: False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False, 10:False}
}

def garbage_man(silent=False):
    unreachable_objects = gc.collect()
    if silent == False:
        print(f"Number of unreachable objects collected: {unreachable_objects}")

def create_nodes(file_obj, num_nodes, verbose):
        nodes = {}
        lines = file_obj.readlines()
        i = 0
        for line in lines:
            if i == 0 and line.strip().split()[0] != "1": 
                if verbose == True:
                    print("DISCARDED LINE",line)
                continue
            if num_nodes !=None and i >= num_nodes:
                break
            line = line.strip().split()
            if len(line) > 1:
                nodes[int(line[0])-1] = {"xy":(float(line[1]), float(line[2])), "costs": {}}
            i += 1
        return nodes

# this populates the connection table with pseudo random 
def random_connections(nodes, loops, traps):
    connections = {}
    node_names = list(nodes.keys())

    for i in node_names:
        connections[i]={}
        for j in node_names:
            if i == len(node_names) or i>=j: 
                connections[i][j] = False
                continue
            if random.randint(0,100)%5 == 0: 
                connections[i][j] = True
            else:
                connections[i][j] = False

        
        if (not True in connections[i].values()):
            connections[i][i+1] = True
    return connections

def fcg_costs(nodes):
    node_names = list(nodes.keys())
    for i in node_names:
        current = nodes[i]
        x1, y1 = current["xy"][0], current["xy"][1]
        for j in node_names:
            to_node = nodes[j]
            x2, y2 = to_node["xy"][0], to_node["xy"][1]
            current["costs"][j] = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return nodes

def dg_costs(nodes, connections):
    node_names = list(nodes.keys())
    for i in node_names:
        current = nodes[i]
        x1, y1 = current["xy"][0], current["xy"][1]
        for j in node_names:
            if connections[i][j] == True:
                to_node = nodes[j]
                x2, y2 = to_node["xy"][0], to_node["xy"][1]
                current["costs"][j] = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return nodes

class Parser:   
    def __init__(self, 
                 path, 
                 num_nodes=None, 
                 connection_type="directed", 
                 connection_src = "static",
                 traps = False,
                 loops = False,
                 verbose = False):
        
        # these class vars come from args and are relevant to functions
        self.file_obj = open(path)
        self.path = path
        self.num_nodes = num_nodes
        self.connection_type = connection_type
        self.verbose = verbose
        self.traps = traps
        self.loops = loops

        # as of 8/26/24, these object vars don't do anything. 
        self.name = self.file_obj.readline()
        self.comment = self.file_obj.readline()
        self.file_type = self.file_obj.readline()
        self.dimension = self.file_obj.readline()
        self.edge_type = self.file_obj.readline()
        self.header = self.file_obj.readline()

        # these are populated by functions
        self.nodes = create_nodes(self.file_obj, self.num_nodes, self.verbose)
        if connection_src == "static":
            self.connections = connections
        elif connection_src == "random":
            self.connections = random_connections(self.nodes, self.traps, self.loops)
        if self.connection_type == "full":
            self.nodes = fcg_costs(self.nodes)
        elif self.connection_type == "directed":
            self.nodes = dg_costs(self.nodes, self.connections)
        self.tour_costs = []
        self.runtimes = {}
 
    def print_nodes(self):
        print(json.dumps(self.nodes, indent=4))
    
    def print_tour_costs(self):
        for i in range(len(self.tour_costs)):
            print(self.tour_costs[i] )

    def clear(self):
        # these are populated by functions. I haven't found an actual use for clearing node values
        self.nodes = {}
        self.tour_costs = []
        self.runtimes = {}
    
    def override_costs(self, ct_or=None):
        if ct_or == None:
            print(
                """usage: Parser.add_costs(ct_or=['full', 'directed']) 
                # changes the cost attribute of the nodes to a desired graph type in lieu of instantiated class var.""")
        elif ct_or=="full":
            self.nodes['costs'] = fcg_costs(self.nodes)
        elif ct_or=="directed":
            self.nodes['costs'] = dg_costs(self.nodes)
        
    def sort_costs(self):
        node_names = list(self.nodes.keys())
        for name in node_names:
            # uses quick sort implementation? check docs
            self.nodes[name]["costs"] = dict(sorted(self.nodes[name]["costs"].items(), key=lambda item: item[1]))
