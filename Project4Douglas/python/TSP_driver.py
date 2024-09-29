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
from genetic import Genetic

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
    # graphs by pop size (different logging files)
    Ns = [500, 1000, 5000]
    starts = ["strong", "random"]

    #  params other colors (string in log info under "params")
    p_ms = [0.001,0.01]
    mutations = ["swap", "inversion"]

    rrs = [20,40]
    # deepest nesting of loops. if elites false, don't iterate through creams
    elites = [False, True]
    creams = [2,5]
    # create time based graphs and generation based graphs

    # FullTraversal object can actually modify the parser object passed into it. neat.
    prsr1 = tsp_parser2.Parser(tsp_file, num_nodes=101)
    tsp_gui = gui.GraphApp(prsr1)
    for _ in range(5):
        for N in Ns:
            for start in starts:
                path = f"{log_dir}/{start}_pop_{N}.csv"
                for p_m in p_ms:
                    for mutation in mutations:
                        for rr in rrs:
                            for elite in elites:
                                if elite:
                                    for cream in creams:
                                        run = Genetic(prsr1.nodes, tsp_gui, N=N, start=start, p_m=p_m, mutate=mutation, rr=rr,
                                                        track_elite=elite, cream=cream)
                                        run.evolution()
                                        for generation in run.family_tree:
                                            cost_keys = list(generation.keys())
                                            cost_vals = [generation[key] for key in cost_keys]
                                            
                                            logging(
                                                path,
                                                cost_keys, 
                                                cost_vals
                                                )
                                else:
                                    run = Genetic(prsr1.nodes, tsp_gui, N=N, start=start, p_m=p_m, mutate=mutation, rr=rr,
                                                track_elite=elite)
                                    run.evolution()
                                    for generation in run.family_tree:
                                        cost_keys = list(generation.keys())
                                        cost_vals = [generation[key] for key in cost_keys]
                                        logging(
                                            path,
                                            cost_keys, 
                                            cost_vals
                                            )
    return prsr1

def logging(log_path, headers, run_info):
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
            log_writer.writerow(run_info)
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

    exit()
main()