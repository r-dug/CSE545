import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

# helper function for cleaning timestamp strings
def date_stringto_float(x):
    time_split = x.split(':')
    h_sec = float(time_split[0]) * 24 * 60
    m_sec = float(time_split[1]) * 60
    sec = float(time_split[2])
    seconds = sum([h_sec,m_sec, sec])
    return seconds

def ensure_plot_path(desired_path, file_name):
    plots_path = f"{desired_path}{file_name}"
    path = ''
    for subdir in desired_path.split('/'):
        path += f"{subdir}/"
        if not os.path.isdir(path):
            os.mkdir(path)
    
    with open(plots_path, 'w') as plots:
        pass
    return plots_path

class Plotting:
    def runtime_plot(time_log, hue_priority=None, file_value=''):
        df = pd.read_csv(time_log)
        df['algorithm'] = pd.Categorical(df['algorithm'], categories=hue_priority, ordered=True)
        df["runtime"] = df[f'runtime'].apply(lambda x: date_stringto_float(x))
        df = df.round({"runtime": 2})
        df_sorted = df.sort_values(by='algorithm')
        
        sns.set_theme(style="darkgrid")
        sns.color_palette("husl", 9)
        sns.catplot( data=df_sorted, x="input_size", y="runtime", hue="algorithm", hue_order=hue_priority, kind="point")
        
        plt.xlabel('Input Size (number of nodes)')
        plt.ylabel('Runtime (seconds)')
        plt.title("Measured Runtimes")
        
        plots_path = ensure_plot_path(time_log, file_value, "runtimes")
        plt.savefig(plots_path)
    
    def cost_plot(cost_log, hue_priority = None, file_value=''):
        df = pd.read_csv(cost_log)
        df.drop(columns='runtime')
        
        sns.set_theme(style="darkgrid")
        sns.color_palette("husl", 9)
        sns.catplot(x='input_size', y='best_cost', hue='algorithm', sharex=False, kind="swarm", hue_order=hue_priority, data=df)
        
        plt.xlabel('Input Size')
        plt.ylabel('Cost')
        plt.title('Cost vs. Input Size')

        plots_path = ensure_plot_path(cost_log, file_value, "costs")
        plt.savefig(plots_path)
    
    def genetic_runtime_plot(cost_log, file_value=''):
        df = pd.read_csv(cost_log)
        df.drop(columns='gen')
        df["runtime"] = df[f'runtime'].apply(lambda x: date_stringto_float(x))
        df = df.round({"runtime": 2})
        no_elite_swap = df[df['parameters'].str.contains('False') & (df['parameters'].str.contains('swap'))]
        elite_swap = df[(df['parameters'].str.contains('True')) & (df['parameters'].str.contains('swap'))]
        no_elite_inversion = df[df['parameters'].str.contains('False') & (df['parameters'].str.contains('inversion'))]
        elite_inversion = df[(df['parameters'].str.contains('True')) & (df['parameters'].str.contains('inversion'))]

        def plot_df (df, title):
            fig, ax = plt.subplots(figsize=(16,16), constrained_layout=True)
            sns.set_theme(style="darkgrid")
            sns.color_palette("husl", 9)
            sns.lineplot(x='runtime', y='best_child_cost', hue='parameters', data=df, ax=ax)
            
            plt.xlabel('runtime (sec)')
            plt.ylabel('Cost')
            plt.title(title)
            ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
            # desired path ex: ./logs/costs/N/random/inversion_elite.jpeg
            N = cost_log.split('/')[-2]
            start_type = cost_log.split('/')[-1].split('.')[-2].split("_")[0]
            desired_path = f'./plots/runtime_graphs/{N}/{start_type}'
            file_name = f'/{title}.jpeg'
            plots_path = ensure_plot_path(desired_path, file_name)
            plt.savefig(f"{plots_path}")
            print(f"saved to {plots_path}")
            plt.close()
        plot_df(no_elite_swap, "no_elite_swap")
        plot_df(elite_swap, "elite_swap")
        plot_df(no_elite_inversion, "no_elite_inversion")
        plot_df(elite_inversion, "elite_inversion")

    def genetic_gen_plot(cost_log, file_value=''):
        df = pd.read_csv(cost_log)
        df.drop(columns='runtime')
        no_elite_swap = df[df['parameters'].str.contains('False') & (df['parameters'].str.contains('swap'))]
        elite_swap = df[(df['parameters'].str.contains('True')) & (df['parameters'].str.contains('swap'))]
        no_elite_inversion = df[df['parameters'].str.contains('False') & (df['parameters'].str.contains('inversion'))]
        elite_inversion = df[(df['parameters'].str.contains('True')) & (df['parameters'].str.contains('inversion'))]

        def plot_df (df, title):
            fig, ax = plt.subplots(figsize=(16,16), constrained_layout=True)
            sns.set_theme(style="darkgrid")
            sns.color_palette("husl", 9)
            sns.lineplot(x='gen', y='best_child_cost', hue='parameters', data=df, ax=ax)
            
            plt.xlabel('Generation')
            plt.ylabel('Cost')
            plt.title(title)
            ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
            # desired path ex: ./logs/costs/N/random/inversion_elite.jpeg
            N = cost_log.split('/')[-2]
            start_type = cost_log.split('/')[-1].split('.')[-2].split("_")[0]
            desired_path = f'./plots/cost_graphs/{N}/{start_type}'
            file_name = f'/{title}.jpeg'
            plots_path = ensure_plot_path(desired_path, file_name)
            plt.savefig(f"{plots_path}")
            print(f"saved to {plots_path}")
            plt.close()
        plot_df(no_elite_swap, "no_elite_swap")
        plot_df(elite_swap, "elite_swap")
        plot_df(no_elite_inversion, "no_elite_inversion")
        plot_df(elite_inversion, "elite_inversion")
        
if __name__ == '__main__':
    csv = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.split('.')[-1] == "csv":
                csv.append(f"{os.path.join(root,file)}")
    print(csv)
    for c in csv:
        # Plotting.genetic_gen_plot(c)
        Plotting.genetic_runtime_plot(c)
        print(f"plotted {c} by generation")