from tsp_parser import Parser
import traversal
from plotting import Plotting
import os
# test file
tsp_file = f"../tsp_files/11NodeDFSBFS.tsp"

test_nodes = {'1': {'x': 5.681818, 'y': 63.0, 'costs': {'2': 21.047512320599083, '3': 8.209853377784102, '4': 25.95058426467555}}, '2': {'x': 11.850649, 'y': 83.983573, 'costs': {'3': 18.99134667015336}}, '3': {'x': 13.798701, 'y': 65.092402, 'costs': {'4': 24.832953901070756, '5': 13.328048415912708}}, '4': {'x': 16.883117, 'y': 40.451745, 'costs': {'5': 17.25084286599127, '6': 12.299021740618441, '7': 13.126129897963565}}, '5': {'x': 23.782468, 'y': 56.262834, 'costs': {'7': 15.830456397643658, '8': 31.911829228876883}}, '6': {'x': 25.0, 'y': 31.211499, 'costs': {'8': 8.691584532591625}}, '7': {'x': 29.951299, 'y': 41.683778, 'costs': {'9': 8.30976297874085, '10': 24.695349854195566}}, '8': {'x': 31.331169, 'y': 25.256674, 'costs': {'9': 13.636152000469929, '10': 10.5818079365504, '11': 16.20664776621843}}, '9': {'x': 37.175325, 'y': 37.577002, 'costs': {'11': 12.289043584330596}}, '10': {'x': 39.935065, 'y': 19.096509, 'costs': {'11': 12.88564306835518}}, '11': {'x': 46.834416, 'y': 29.979466, 'costs': {}}}
# test node object creation form parser
def node_creation(tsp_file):
    prsr1 = Parser(tsp_file, verbose = True) # using defaults other than verbosity (num_nodes=None, connection_type="directed", connection_src = "static",traps = False,loops = False,verbose = False)
    test_results = {}
    errors = {}
    for name in prsr1.nodes.keys():
        
        x,x_bool = prsr1.nodes[name]['x'], prsr1.nodes[name]['x'] == test_nodes[name]['x']
        y, y_bool = prsr1.nodes[name]['y'], prsr1.nodes[name]['y'] == test_nodes[name]['y']
        costs, costs_bool = prsr1.nodes[name]['costs'], prsr1.nodes[name]['costs'] == test_nodes[name]['costs']
        test_results[name] = {
            "x": x_bool, "y": y_bool, "costs": costs_bool, 
            "vals": {"x": x, "y": y, "costs": costs}
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