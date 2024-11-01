# visualization of the trend analysis
import matplotlib.pyplot as plt
import seaborn as sns

def plot_trend_analysis(data):
    # set up the figure
    fig, ax = plt.subplots(figsize=(10, 6)) 

    # plot the price first
    sns.lineplot(x='date', y='close', data=data, ax=ax) 

    # plot the buy_or_sell spot
    sns.scatterplot(x='date',y='buy_or_sell',data=data,ax=ax)

    plt.show()