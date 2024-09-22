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
import gui
import tsp_parser2 
from traversal import FullTraversal, Directed
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


def tour(tsp_file):
    tsp_file_name = str(tsp_file.split('/')[-1])
    print(f"iterating through: {tsp_file_name}")
    
    m = "static"
    # FullTraversal object can actually modify the parser object passed into it. neat.
    prsr1 = tsp_parser2.Parser(tsp_file,connection_type="full", connection_src=m)
    tsp_gui = gui.GraphApp(prsr1)
    FullTraversal().greedy(prsr1, tsp_gui)
    FullTraversal().greedy_insertion(prsr1, tsp_gui)
    # FullTraversal().random_restart(prsr1, 100000, tsp_gui)
    for tour_cost in prsr1.tour_costs:
        cost_keys = list(tour_cost.keys())
        cost_vals = [tour_cost[key] for key in cost_keys]
        logging(
            log_path,
            cost_keys, 
            cost_vals
            )
    return prsr1

def logging(log_path, headers, runtimes):
    header = None
    # look for dir if not found, make it
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    if not os.path.isfile(log_path):
        with open(log_path, "w", newline='') as log_file:
            pass
    # try reading the headers, if none they don't match those found in log output write the file with appropriate headers
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
        # then append the logging results to the log file
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
    except Exception as e:
        print(e)
        exit()

    for tsp in tsps:
        parser = tour(tsp)

   
    garbage_man()
    try:
        tour_costs = parser.tour_costs
        algo_list = list(set([tour_cost['algorithm'] for tour_cost in tour_costs]))
    except Exception as e:
        print(e)
    
    
    Plotting.cost_plot(
        log_path, 
        hue_priority=algo_list,
        file_value=None)#tsps[0].split('/')[-1]

    
    garbage_man()


    Plotting.runtime_plot(
        log_path,
        hue_priority=algo_list,
        file_value=None)#tsps[0].split('/')[-1]

    
    garbage_man()
    exit()
main()