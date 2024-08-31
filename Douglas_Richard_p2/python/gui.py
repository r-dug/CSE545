import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualization")

        # Create a frame for the matplotlib figure
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create the graph and draw it
        self.create_graph()
        self.draw_graph()

    def create_graph(self):
        # Create a simple graph with NetworkX
        self.graph = nx.Graph()

        # Adding nodes
        self.graph.add_node(1)
        self.graph.add_node(2)
        self.graph.add_node(3)
        self.graph.add_node(4)

        # Adding edges
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(2, 4)
        self.graph.add_edge(3, 4)

    def draw_graph(self):
        # Create a figure
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Draw the graph using the Spring layout
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=700, font_size=15)

        # Embedding the plot in the Tkinter GUI
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
