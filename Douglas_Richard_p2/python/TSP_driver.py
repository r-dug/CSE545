"""
Author: Richard Douglas
Description:
this is the driver script to iterate through all sample tsp files
it runs various algorithms to find a hamiltonian circuit on a set of nodes
it logs the calculated costs and runtimes for those algorithms on each file 
"""

import sys
import os
from datetime import datetime
import csv
import gc
# add libraries from the cwd into the PATH to allow local imports
sys.path.append(os.getcwd())
import tsp_parser2 
from traversal import FullTraversal
from plotting import Plotting

gc.set_threshold(0) # collect garbage manually...
log_fn = f"costs_{datetime.today().date()}.csv"
log_dir = "./logs"
log_path = f"{log_dir}/{log_fn}"

def find_salespeople():
    tsps = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.split('.')[-1] == "tsp":
                tsps.append(f"{os.path.join(root,file)}")
    return tsps


def tour(tsp_file, connection_type):
    tsp_file_name = tsp_file.split('/')[-1]
    print(f"iterating through: {tsp_file_name}")
    for num in range(2,10):
        parser = tsp_parser2.Parser(tsp_file, num_nodes=num, connection_type=connection_type)
        # FullTraversal object can actually modify the parser object passed into it. neat.
        FullTraversal.brute_force(parser)
        FullTraversal.brute_force_restart(parser)
        FullTraversal.random(parser)
        parser.sort_costs()
        FullTraversal.greedy(parser)
        FullTraversal.random_restart(parser, 20000)

        for tour_cost in parser.tour_costs:
            cost_keys = list(tour_cost.keys())
            cost_vals = [tour_cost[key] for key in cost_keys]
            logging(
                log_path,
                cost_keys, 
                cost_vals
                )
    return parser

def logging(log_path, headers, runtimes):
    header = None
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    if not os.path.isfile(log_path):
        with open(log_path, "w", newline='') as log_file:
            pass
    try:
        with open(log_path, "r", newline='') as log_file:
                reader = csv.reader(log_file)
                header = next(reader)
    except Exception as e: 
        print(e)
    try:
        if header == None or header != headers:
            with open(log_path, "w", newline='') as log_file:
                log_writer = csv.writer(log_file)            
                log_writer.writerow(headers)
        else:
            with open(log_path, "a", newline='') as log_file:
                log_writer = csv.writer(log_file)
                log_writer.writerow(runtimes)
    except Exception as e:
        print(e)
def garbage_man(silent=False):
    unreachable_objects = gc.collect()
    if silent == False:
        print(f"Number of unreachable objects collected: {unreachable_objects}")


def main():
    garbage_man()
    parser = None
    try:
        tsps = find_salespeople()
        # print(tsps)
    except Exception as e:
        print(e)
        exit()
    try:
        for tsp in tsps:
            parser = tour(tsp, "full")
    except Exception as e:
        print(e)
   
    garbage_man()
    try:
        tour_costs = parser.tour_costs
        algo_list = list(set([tour_cost['algorithm'] for tour_cost in tour_costs]))
    except Exception as e:
        print(e)
    
    try:
        Plotting.cost_plot(
            log_path, 
            hue_priority=algo_list,
            file_value=None)#tsps[0].split('/')[-1]
    except Exception as e:
        print(e)
        exit()
    
    garbage_man()

    try:
        Plotting.runtime_plot(
            log_path,
            hue_priority=algo_list,
            file_value=None)#tsps[0].split('/')[-1]
    except Exception as e:
        print(e)
        exit()
    
    garbage_man()
    exit()
main()