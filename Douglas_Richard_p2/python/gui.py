from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import time
import random
import tsp_parser2

test_nodes = {'1': {"coordinates": (5.681818, 63.0), 'costs': {'2': 21.047512320599083, '3': 8.209853377784102, '4': 25.95058426467555}}, '2': {"coordinates": (11.850649, 83.983573), 'costs': {'3': 18.99134667015336}}, '3': {"coordinates": (13.798701, 65.092402), 'costs': {'4': 24.832953901070756, '5': 13.328048415912708}}, '4': {"coordinates": (16.883117, 40.451745), 'costs': {'5': 17.25084286599127, '6': 12.299021740618441, '7': 13.126129897963565}}, '5': {"coordinates": (23.782468, 56.262834), 'costs': {'7': 15.830456397643658, '8': 31.911829228876883}}, '6': {"coordinates": (25.0, 31.211499), 'costs': {'8': 8.691584532591625}}, '7': {"coordinates":( 29.951299, 41.683778), 'costs': {'9': 8.30976297874085, '10': 24.695349854195566}}, '8': {"coordinates": (31.331169, 25.256674), 'costs': {'9': 13.636152000469929, '10': 10.5818079365504, '11': 16.20664776621843}}, '9': {"coordinates": (37.175325, 37.577002), 'costs': {'11': 12.289043584330596}}, '10': {"coordinates": (39.935065, 19.096509), 'costs': {'11': 12.88564306835518}}, '11': {"coordinates": (46.834416, 29.979466), 'costs': {}}}


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualization")
        # Create text widget and specify size.
        self.T = Text(root, height = 5, width = 52)
        self.T.pack()

        # Create a frame for the matplotlib figure
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=BOTH, expand=True)

        # Create the graph and draw it
        self.create_graph(test_nodes)
        self.draw_graph()

    def create_graph(self, nodes):
        self.graph = nx.DiGraph()
        self.edge_labels = {}
        self.edges = []
        self.pos = { }
        for node in nodes.keys():
            self.pos[node] = nodes[node]["coordinates"]
            for connection in nodes[node]['costs']:
                edge = (node, connection)
                self.edges.append(edge)
                self.edge_labels[edge] = nodes[node]['costs'][connection]

    def draw_graph(self):
        # Adding nodes and edges
        self.graph.add_edges_from(self.edges, pos=self.pos, fixed=self.edges)
        # Create a figure
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Draw the graph using the Spring layout
        self.pos = nx.bfs_layout(self.graph, start='1')
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=700, font_size=15)
        nx.draw_networkx_edge_labels(self.graph, self.pos,edge_labels=self.edge_labels)
        # Embedding the plot in the Tkinter GUI
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def update(self, node_change, edge_change):
        self.ax.clear()  # Clear the previous frame
        
        # Randomly generate colors for nodes and edges
        node_colors = ['blue' for _ in range(len(self.graph.nodes))]
        edge_colors = ['magenta' for _ in range(len(self.graph.edges))]
        node_colors[node_change] = 'red'
        if edge_change != None:
            edge_colors[edge_change] = 'yellow'
        
        # Draw the graph with updated colors
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=700, font_size=15)
        nx.draw_networkx_edge_labels(self.graph, self.pos,edge_labels=self.edge_labels)

        self.canvas.draw()


if __name__ == "__main__":
    root = Tk()
    app = GraphApp(root)
    print(app.graph.nodes)
    print(app.graph.edges)
    while True:
        for i in range(len(app.graph.nodes)):
            node = list(app.graph.nodes)[i]
            print(test_nodes[node]["costs"])
            if node == '11':
                app.update(i, None)
                root.update_idletasks()
                root.update()
                time.sleep(10)
            for j in range(len(app.graph.edges)):
                edge = list(app.graph.edges)[j]
                if edge[0] == node:
                    cost = test_nodes[node]["costs"][edge[1]]
                    cost_info = f"Cost from {edge[0]} to {edge[1]}: {cost}\n"
                    app.T.delete("0.0", END)
                    app.T.insert(END, cost_info)
                    app.update(i, j)
                    root.update_idletasks()
                    root.update()
                    time.sleep(5)
