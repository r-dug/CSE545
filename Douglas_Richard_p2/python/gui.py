from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import time


test_nodes = {'1': {"coordinates": (5.681818, 63.0), 'costs': {'2': 21.047512320599083, '3': 8.209853377784102, '4': 25.95058426467555}}, '2': {"coordinates": (11.850649, 83.983573), 'costs': {'3': 18.99134667015336}}, '3': {"coordinates": (13.798701, 65.092402), 'costs': {'4': 24.832953901070756, '5': 13.328048415912708}}, '4': {"coordinates": (16.883117, 40.451745), 'costs': {'5': 17.25084286599127, '6': 12.299021740618441, '7': 13.126129897963565}}, '5': {"coordinates": (23.782468, 56.262834), 'costs': {'7': 15.830456397643658, '8': 31.911829228876883}}, '6': {"coordinates": (25.0, 31.211499), 'costs': {'8': 8.691584532591625}}, '7': {"coordinates":( 29.951299, 41.683778), 'costs': {'9': 8.30976297874085, '10': 24.695349854195566}}, '8': {"coordinates": (31.331169, 25.256674), 'costs': {'9': 13.636152000469929, '10': 10.5818079365504, '11': 16.20664776621843}}, '9': {"coordinates": (37.175325, 37.577002), 'costs': {'11': 12.289043584330596}}, '10': {"coordinates": (39.935065, 19.096509), 'costs': {'11': 12.88564306835518}}, '11': {"coordinates": (46.834416, 29.979466), 'costs': {}}}


class GraphApp:
    def __init__(self, parser):
        self.label = ''
        self.root = Tk()
        self.root.title(f"Visualization {self.label}")
        # Create text widget and specify size.
        self.T = Text(self.root, height = 5, width = 52)
        self.T.pack()

        # Create a frame for the matplotlib figure
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=BOTH, expand=True)

        # Create the graph and draw it
        self.parser = parser
        self.create_graph()
        self.draw_graph()

    def create_graph(self):
        nodes = self.parser.nodes
        print(nodes)
        self.graph = nx.DiGraph()
        self.edge_labels = {}
        self.edges = []
        self.pos = { }
        for node in nodes.keys():
            self.pos[node] = nodes[node]["xy"]
            # print(f"pos{node}: {self.pos[node]}")
            for connection in nodes[node]['costs'].keys():
                edge = (node, connection)
                # print(f"edge: {edge}")
                self.edges.append(edge)
                self.edge_labels[edge] = nodes[node]['costs'][connection]
                # print(f"{edge}: {self.edge_labels[edge]}")

    def draw_graph(self):
    # Adding nodes and edges
        self.graph.add_edges_from(self.edges, pos=self.pos, fixed=self.edges)

        # Create a figure
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Use the predefined coordinates for the node positions
        self.pos = {node: (data['xy'][0], data['xy'][1]) for node, data in self.parser.nodes.items()}

        # Draw the graph using the predefined layout
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=700, font_size=15)
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=self.edge_labels)

        # Embedding the plot in the Tkinter GUI
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def update(self, node_change, edge_change):
        self.ax.clear()  # Clear the previous frame
        node_change_idx = list(self.graph.nodes).index(node_change)
        edge_change_idx = list(self.graph.edges).index(edge_change)
        # Randomly generate colors for nodes and edges
        node_colors = ['blue' for _ in range(len(self.graph.nodes))]
        edge_colors = ['magenta' for _ in range(len(self.graph.edges))]
        node_colors[node_change_idx] = 'red'
        if edge_change != None:
            edge_colors[edge_change_idx] = 'yellow'
        
        # Draw the graph with updated colors
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=700, font_size=15)
        nx.draw_networkx_edge_labels(self.graph, self.pos,edge_labels=self.edge_labels)

        self.canvas.draw()


def animate (app, label, tour):
    app.label = label
    for i in range(len(tour)-1):
        edge = (tour[i], tour[i+1])
        cost = app.parser.nodes[edge[0]]["costs"][edge[1]]
        cost_info = f"Cost from {edge[0]} to {edge[1]}: {cost}\n"
        app.T.delete("0.0", END)
        app.T.insert(END, cost_info)
        app.update(edge[1], edge)
        app.root.update_idletasks()
        app.root.update()
        time.sleep(.5)
