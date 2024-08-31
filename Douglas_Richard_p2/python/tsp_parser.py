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
    '1':{'1':False,'2': True, '3':True, '4':True, '5':False, '6':False, '7':False, '8':False, '9':False, '10':False, '11':False},
    '2':{'1':False,'2': False, '3':True, '4':False, '5':False, '6':False, '7':False, '8':False, '9':False, '10':False, '11':False},
    '3':{'1':False,'2': False, '3':False, '4':True, '5':True, '6':False, '7':False, '8':False, '9':False, '10':False, '11':False},
    '4':{'1':False,'2': False, '3':False, '4':False, '5':True, '6':True, '7':True, '8':False, '9':False, '10':False, '11':False},
    '5':{'1':False,'2': False, '3':False, '4':False, '5':False, '6':False, '7':True, '8':True, '9':False, '10':False, '11':False},
    '6':{'1':False,'2': False, '3':False, '4':False, '5':False, '6':False, '7':False, '8':True, '9':False, '10':False, '11':False},
    '7':{'1':False,'2': False, '3':False, '4':False, '5':False, '6':False, '7':False, '8':False, '9':True, '10':True, '11':False},
    '8':{'1':False,'2': False, '3':False, '4':False, '5':False, '6':False, '7':False, '8':False, '9':True, '10':True, '11':True},
    '9':{'1':False,'2': False, '3':False, '4':False, '5':False, '6':False, '7':False, '8':False, '9':False, '10':False, '11':True},
    '10':{'1':False,'2': False, '3':False, '4':False, '5':False, '6':False, '7':False, '8':False, '9':False, '10':False, '11':True},
    '11':{'1':False,'2': False, '3':False, '4':False, '5':False, '6':False, '7':False, '8':False, '9':False, '10':False, '11':False}
}

def garbage_man(silent=False):
    unreachable_objects = gc.collect()
    if silent == False:
        print(f"Number of unreachable objects collected: {unreachable_objects}")
def fcg_costs(nodes):
    node_names = list(nodes.keys())
    for i in node_names:
        current = nodes[i]
        x1 = current["x"]
        y1 = current['y']
        for j in node_names:
            to_node = nodes[j]
            x2 = to_node["x"]
            y2 = to_node["y"]
            current["costs"][j] = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return nodes

def dg_costs(nodes):
    node_names = list(nodes.keys())
    for i in node_names:
        current = nodes[i]
        x1 = current["x"]
        y1 = current['y']
        for j in node_names:
            if connections[i][j] != False:
                to_node = nodes[j]
                x2 = to_node["x"]
                y2 = to_node["y"]
                current["costs"][j] = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return nodes

class Parser:   
    def __init__(self, 
                 path, 
                 num_nodes=None, 
                 connection="directed", 
                 verbose = False):
        # these class vars come from args and are relevant to functions
        self.file_obj = open(path)
        self.path = path
        self.num_nodes = num_nodes
        self.connection_type = connection
        self.verbose = verbose

        # as of 8/26/24, these nodes don't do anything. 
        self.name = self.file_obj.readline()
        self.comment = self.file_obj.readline()
        self.file_type = self.file_obj.readline()
        self.dimension = self.file_obj.readline()
        self.edge_type = self.file_obj.readline()
        self.header = self.file_obj.readline()

        # these are populated by functions
        self.nodes = {}
        self.tour_costs = []
        self.runtimes = {}
 
    def print_nodes(self):
        print(json.dumps(self.nodes, indent=4))
    
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

    def clear(self):
                # these are populated by functions
        self.nodes = {}
        self.tour_costs = []
        self.runtimes = {}
    
    def add_costs(self, ct_or=None):
        if self.connection_type == "full" or ct_or=="full":
            self.nodes = fcg_costs(self.nodes)
        elif self.connection_type == "directed" or ct_or=="directed":
            self.nodes = dg_costs(self.nodes)
        
    def sort_costs(self):
        node_names = list(self.nodes.keys())
        for name in node_names:
            # uses quick sort implementation? check docs
            self.nodes[name]["costs"] = dict(sorted(self.nodes[name]["costs"].items(), key=lambda item: item[1]))
