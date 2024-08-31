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
import tsp_parser
from plotting import Plotting

gc.set_threshold(0) # collect garbage manually...
log_path = f"./logs/costs_{datetime.today().date()}.csv"

def find_salespeople():
    tsps = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.split('.')[-1] == "tsp":
                tsps.append(f"{os.path.join(root,file)}")
    return tsps

def create_nodes(num_nodes, tsp_file):
    parser =  tsp_parser.Parser(tsp_file, num_nodes)
    parser.create_nodes()
    parser.add_costs()
    return parser

def tour(tsp_file):
    tsp_file_name = tsp_file.split('/')[-1]
    print(f"iterating through: {tsp_file_name}")
    for num in range(2,13):
        parser = create_nodes(num, tsp_file)
        parser.brute_force()
        parser.brute_force_restart()
        parser.random()
        parser.sort_costs()
        parser.greedy()
        parser.random_restart(20000)

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
    try:
        with open(log_path, "r", newline='') as log_file:
                reader = csv.reader(log_file)
                header = next(reader)
    except Exception as e: 
        print(e)
    if header == None or header != headers:
        with open(log_path, "w", newline='') as log_file:
            log_writer = csv.writer(log_file)            
            log_writer.writerow(headers)
    else:
        with open(log_path, "a", newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(runtimes)

def garbage_man(silent=False):
    unreachable_objects = gc.collect()
    if silent == False:
        print(f"Number of unreachable objects collected: {unreachable_objects}")


if __name__ == "__main__":
    garbage_man()
    parser = None
    try:
        tsps = find_salespeople()
    except Exception as e:
        print(e)
        exit()
    
    try:
        for tsp in tsps:
            try:
                parser = tour(tsp)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        exit()
        
    garbage_man()
    tour_costs = parser.tour_costs
    algo_list = list(set([tour_cost['algorithm'] for tour_cost in tour_costs]))
    print(algo_list)
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