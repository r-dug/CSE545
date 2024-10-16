import random
import datetime
import gui
import gc

class Genetic():
    def __init__(self, nodes, gui, gens = 2000, p_m = 0.01, N = 5000, start = "strong", cream = 2, track_elite = True, mutate="swap"):
        self.nodes = nodes # our same old dictionary of nodes in a tsp graph
        self.gui = gui
        
        self.generations = 0
        self.max_gens = gens
        self.runtime = None

        self.p_m = p_m
        
        self.chromosome_size = len(nodes.keys())
        self.pop_size = N
        self.pop_fitness = 0

        self.elites = []
        self.cream_max = int(N/cream)
        self.track_elite = track_elite
        
        self.best_cost = float('inf')
        self.best_child = []
        self.best_child_gen = 0
        
        self.mutations = 0

        self.parents = [] # a list of all "chromosomes" and their "fitness"
        self.children = []

        self.family_tree = []

        # for logging
        self.start_type = start
        # selecting initial population type between seeded with heuristic and not
        if start == "strong":
            self.initial_population = self.strong_start
        elif start == "random":
            self.initial_population = self.random_start
        self.initial_population
        # for selecting parent selection. only roulette seems viable, really
        self.select_parents = self.roulette
        
        # for logging
        self.mut = mutate
        # for selecting mutation function
        if mutate == "swap":
            self.mutate = self.swap_mutate
        elif mutate == "inversion":
            self.mutate = self.inversion_mutate


    def random_chrome(self):
        node_names = list(self.nodes.keys())
        start_node = node_names[0]
        
        visited = [start_node]
        unvisited = list(set(node_names)-set(visited))

        while len(visited) < len(self.nodes):
            rand_idx = random.randint(0, len(unvisited)-1)
            curr_node = unvisited[rand_idx]
            visited.append(curr_node)
            unvisited.remove(curr_node)
        visited.append(start_node)
        cost = self.calc_cost(visited)
        return visited, cost

    def sort_costs(self):
        node_names = list(self.nodes.keys())
        for name in node_names:
            self.nodes[name]["costs"] = dict(sorted(self.nodes[name]["costs"].items(), key=lambda item: item[1]))

    def greedy(self):
        self.sort_costs()
        node_names = list(self.nodes.keys())
        start_node = node_names[random.randint(1,len(node_names)-1)]
        visited = [node_names[0],start_node]
        unvisited = set(node_names)-set(visited)
        while len(visited) < len(node_names):
            curr = visited[-1]
            costs = list(self.nodes[curr]["costs"].items())
            for c in costs:
                if c[0] in unvisited:
                    visited.append(c[0])
                    unvisited.remove(c[0])
                    break
        visited.append(node_names[0])
        cost = self.calc_cost(visited)
        return visited, cost
    

    def strong_start(self):
        while len(self.parents) < self.cream_max:
            chromosome, cost = self.greedy()
            self.parents.append({"chromosome": chromosome, "cost": cost})

        while len(self.parents) < self.pop_size:
            chromosome, cost = self.random_chrome()
            self.parents.append({"chromosome": chromosome, "cost": cost})

    # generate N random traversals of graph
    def random_start(self):
        while len(self.parents) < self.pop_size:
            chromosome, cost = self.random_chrome()
            self.parents.append({"chromosome": chromosome, "cost": cost})
    
    # need not be run for initial population but all others must run this calculation
    def calc_cost(self, chromosome):
        cost = 0
        for i in range(len(chromosome)-1):
            j = i+1
            this_node = chromosome[i]
            next_node = chromosome[j]
            cost += self.nodes[this_node]["costs"][next_node]
        if cost < self.best_cost:
            self.best_cost = cost
            self.best_child = chromosome
            self.best_child_gen = self.generations
            # print(f"NEW BEST COST!!!\n\tcost: {self.best_cost}\n\t{self.best_child_gen}")
        return cost
    
    # measure fitness of all chromosomes
    def population_fitness(self):
        # Find the minimum and maximum costs in the current population
        costs = [p["cost"] for p in self.parents]
        max_cost = max(costs)
        min_cost = min(costs)
        # If max_cost == min_cost, we need to handle the degenerate case
        if max_cost == min_cost:
            # In this case, all individuals have the same fitness
            for p in self.parents:
                p["fitness"] = 1.0  # Assign equal fitness
            return
        # Normalize fitness based on the cost
        self.pop_fitness = 0
        for p in self.parents:
            # Invert the cost to make lower costs correspond to higher fitness
            # Normalization formula: (max_cost - cost) / (max_cost - min_cost)
            normalized_fitness = (max_cost - p["cost"]) / (max_cost - min_cost)
            p["fitness"] = normalized_fitness
            self.pop_fitness += normalized_fitness

        # normalize the fitness so that they sum to 1
        for p in self.parents:
            p["fitness"] /= self.pop_fitness


    def roulette(self):
        # Roulette wheel selection
        pick1 = random.random()
        pick2 = random.random()
        current = 0
        p1 = p2 = None

        for p in self.parents:
            current += p["fitness"]
            if current > pick1 and p1 == None:
                p1 = p
            if current > pick2 and p2 == None:
                p2 = p
            if p1 != None and p2 != None:
                break
        return p1, p2
    
    def create_offspring(self, parent1, parent2):
        p1 = parent1["chromosome"]
        p2 = parent2["chromosome"]
        if p1 == p2:
            c1_chrome = self.mutate(p1)
            cost1 = self.calc_cost(c1_chrome)
            child1 = {"chromosome" : c1_chrome, "cost" : cost1}
            return child1
        
        cross = random.randint(0,len(p1)-1)
        c1 = p1[:cross]
        c1 = self.chromosome_repair(c1,p2)

        # print("made children from crossover")
        return c1
    def chromosome_repair(self, chrome, parent):
        for gene in parent:
            if not gene in chrome:
                chrome.append(gene)
        chrome.append(parent[0])
        chrome = self.mutate(chrome)
        cost = self.calc_cost(chrome)
        child = {"chromosome" : chrome, "cost": cost}
        # print(cost)
        return child

    # mutators
    def swap_mutate(self, chromosome):
        if random.random() < self.p_m:
            i, j = sorted(random.sample(range(1, len(chromosome)-1), 2))
            temp = chromosome[i]
            chromosome[i] = chromosome[j]
            chromosome[j] = temp
            # print("Swap mutation occurred")
        return chromosome

    def inversion_mutate(self, chromosome):
        if random.random() < self.p_m:
            i, j = sorted(random.sample(range(1, int(len(chromosome)-2)), 2))
            chromosome[i:j] = reversed(chromosome[i:j])
            # print("Inversion mutation occurred")
        return chromosome

    def next_gen(self):
        while len(self.children) < self.pop_size - self.cream_max:
            p1, p2 = self.select_parents()
            try:
                c1 = self.create_offspring(p1,p2)
            except Exception as e:
                print(e)
            self.children.append(c1)
        self.children.extend(self.elites)

    # we can run this 
    def mating(self):
        start = datetime.datetime.now()
        self.children = []
        self.population_fitness()
        self.next_gen()
        self.parents = self.children
        if self.track_elite:
            self.elites = sorted(self.parents, key=lambda x: x["cost"])[:self.cream_max]
        mate_time  = datetime.datetime.now() - start
        if self.generations == 0:
            self.runtime = mate_time
        else:
            self.runtime += mate_time
        gui.animate_path(self.gui, f"gen:{self.generations}", self.best_child, 0, self.best_cost, {
                        "N": self.pop_size,
                        "initialize": self.start_type,
                        "p_m": self.p_m,
                        "mutation": self.mut,
                        "elites": self.track_elite,
                        "elite size": self.cream_max
                        })
        self.family_tree.append(
                {
                    "gen": self.generations,
                    "chromosome size":self.chromosome_size,
                    "parameters":{
                        "prob of mutation": self.p_m,
                        "mutation": self.mut, 
                        "elites": self.track_elite,
                        "elite size": self.cream_max
                        },
                    "runtime": self.runtime,
                    "best_child_cost": self.best_cost,
                    "best_gen": self.best_child_gen
                }
            )
    def check_convergence(self, threshold=50):
        if self.generations - self.best_child_gen >= threshold:
            print(f"Converged after {self.generations} generations.")
            return True
        return False

    def evolution(self):
        self.initial_population()
        while self.generations < self.max_gens:
            self.mating()
            self.generations += 1
            if self.check_convergence():
                break
            gc.collect()
        print("*"*25, "\nRUNTIME: ", self.runtime)
        print("*"*25, "\nBEST COST:\n\t",self.best_cost)
        print("*"*25, "\nBEST PATH:\n\t",self.best_child)
        print("*"*25)
