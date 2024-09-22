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
        self.root.geometry("400x400")
        self.root.title(f"Visualization {self.label}")
        # Create text widget and specify size.
        self.T = Text(self.root, height = 10, width = 100)
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
        self.graph = nx.DiGraph()
        self.edges = []
        self.pos = { }
        for node in nodes.keys():
            self.pos[node] = nodes[node]["xy"]
            for connection in nodes[node]['costs'].keys():
                edge = (node, connection)
                self.edges.append(edge)

    def draw_graph(self):
    # Adding nodes and edges
        self.graph.add_edges_from(self.edges, pos=self.pos, fixed=self.edges)

        # Create a figure
        self.figure = plt.Figure(figsize=(100, 100))
        self.ax = self.figure.add_subplot(111)

        # Use the predefined coordinates for the node positions
        self.pos = {node: (data['xy'][0], data['xy'][1]) for node, data in self.parser.nodes.items()}

        # Draw the graph using the predefined layout
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=7, font_size=0)

        # Embedding the plot in the Tkinter GUI
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def update(self, edges, nodes, dest):
        self.ax.clear()  # Clear the previous frame
        dest_idx = list(self.graph.nodes).index(dest)
        e_indices = []
        v_indices = []
        
        for node in nodes:
            v_idx = list(self.graph.nodes).index(node)
            v_indices.append(v_idx)
        for edge in edges:
            e_idx = list(self.graph.edges).index(edge)
            e_indices.append(e_idx)
        # Randomly generate colors for nodes and edges
        node_colors = ['blue' for _ in range(len(self.graph.nodes))]
        edge_colors = ['magenta' for _ in range(len(self.graph.edges))]
        for v in v_indices:
            node_colors[v] = 'red'
        
        for e in e_indices:
            edge_colors[e] = 'yellow'
        node_colors[dest_idx] = 'green'
        
        # Draw the graph with updated colors
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_color=node_colors, node_size=7)
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=edges, ax=self.ax)
        # nx.draw_networkx_edge_labels(self.graph, self.pos,edge_labels=self.edge_labels)

        self.canvas.draw()
def save_animation(app, tour, filename):
    fig = app.figure
    def update_func(i):
        edge = (tour[i], tour[i+1])
        app.update(tour[i+1], edge)

    ani = animation.FuncAnimation(fig, update_func, frames=len(tour)-1, repeat=False)
    ani.save(filename, writer='ffmpeg', fps=50)  # Saving as .mp4


def animate (app, label, tour, dest, best_cost):
    app.label = label
    app.root.title(f"Visualization {label}")

    for i in range(len(tour)-1):
        edge = (tour[i], tour[i+1])
        cost = app.parser.nodes[edge[0]]["costs"][edge[1]]
        cost_info = f"Cost from {edge[0]} to {edge[1]}: {cost}\n best cost {best_cost}"
        app.T.delete("0.0", END)
        app.T.insert(END, cost_info)
        app.update([edge[1]], [edge], dest)
        app.root.update_idletasks()
        app.root.update()
        if edge[1] == dest: 
            success_msg = f"SUCCESSFUL PATH: {tour} \ncost: {best_cost}\n"
            app.T.delete("0.0", END)
            app.T.insert(END, success_msg)
            app.root.update_idletasks()
            app.root.update()
            time.sleep(1)
        time.sleep(.1)
def animate_path (app, label, tour, dest, best_cost):
    app.label = label
    app.root.title(f"Visualization {label}")
    edges = []
    for i in range(len(tour)-1):
        edge = (tour[i], tour[i+1])
        edges.append(edge)

    cost_info = f"path cost {best_cost}"
    app.T.delete("0.0", END)
    app.T.insert(END, cost_info)
    app.update(edges, tour, dest)
    app.root.update_idletasks()
    app.root.update()
    
    time.sleep(.1)
