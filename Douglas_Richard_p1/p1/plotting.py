import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# helper function for cleaning timestamp strings
def date_stringto_float(x):
    time_split = x.split(':')
    h_sec = float(time_split[0]) * 24 * 60
    m_sec = float(time_split[1]) * 60
    sec = float(time_split[2])
    seconds = sum([h_sec,m_sec, sec])
    return seconds

class Plotting:
    def runtime_plot(time_log, hue_priority=None, file_value=''):
        df = pd.read_csv(time_log)
        df['algorithm'] = pd.Categorical(df['algorithm'], categories=hue_priority, ordered=True)
        df["runtime"] = df[f'runtime'].apply(lambda x: date_stringto_float(x))
        df_sorted = df.sort_values(by='algorithm')
        
        sns.set_theme(style="darkgrid")
        sns.color_palette("husl", 9)
        sns.catplot( data=df_sorted, x="input_size", y="runtime", hue="algorithm", hue_order=hue_priority, kind="point")
        
        plt.xlabel('Input Size (number of nodes)')
        plt.ylabel('Runtime (seconds)')
        plt.title("Measured Runtimes")
        
        plt.savefig(f"./logs/runtime_plots/{time_log.split('/')[-1].split('.')[0]}_{file_value}_plot.png")
    
    def cost_plot(cost_log, hue_priority = None, file_value=''):
        df = pd.read_csv(cost_log)
        df.drop(columns='runtime')

        # df_pivot = df.pivot(index="input_size", columns="algorithm", values="cost")
        # df['algorithm'] = pd.Categorical(df['algorithm'], categories=hue_priority, ordered=True)
        # df_sorted = df.sort_values(by='algorithm')
        
        sns.set_theme(style="darkgrid")
        sns.color_palette("husl", 9)
        sns.catplot(x='input_size', y='cost', hue='algorithm', kind="box", hue_order=hue_priority, data=df)
        
        plt.xlabel('Input Size')
        plt.ylabel('Cost')
        plt.title('Cost vs. Input Size')

        plt.savefig(f"./logs/cost_plots/{cost_log.split('/')[-1].split('.')[0]}_{file_value}_plot.png")

