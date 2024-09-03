from tsp_parser import Parser
import traversal
from plotting import Plotting
import os
# test file
tsp_file = f"../tsp_files/11PointDFSBFS.tsp"

test_nodes = {'1': {"coordinates": (5.681818, 63.0), 'costs': {'2': 21.047512320599083, '3': 8.209853377784102, '4': 25.95058426467555}}, '2': {"coordinates": (11.850649, 83.983573), 'costs': {'3': 18.99134667015336}}, '3': {"coordinates": (13.798701, 65.092402), 'costs': {'4': 24.832953901070756, '5': 13.328048415912708}}, '4': {"coordinates": (16.883117, 40.451745), 'costs': {'5': 17.25084286599127, '6': 12.299021740618441, '7': 13.126129897963565}}, '5': {"coordinates": (23.782468, 56.262834), 'costs': {'7': 15.830456397643658, '8': 31.911829228876883}}, '6': {"coordinates": (25.0, 31.211499), 'costs': {'8': 8.691584532591625}}, '7': {"coordinates":( 29.951299, 41.683778), 'costs': {'9': 8.30976297874085, '10': 24.695349854195566}}, '8': {"coordinates": (31.331169, 25.256674), 'costs': {'9': 13.636152000469929, '10': 10.5818079365504, '11': 16.20664776621843}}, '9': {"coordinates": (37.175325, 37.577002), 'costs': {'11': 12.289043584330596}}, '10': {"coordinates": (39.935065, 19.096509), 'costs': {'11': 12.88564306835518}}, '11': {"coordinates": (46.834416, 29.979466), 'costs': {}}}
# test node object creation form parser
def node_creation(tsp_file):
    prsr1 = Parser(tsp_file, verbose = True) # using defaults other than verbosity (num_nodes=None, connection_type="directed", connection_src = "static",traps = False,loops = False,verbose = False)
    test_results = {}
    errors = {}
    for name in prsr1.nodes.keys():
        
        x,x_bool = prsr1.nodes[name]["coordinates"][0], prsr1.nodes[name]["coordinates"][0] == test_nodes[name]["coordinates"][0]
        y, y_bool = prsr1.nodes[name]["coordinates"][1], prsr1.nodes[name]["coordinates"][1] == test_nodes[name]["coordinates"][1]
        costs, costs_bool = prsr1.nodes[name]['costs'], prsr1.nodes[name]['costs'] == test_nodes[name]['costs']
        test_results[name] = {
            "coordinates": bool(x_bool*y_bool), "costs": costs_bool, 
            "vals": {"coordinates": (x, y), "costs": costs}
            }
        for results in test_results[name].items():
            if results[1] == False:
                key = results[0]
                error_category = f"{name}:node_creation"
                expected_val = test_nodes[name][key]
                resultant_val = test_results[name]["vals"][key]
                errors[error_category] = [f"{key} does not match {key}  ||  expected: {expected_val}, got: {resultant_val}"]

    print(errors)
if __name__ == "__main__":
    node_creation(tsp_file)